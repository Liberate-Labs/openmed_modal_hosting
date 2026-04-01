from openmed import BatchProcessor

print("=" * 80)
print("BATCH PROCESSING")
print("=" * 80)

batch_texts = [
    "Patient: John Doe, DOB: 01/15/1970, SSN: 123-45-6789",
    "Dr. Sarah Johnson, Phone: (555) 123-4567, Email: sarah@email.com",
    "MRN: 87654321, Admission: 2024-03-20, Discharge: 2024-03-25",
    "Address: 123 Main Street, Boston, MA 02101, ZIP: 02101",
    "Contact: patient.name@hospital.org, Emergency: (555) 987-6543",
]

processor = BatchProcessor(
    model_name="openmed/OpenMed-PII-SuperClinical-Large-434M-v1",
    confidence_threshold=0.5,
    group_entities=True,
    continue_on_error=True,
)

batch_result = processor.process_texts(batch_texts)

print("Batch processing completed!")
print(f"  Total items: {batch_result.total_items}")
print(f"  Successful: {batch_result.successful_items}")
print(f"  Failed: {batch_result.failed_items}")
print(f"  Total processing time: {batch_result.total_processing_time:.2f}s")

print("\n" + "-" * 80)
print("Results per note:\n")

for item_result in batch_result.items:
    if not item_result.success:
        print(f"❌ {item_result.id}: {item_result.error}")
        continue

    ents = item_result.result.entities
    print(f"📄 {item_result.id}:")
    print(f"   Entities found: {len(ents)}")
    for entity in ents[:3]:
        print(f"     - [{entity.label}] '{entity.text}'")
    if len(ents) > 3:
        print(f"     ... and {len(ents) - 3} more")
    print()
