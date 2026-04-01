import time
import modal

MODEL_NAME = "openmed/OpenMed-PII-SuperClinical-Large-434M-v1"

app = modal.App("openmed-pii-detection")

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        "openmed==0.6.4",
        "fastapi>=0.116.0",
        "torch>=2.0",
        "transformers>=4.57.1",
        "huggingface-hub>=0.30",
        "accelerate>=0.29",
        "pysbd>=0.3.4",
    )
    .run_commands(
        "python -c \""
        "from huggingface_hub import snapshot_download; "
        f"snapshot_download('{MODEL_NAME}')"
        "\""
    )
)

@app.cls(
    gpu="L4",
    image=image,
    scaledown_window=300,
    timeout=600,
)
@modal.concurrent(max_inputs=50)
class PIIDetectionService:
    @modal.enter()
    def load_model(self):
        from openmed import ModelLoader

        self.model_name = MODEL_NAME
        self.loader = ModelLoader()
        self.loader.create_pipeline(
            self.model_name,
            task="token-classification",
            aggregation_strategy="simple",
        )
        print(f"Model {self.model_name} loaded successfully")

    @modal.asgi_app()
    def fastapi_app(self):
        from fastapi import FastAPI
        from pydantic import BaseModel
        from typing import Optional

        api = FastAPI(title="OpenMed PII Detection")

        class PIIRequest(BaseModel):
            text: str
            confidence_threshold: float = 0.5
            use_smart_merging: bool = True

        class BatchPIIRequest(BaseModel):
            texts: list[str]
            confidence_threshold: float = 0.5
            use_smart_merging: bool = True

        class EntityResponse(BaseModel):
            text: str
            label: str
            confidence: float
            start: Optional[int] = None
            end: Optional[int] = None

        class PIIResponse(BaseModel):
            entities: list[EntityResponse]
            entity_count: int
            processing_time_ms: float

        class BatchItemResponse(BaseModel):
            id: str
            success: bool
            entities: list[EntityResponse]
            entity_count: int
            error: Optional[str] = None

        class BatchPIIResponse(BaseModel):
            items: list[BatchItemResponse]
            total_items: int
            successful_items: int
            failed_items: int
            total_processing_time_ms: float

        @api.get("/")
        def health_check():
            return {"status": "ok", "model": self.model_name}

        @api.post("/extract_pii", response_model=PIIResponse)
        def extract_pii_endpoint(request: PIIRequest):
            from openmed import extract_pii

            start = time.perf_counter()
            result = extract_pii(
                request.text,
                model_name=self.model_name,
                confidence_threshold=request.confidence_threshold,
                use_smart_merging=request.use_smart_merging,
                loader=self.loader,
            )
            elapsed_ms = (time.perf_counter() - start) * 1000

            entities = [
                EntityResponse(
                    text=e.text,
                    label=e.label,
                    confidence=round(e.confidence, 4),
                    start=e.start,
                    end=e.end,
                )
                for e in result.entities
            ]
            return PIIResponse(
                entities=entities,
                entity_count=len(entities),
                processing_time_ms=round(elapsed_ms, 2),
            )

        @api.post("/batch_extract_pii", response_model=BatchPIIResponse)
        def batch_extract_pii_endpoint(request: BatchPIIRequest):
            from openmed import extract_pii

            batch_start = time.perf_counter()
            items = []
            successful = 0
            failed = 0

            for idx, text in enumerate(request.texts):
                item_id = f"item_{idx}"
                try:
                    result = extract_pii(
                        text,
                        model_name=self.model_name,
                        confidence_threshold=request.confidence_threshold,
                        use_smart_merging=request.use_smart_merging,
                        loader=self.loader,
                    )
                    entities = [
                        EntityResponse(
                            text=e.text,
                            label=e.label,
                            confidence=round(e.confidence, 4),
                            start=e.start,
                            end=e.end,
                        )
                        for e in result.entities
                    ]
                    items.append(BatchItemResponse(
                        id=item_id,
                        success=True,
                        entities=entities,
                        entity_count=len(entities),
                    ))
                    successful += 1
                except Exception as e:
                    items.append(BatchItemResponse(
                        id=item_id,
                        success=False,
                        entities=[],
                        entity_count=0,
                        error=str(e),
                    ))
                    failed += 1

            total_ms = (time.perf_counter() - batch_start) * 1000
            return BatchPIIResponse(
                items=items,
                total_items=len(request.texts),
                successful_items=successful,
                failed_items=failed,
                total_processing_time_ms=round(total_ms, 2),
            )

        return api
