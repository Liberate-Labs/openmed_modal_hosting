# OpenMed PII Detection — Benchmark Results

**Model:** `openmed/OpenMed-PII-SuperClinical-Large-434M-v1`
**Platform:** Modal (Serverless)
**Endpoint:** REST API (FastAPI)

---

## T4 GPU (16GB VRAM)

### Single Text Extraction


| Input Size   | Entities | Server (s) | Round-trip (s) |
| ------------ | -------- | ---------- | -------------- |
| ~400 tokens  | 32       | 8.4        | 9.6            |
| ~700 tokens  | 80       | 12.5       | 13.9           |
| ~1000 tokens | 133      | 20.8       | 22.4           |
| ~1300 tokens | 184      | 25.0       | 26.4           |
| ~1500 tokens | 241      | 34.5       | 35.9           |

### Batch Processing (5 texts — same inputs)

| Metric                   | Value       |
| ------------------------ | ----------- |
| Total texts              | 5           |
| Total entities detected  | 670         |
| Server processing time   | 94.1s       |
| Round-trip time          | 96.1s       |
| Avg server time per text | 18.8s       |

---

## L4 GPU (24GB VRAM)

### Single Text Extraction

| Input Size   | Entities | Server (s) | Round-trip (s) |
| ------------ | -------- | ---------- | -------------- |
| ~400 tokens  | 32       | 5.8        | 7.0            |
| ~700 tokens  | 80       | 11.7       | 12.8           |
| ~1000 tokens | 133      | 18.7       | 20.1           |
| ~1300 tokens | 184      | 23.0       | 24.7           |
| ~1500 tokens | 241      | 34.5       | 36.0           |

### Batch Processing (5 texts — same inputs)

| Metric                   | Value       |
| ------------------------ | ----------- |
| Total texts              | 5           |
| Total entities detected  | 670         |
| Server processing time   | 92.2s       |
| Round-trip time          | 93.9s       |
| Avg server time per text | 18.4s       |
