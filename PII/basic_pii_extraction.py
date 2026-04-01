import time
from openmed import ModelLoader, extract_pii

MODEL_NAME = "openmed/OpenMed-PII-SuperClinical-Large-434M-v1"

load_start = time.perf_counter()
loader = ModelLoader()
loader.create_pipeline(MODEL_NAME, task="token-classification", aggregation_strategy="simple")
load_ms = (time.perf_counter() - load_start) * 1000
print(f"Model loaded in {load_ms:.1f}ms")

teacher_report_text = """
ANNUAL PERFORMANCE EVALUATION REPORT — ACADEMIC YEAR 2023–2024
Greenfield Unified School District
Prepared by: Dr. Margaret L. Harrington, Superintendent
Office Address: 88 District Boulevard, Springfield, IL 62704
Contact: (217) 555-0192 | m.harrington@greenfieldusd.edu

This report documents the formal annual performance evaluations for all certified teaching staff
employed by Greenfield Unified School District during the 2023–2024 academic year. Evaluations
were conducted in accordance with Illinois Administrative Code Part 50 and district Board Policy
5120. All personally identifiable information contained herein is protected under FERPA and the
Illinois School Student Records Act. Unauthorized disclosure is prohibited. Questions regarding
this document should be directed to the Office of Human Resources at (217) 555-0192 or via email
to hr@greenfieldusd.edu. Physical correspondence should be sent to 88 District Boulevard,
Springfield, IL 62704, Attention: HR Records Division.

------------------------------------------------------------------------
TEACHER 1
------------------------------------------------------------------------
Full Name: Prof. James R. Thornton
Employee ID: EMP-20341
Date of Birth: 07/22/1979
Social Security Number: 547-83-2910
Home Address: 14 Maplewood Lane, Apt 3B, Decatur, IL 62521
Personal Phone: (217) 555-3847
Work Email: j.thornton@greenfieldusd.edu
Emergency Contact: Linda Thornton — (217) 555-9201

Subject Taught: Advanced Placement Chemistry (Grades 11–12)
Years of Service: 14 years

Performance Summary:
Prof. James R. Thornton has consistently demonstrated outstanding pedagogical skill throughout the
2023–2024 academic year. His student pass rate in AP Chemistry reached 91%, the highest in the
district. Peer evaluators noted his structured lesson plans and data-driven approach to formative
assessment. He was formally observed on 04/11/2024 by Principal Dr. Roberta N. Fields
(DOB: 11/03/1968, SSN: 312-67-5490, office@fields.greenfield.edu), who rated his performance as
Exemplary. Thornton attended the National Science Teachers Conference in Denver, CO 80202 on
March 14–16, 2024 and presented a well-received workshop on project-based learning in secondary
chemistry. His laboratory redesign proposal, submitted to the district facilities committee, was
approved for a $32,000 renovation grant funded jointly by the state and the Thornton Family
Foundation. He holds an Illinois Teaching Certificate No. IL-TCH-004821 valid through 06/30/2027
and a National Board Certification (NB-CHEM-2019-7734). His direct deposit is linked to account
ending 6641 at Midwest Community Bank, routing number 071923284. Emergency medical contact:
Dr. Patricia Nguyen, (217) 555-0044, p.nguyen@springfieldmed.org, 901 Medical Plaza,
Springfield, IL 62702.

Professional Development Log (Teacher 1):
  - 08/14/2023: District Induction Day, Greenfield Professional Center, Springfield, IL
  - 09/22/2023: Formative Assessment Strategies Workshop, 44 Lake Drive, Decatur, IL 62522
  - 11/10/2023: AP Chemistry Grader Training, College Board Regional Office, Chicago, IL 60604
  - 03/14/2024: NSTA Annual Conference, Colorado Convention Center, Denver, CO 80202
  - 05/03/2024: Illinois Science Teachers Association Symposium, Normal, IL 61761

Personal Notes on File: Thornton submitted a formal accommodation request on 01/08/2024
referencing a medical diagnosis (confidential under ADA). HR correspondence was handled by
benefits coordinator Ms. Rachel Gibson, r.gibson@greenfieldusd.edu, (217) 555-0033. His
FMLA paperwork was processed by third-party administrator OptumHealth, case reference
FMLA-2024-THN-00482, contact 1-866-555-0120. Thornton's professional references on file:
Dr. Alan Marsh, a.marsh@uiuc.edu, (217) 244-1100, 505 S. Goodwin Avenue, Urbana, IL 61801;
and Prof. Carla Stevenson, c.stevenson@siu.edu, (618) 453-2121, Mail Code 4301, Carbondale, IL 62901.


End of Report. Prepared by: Ms. Beverly K. Cross, Records Officer, bev.cross@greenfieldusd.edu,
(217) 555-8844, 88 District Boulevard, Springfield, IL 62704. Date: 06/20/2024.
"""

expected_entities = [
    ("first_name", "Margaret"), ("last_name", "Harrington"),
    ("street_address", "88 District Boulevard"), ("city", "Springfield"), ("state", "IL"), ("postcode", "62704"),
    ("phone_number", "(217) 555-0192"), ("email", "m.harrington@greenfieldusd.edu"),
    ("email", "hr@greenfieldusd.edu"),
    ("first_name", "James"), ("last_name", "Thornton"),
    ("date_of_birth", "07/22/1979"), ("ssn", "547-83-2910"),
    ("street_address", "14 Maplewood Lane"), ("city", "Decatur"), ("state", "IL"), ("postcode", "62521"),
    ("phone_number", "(217) 555-3847"), ("email", "j.thornton@greenfieldusd.edu"),
    ("first_name", "Linda"), ("last_name", "Thornton"), ("phone_number", "(217) 555-9201"),
    ("first_name", "Roberta"), ("last_name", "Fields"),
    ("date_of_birth", "11/03/1968"), ("ssn", "312-67-5490"), ("email", "office@fields.greenfield.edu"),
    ("city", "Denver"), ("state", "CO"), ("postcode", "80202"),
    ("bank_routing_number", "071923284"),
    ("first_name", "Patricia"), ("last_name", "Nguyen"),
    ("phone_number", "(217) 555-0044"), ("email", "p.nguyen@springfieldmed.org"),
    ("street_address", "901 Medical Plaza"), ("city", "Springfield"), ("state", "IL"), ("postcode", "62702"),
    ("street_address", "44 Lake Drive"), ("city", "Decatur"), ("state", "IL"), ("postcode", "62522"),
    ("city", "Chicago"), ("state", "IL"), ("postcode", "60604"),
    ("first_name", "Rachel"), ("last_name", "Gibson"),
    ("email", "r.gibson@greenfieldusd.edu"), ("phone_number", "(217) 555-0033"),
    ("phone_number", "1-866-555-0120"),
    ("first_name", "Alan"), ("last_name", "Marsh"),
    ("email", "a.marsh@uiuc.edu"), ("phone_number", "(217) 244-1100"),
    ("street_address", "505 S. Goodwin Avenue"), ("city", "Urbana"), ("state", "IL"), ("postcode", "61801"),
    ("first_name", "Carla"), ("last_name", "Stevenson"),
    ("email", "c.stevenson@siu.edu"), ("phone_number", "(618) 453-2121"),
    ("city", "Carbondale"), ("state", "IL"), ("postcode", "62901"),
]

print(f"Expected entity count: {len(expected_entities)}")

start = time.perf_counter()
result_teacher = extract_pii(
    teacher_report_text,
    model_name=MODEL_NAME,
    confidence_threshold=0.5,
    use_smart_merging=True,
    loader=loader,
)
latency_ms = (time.perf_counter() - start) * 1000

print(f"Found {len(result_teacher.entities)} PII entities (latency: {latency_ms:.1f}ms):\n")
for i, entity in enumerate(result_teacher.entities, 1):
    print(f"{i:2d}. [{entity.label:25s}] '{entity.text:30s}' (confidence: {entity.confidence:.3f})")

print("\n" + "=" * 80)
