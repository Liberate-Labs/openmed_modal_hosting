import time
import json
import requests

BASE_URL = "https://liberate-ai--openmed-pii-detection-piidetectionservice-f-128896.modal.run"

# ─────────────────────────────────────────────────────────────────────────────
# Test Texts — varying token sizes (~400, ~700, ~1000, ~1300, ~1500 tokens)
# ─────────────────────────────────────────────────────────────────────────────

TEXT_400 = """
Patient Intake Form — Community Health Center
Date: 03/15/2024
Patient Name: Sarah Michelle Patterson
Date of Birth: 06/14/1988
Social Security Number: 298-47-5631
Home Address: 742 Evergreen Terrace, Apt 12B, Portland, OR 97201
Phone: (503) 555-0147
Email: s.patterson@gmail.com
Emergency Contact: David Patterson (Spouse) — (503) 555-0298

Primary Care Physician: Dr. Amanda Chen, NPI: 1234567890
Phone: (503) 555-0333, Email: a.chen@commhealth.org
Office: 200 Medical Drive, Suite 400, Portland, OR 97210

Insurance: Aetna PPO, Policy#: AET-882341, Group: GRP-5500
Subscriber: Sarah M. Patterson, Member ID: SPT-992210

Chief Complaint: Patient reports persistent lower back pain for 3 weeks.
Allergies: Penicillin, Sulfa drugs
Current Medications: Lisinopril 10mg daily, Metformin 500mg twice daily

Referring Provider: Dr. James Liu, Fax: (503) 555-0411, j.liu@orthopnw.com
Lab Orders sent to Quest Diagnostics, Account: QD-77421, Contact: 1-800-555-0199
"""

TEXT_700 = """
DISCHARGE SUMMARY — MEMORIAL GENERAL HOSPITAL
Record ID: DSR-2024-04521
Date of Admission: 02/28/2024
Date of Discharge: 03/05/2024

Patient Information:
Full Name: Robert James Williamson
Date of Birth: 11/22/1965
Social Security Number: 412-68-9033
Home Address: 1847 Oakwood Boulevard, Unit 5, Chicago, IL 60616
Personal Phone: (312) 555-0184
Work Phone: (312) 555-0290
Email: r.williamson@protonmail.com
Employer: Midwest Engineering Corp, 500 Industrial Parkway, Chicago, IL 60607

Emergency Contacts:
1. Patricia Williamson (Wife) — (312) 555-0285, p.williamson@yahoo.com
2. Thomas Williamson (Son) — (773) 555-0192, Address: 330 Lakeview Ave, Evanston, IL 60201

Insurance Information:
Primary: Blue Cross Blue Shield of Illinois, Policy#: BCBS-IL-7723401
Group: GRP-MEC-200, Subscriber ID: RJW-441298
Secondary: Medicare Part B, Beneficiary ID: 1EG4-TE5-MK72

Attending Physician: Dr. Priya Anand, MD, FACC
NPI: 9876543210, License: IL-MD-045892
Office: 1200 Michigan Avenue, Suite 800, Chicago, IL 60605
Phone: (312) 555-0377, Fax: (312) 555-0378
Email: p.anand@memorialhospital.org

Consulting Physicians:
1. Dr. Michael Torres, Pulmonology, NPI: 5678901234, m.torres@memorialhospital.org
2. Dr. Karen Johansson, Endocrinology, Phone: (312) 555-0401, k.johansson@uchicago.edu

Admission Diagnosis: Acute exacerbation of congestive heart failure (CHF), NYHA Class III
Secondary Diagnoses: Type 2 Diabetes Mellitus, Chronic Kidney Disease Stage 3a, Hypertension

Hospital Course:
Mr. Williamson presented to the ED on 02/28/2024 with progressive dyspnea, orthopnea, and bilateral
lower extremity edema over 5 days. Initial labs showed BNP 1,842 pg/mL, Creatinine 1.9 mg/dL,
HbA1c 8.2%. Chest X-ray demonstrated bilateral pleural effusions and cardiomegaly. Echocardiogram
on 03/01/2024 revealed LVEF 30%, moderate mitral regurgitation. Patient was managed with IV
furosemide diuresis, achieving net negative fluid balance of 4.2 liters over 5 days.

Discharge Medications:
- Furosemide 40mg PO BID, Lisinopril 20mg daily, Carvedilol 12.5mg BID
- Metformin 1000mg BID, Empagliflozin 10mg daily, Aspirin 81mg daily

Follow-up Appointments:
- Dr. Priya Anand, Cardiology: 03/12/2024 at 10:00 AM, (312) 555-0377
- Dr. Karen Johansson, Endocrinology: 03/19/2024, (312) 555-0401
- Lab work at Quest Diagnostics (Account: QD-CHI-88210): 03/10/2024

Discharge Planner: Nancy Rivera, RN, BSN, Phone: (312) 555-0450, n.rivera@memorialhospital.org
Dictated by: Dr. Priya Anand, 03/05/2024 14:32 CST
"""

TEXT_1000 = """
COMPREHENSIVE BEHAVIORAL HEALTH ASSESSMENT
Facility: Sunrise Behavioral Health Institute
Facility Address: 3200 Wellness Way, Suite 100, Austin, TX 78701
Phone: (512) 555-0100, Fax: (512) 555-0101
Assessment Date: 01/18/2024
Clinician: Dr. Rebecca Foster, PhD, Licensed Psychologist
License: TX-PSY-34521, NPI: 3456789012
Email: r.foster@sunrisebhi.com, Phone: (512) 555-0115

PATIENT DEMOGRAPHICS:
Full Name: Alexandra Nicole Vasquez
Preferred Name: Alex
Date of Birth: 09/03/1995
Age: 28 years
Social Security Number: 523-71-8844
Gender: Female
Ethnicity: Hispanic/Latina
Primary Language: English, Secondary: Spanish

Contact Information:
Home Address: 1605 South Lamar Boulevard, Apt 204, Austin, TX 78704
Mailing Address: PO Box 4421, Austin, TX 78765
Cell Phone: (512) 555-0267
Home Phone: (512) 555-0268
Email: alex.vasquez95@outlook.com
Employer: TechVista Solutions, 800 Congress Avenue, Floor 12, Austin, TX 78701
Work Phone: (512) 555-0500, Supervisor: Mark Henderson, m.henderson@techvista.com

Emergency Contacts:
1. Maria Elena Vasquez (Mother) — (210) 555-0334, m.vasquez@sbcglobal.net
   Address: 445 Riverwalk Drive, San Antonio, TX 78205
2. Carlos Vasquez (Father) — (210) 555-0335, c.vasquez@gmail.com
3. Jennifer Park (Friend) — (512) 555-0401, j.park@gmail.com

Insurance Information:
Primary: United Healthcare Choice Plus
Policy Number: UHC-TX-9921054
Group Number: GRP-TVS-300
Subscriber: Alexandra N. Vasquez
Member ID: ANV-887213
Claims Address: PO Box 740800, Atlanta, GA 30374
Authorization Phone: 1-800-555-0234

Secondary: None

Referral Source:
Dr. Stephen Garcia, MD, Primary Care Physician
Practice: Central Texas Family Medicine
Address: 2100 Red River Street, Austin, TX 78705
Phone: (512) 555-0188, Fax: (512) 555-0189
Email: s.garcia@ctfamilymed.com, NPI: 7890123456

PRESENTING CONCERNS:
Patient self-referred following recommendation from PCP Dr. Garcia. Reports experiencing persistent
anxiety symptoms for approximately 8 months, worsening over the past 3 months. Symptoms include
excessive worry about work performance, difficulty sleeping (averaging 4-5 hours per night),
muscle tension, irritability, and difficulty concentrating. Patient reports two panic attacks in the
past month — the first occurred on 12/15/2023 at her workplace and the second on 01/05/2024 while
driving on I-35. She pulled over at the Shell station at 7800 N. Lamar Blvd and called 911.
EMS responded but no transport was needed. Incident report filed by Paramedic Tony Russo,
Badge#: AFD-2247, t.russo@austinfd.gov.

PSYCHIATRIC HISTORY:
Previous treatment with Dr. Linda Nakamura, LCSW, at Balanced Mind Counseling, 900 West Avenue,
Austin, TX 78701, Phone: (512) 555-0322, l.nakamura@balancedmind.com. Attended 12 sessions
from 06/2022 to 11/2022 for adjustment disorder. Records requested on 01/10/2024.
Previous medication trial: Sertraline 50mg prescribed by Dr. Garcia, taken 07/2022 to 10/2022,
discontinued due to GI side effects. No history of psychiatric hospitalization.

FAMILY HISTORY:
Mother (Maria, age 56): Generalized Anxiety Disorder, treated by Dr. Rosa Delgado,
(210) 555-0440, r.delgado@alamopsych.com
Father (Carlos, age 59): No psychiatric history, Hypertension, Type 2 Diabetes
Sister (Isabella Vasquez, age 24): No psychiatric history
  Address: 1200 University Avenue, Apt 8, San Marcos, TX 78666
  Phone: (512) 555-0477, i.vasquez@txstate.edu

SUBSTANCE USE:
Alcohol: Social use, 2-3 drinks per weekend. Denies binge drinking.
Tobacco: Never. Cannabis: Occasional use, approximately 1-2 times per month.
Prescription misuse: Denied. Illicit substances: Denied.

MEDICAL HISTORY:
Current PCP: Dr. Stephen Garcia (see above)
Pharmacy: Walgreens #5521, 1000 East 41st Street, Austin, TX 78751
  Pharmacist: Jennifer Tran, RPh, Phone: (512) 555-0600
Allergies: Codeine (nausea/vomiting), Latex (contact dermatitis)
Current Medications: Oral contraceptive (Yaz), Vitamin D 2000 IU daily, Melatonin 5mg PRN

ASSESSMENT RESULTS:
PHQ-9 Score: 12 (Moderate depression)
GAD-7 Score: 16 (Severe anxiety)
PCL-5 Score: 18 (Below clinical threshold for PTSD)
"""

TEXT_1300 = """
WORKERS' COMPENSATION INDEPENDENT MEDICAL EXAMINATION REPORT
Case Number: WC-2024-FL-08834
Carrier: Hartford Insurance Company, Claims Division
Claims Adjuster: Barbara Mitchell, Phone: (860) 555-0220, b.mitchell@hartford.com
Attorney for Claimant: Richard Goldstein, Esq., Goldstein & Associates
  Address: 200 South Biscayne Boulevard, Suite 3100, Miami, FL 33131
  Phone: (305) 555-0155, Fax: (305) 555-0156, r.goldstein@goldsteinlaw.com
  Paralegal: Christine Yu, c.yu@goldsteinlaw.com, (305) 555-0157
Attorney for Employer: Laura Whitfield, Esq., Whitfield Palmer LLP
  Address: 100 SE 2nd Street, Suite 2800, Miami, FL 33131
  Phone: (305) 555-0199, l.whitfield@whitfieldpalmer.com

EXAMINING PHYSICIAN:
Name: Dr. Howard J. Bernstein, MD, FAAOS
Board Certification: Orthopedic Surgery, Sports Medicine
License: FL-MD-OS-78432, NPI: 4567890123
Practice: South Florida Orthopedic Associates
Address: 7500 SW 87th Avenue, Suite 300, Miami, FL 33173
Phone: (305) 555-0300, Fax: (305) 555-0301
Email: h.bernstein@sforthopedic.com

CLAIMANT INFORMATION:
Full Name: Miguel Antonio Reyes-Castillo
Date of Birth: 04/17/1982
Age: 41 years
Social Security Number: 591-24-8867
Home Address: 14220 SW 152nd Street, Miami, FL 33177
Cell Phone: (786) 555-0412
Email: m.reyescastillo@icloud.com
Marital Status: Married
Spouse: Ana Lucia Reyes, Phone: (786) 555-0413, a.reyes@hotmail.com
Dependents: 3 children (ages 14, 11, 7)

Employer: Atlantic Coast Construction, Inc.
Employer Address: 8900 NW 33rd Street, Doral, FL 33172
Employer Phone: (305) 555-0500
Supervisor: Frank Delaney, f.delaney@atlanticcoast.com, (305) 555-0502
HR Contact: Sandra Kim, s.kim@atlanticcoast.com, (305) 555-0501

INJURY DETAILS:
Date of Injury: 09/12/2023
Location: Construction site at 1 Brickell City Centre, Miami, FL 33131
Description: Claimant, employed as a journeyman electrician (Employee ID: ACC-E-4421), was working
on the 14th floor of a commercial high-rise project when he slipped on wet concrete and fell
approximately 8 feet from scaffolding, landing on his left side. Co-worker Pedro Alvarez
(Badge: ACC-E-5567, Phone: (786) 555-0480, p.alvarez@atlanticcoast.com) witnessed the incident
and called site safety officer Thomas Burke (Phone: (305) 555-0510, t.burke@atlanticcoast.com).

OSHA Incident Report: OSHA-FL-2023-09-44218
First Responder: Miami-Dade Fire Rescue, Station 47, Paramedic Lisa Fernandez, Badge#: MDFR-2891
Transport: Jackson Memorial Hospital ED, Trauma Bay 4, Arrival: 09/12/2023 at 14:47 EST

TREATMENT HISTORY:
1. Emergency Department — Jackson Memorial Hospital, 09/12/2023
   Attending: Dr. Raj Patel, MD, Emergency Medicine
   Phone: (305) 555-0600, r.patel@jhsmiami.org
   Findings: Left shoulder dislocation, left lateral rib fractures (ribs 7-9), left hip contusion
   Treatment: Closed reduction of shoulder, pain management, discharged 09/13/2023

2. Orthopedic Follow-up — Dr. Carmen Iglesias, MD
   Practice: Miami Bone & Joint Center, 6200 Sunset Drive, Suite 401, South Miami, FL 33143
   Phone: (305) 555-0650, Fax: (305) 555-0651, c.iglesias@miamiboneandjoint.com
   NPI: 2345678901, License: FL-MD-OS-65210
   Visits: 09/20/2023, 10/04/2023, 10/25/2023, 11/15/2023, 12/13/2023, 01/17/2024
   Treatment: Physical therapy referral, Tramadol 50mg Q6H PRN, Meloxicam 15mg daily
   MRI Left Shoulder (10/02/2023): Partial thickness rotator cuff tear, Hill-Sachs lesion
   MRI Left Hip (10/02/2023): Labral tear, bone marrow edema

3. Physical Therapy — ProMotion Rehabilitation
   Therapist: Angela Washington, DPT, License: FL-PT-11234
   Address: 9400 S. Dixie Highway, Suite 200, Pinecrest, FL 33156
   Phone: (305) 555-0700, a.washington@promotionrehab.com
   Sessions completed: 24 of 36 authorized (09/25/2023 to 01/15/2024)
   Progress: ROM improved from 90 to 145 flexion, strength 4/5 in abduction

4. Pain Management — Dr. Victor Huang, MD
   Practice: Comprehensive Pain Solutions, 5000 University Drive, Coral Gables, FL 33146
   Phone: (305) 555-0750, v.huang@comprehensivepain.com, NPI: 6789012345
   Left shoulder subacromial injection: 11/01/2023, 12/20/2023
   Left hip intra-articular injection: 11/15/2023

CURRENT MEDICATIONS:
Prescribed by Dr. Iglesias: Tramadol 50mg Q6H PRN, Meloxicam 15mg daily, Cyclobenzaprine 10mg QHS
Prescribed by Dr. Huang: Gabapentin 300mg TID (started 12/20/2023)
OTC: Acetaminophen 500mg PRN, Omega-3 fish oil, Multivitamin
Pharmacy: CVS #6632, 15200 SW 127th Avenue, Miami, FL 33196, Phone: (305) 555-0800

EXAMINATION DATE: 01/22/2024

PHYSICAL EXAMINATION FINDINGS:
General: Well-developed, well-nourished male in no acute distress. Height: 5'10", Weight: 195 lbs.
Left Shoulder: Mild anterior capsular laxity, positive apprehension test, positive O'Brien's test.
Active ROM: Flexion 145, Abduction 130, External rotation 60, Internal rotation T12.
Left Hip: Antalgic gait pattern, positive FADIR test, pain with resisted internal rotation.
Active ROM: Flexion 110, Internal rotation 15, External rotation 35.
Neurovascular: Intact distally. No signs of complex regional pain syndrome.

MEDICAL RECORDS REVIEWED:
Jackson Memorial Hospital ED records (09/12-13/2023), obtained from Medical Records Dept,
Contact: Maria Santos, m.santos@jhsmiami.org, (305) 555-0610
Dr. Iglesias office records (09/20/2023 to 01/17/2024), 142 pages
ProMotion Rehabilitation therapy notes, 24 visits
Dr. Huang pain management records, 3 visits
MRI reports from Advanced Imaging of Miami, 2300 Coral Way, Miami, FL 33145
  Radiologist: Dr. Neil Patterson, n.patterson@advancedimaging.com, (305) 555-0450

Report prepared by: Dr. Howard J. Bernstein, MD, FAAOS
Dictated: 01/22/2024, Transcribed: 01/23/2024 by Medical Transcriptionist Kelly O'Brien,
k.obrien@sforthopedic.com
"""

TEXT_1500 = """
MULTI-DISCIPLINARY TEAM CONFERENCE — COMPLEX CASE REVIEW
CHILDREN'S HOSPITAL OF PHILADELPHIA (CHOP)
3401 Civic Center Boulevard, Philadelphia, PA 19104
Conference Date: 02/08/2024, 08:00-09:30 AM EST
Conference Room: Colket Translational Research Building, Room 14-200
Recorded by: Clinical Documentation Specialist Amy Richardson, BSN, RN
Phone: (215) 555-0100, a.richardson@chop.edu

PATIENT IDENTIFICATION:
Full Name: Sophia Grace Delacroix-Thompson
Date of Birth: 07/29/2017
Age: 6 years, 6 months
Medical Record Number: CHOP-2019-445521
Social Security Number: 187-42-6693
Home Address: 842 Spruce Street, Apartment 3F, Philadelphia, PA 19107
Primary Language: English, Secondary Language: French

PARENTS/LEGAL GUARDIANS:
Mother: Dr. Isabelle Marie Delacroix, PhD (Biochemistry)
  Employer: University of Pennsylvania, Department of Chemistry
  Work Address: 231 South 34th Street, Philadelphia, PA 19104
  Cell: (215) 555-0234, Work: (215) 555-0235
  Email: i.delacroix@upenn.edu
  SSN: 223-56-7891

Father: Marcus James Thompson, JD
  Employer: Thompson & Blackwell LLP, Partner
  Work Address: 1700 Market Street, Suite 3200, Philadelphia, PA 19103
  Cell: (215) 555-0236, Work: (215) 555-0237
  Email: m.thompson@thompsonblackwell.com
  SSN: 334-67-8902

Emergency Contacts:
1. Grandparent: Claudette Delacroix — (215) 555-0240, 115 Pine Street, Philadelphia, PA 19106
2. Aunt: Victoria Thompson — (610) 555-0300, v.thompson@gmail.com, Bryn Mawr, PA 19010
3. Family Friend/Neighbor: Dr. Helen Zhao — (215) 555-0242, h.zhao@jefferson.edu

Insurance:
Primary: Aetna Student Health (UPenn), Policy#: AET-UPENN-88341, Group: GRP-FAC-100
  Subscriber: Isabelle M. Delacroix, Member ID: IMD-221098
Secondary: CIGNA (Thompson & Blackwell), Policy#: CIG-TB-55692
  Subscriber: Marcus J. Thompson, Member ID: MJT-778432
Authorization Coordinator: Denise Crawford, (800) 555-0280, d.crawford@aetna.com

CONFERENCE ATTENDEES:
1. Dr. Elena Petrov, MD — Pediatric Neurology, Conference Chair
   NPI: 1122334455, License: PA-MD-NEU-33210
   Phone: (215) 555-0110, e.petrov@chop.edu
   Office: Wood Center, 3rd Floor, Suite 310

2. Dr. James Okafor, MD — Pediatric Neurosurgery
   NPI: 2233445566, License: PA-MD-NS-44521
   Phone: (215) 555-0120, j.okafor@chop.edu

3. Dr. Sarah Lindgren, MD — Pediatric Epileptology
   NPI: 3344556677, License: PA-MD-EP-55832
   Phone: (215) 555-0130, s.lindgren@chop.edu

4. Dr. Michelle Santos, PsyD — Pediatric Neuropsychology
   License: PA-PSY-22143, Phone: (215) 555-0140, m.santos@chop.edu

5. Katherine Chen, MS, CGC — Genetic Counselor
   Phone: (215) 555-0150, k.chen@chop.edu

6. Rachel Abramowitz, MSW, LCSW — Social Worker
   License: PA-SW-66721, Phone: (215) 555-0160, r.abramowitz@chop.edu

7. Amanda Liu, RN, BSN — Epilepsy Nurse Navigator
   Phone: (215) 555-0170, a.liu@chop.edu

8. Thomas Brennan, PharmD — Clinical Pharmacist
   Phone: (215) 555-0180, t.brennan@chop.edu

CLINICAL SUMMARY:
Sophia is a 6-year-old girl with drug-resistant focal epilepsy, first presenting at age 3 years
with focal motor seizures affecting the right upper extremity, initially evaluated by Dr. Maria
Gonzalez at St. Christopher's Hospital for Children, Erie Avenue at Front Street, Philadelphia,
PA 19134, Phone: (215) 555-0400, m.gonzalez@stchristophers.com, NPI: 4455667788. Transferred
to CHOP Epilepsy Program on 08/15/2021 under the care of Dr. Petrov.

SEIZURE HISTORY:
Current seizure frequency: 8-12 focal motor seizures per week despite adequate trials of four
anti-seizure medications. Breakthrough status epilepticus on 11/22/2023 requiring PICU admission
(5 days), managed by PICU attending Dr. Robert Kim, (215) 555-0200, r.kim@chop.edu.

MEDICATION HISTORY:
1. Levetiracetam (Keppra): Started 03/2021 by Dr. Gonzalez, max dose 40mg/kg/day — inadequate
   seizure control, behavioral side effects (aggression). Discontinued 09/2021.
2. Oxcarbazepine (Trileptal): Started 09/2021, max dose 45mg/kg/day — partial response,
   hyponatremia (Na 128 mEq/L on 01/15/2022). Discontinued 03/2022.
3. Lacosamide (Vimpat): Started 03/2022, current dose 8mg/kg/day — partial response, continued.
4. Clobazam (Onfi): Started 08/2022, current dose 0.5mg/kg/day — partial response, continued.
Pharmacy: CHOP Outpatient Pharmacy, Contact: Jennifer Walsh, RPh, (215) 555-0190, j.walsh@chop.edu

DIAGNOSTIC WORKUP:
1. Brain MRI (3T) — 09/01/2021, 03/15/2022, 09/20/2023
   Performed at CHOP Radiology, Read by Dr. Patricia Yamamoto, MD, Pediatric Neuroradiology
   NPI: 5566778899, p.yamamoto@chop.edu, (215) 555-0210
   Findings: Left temporal focal cortical dysplasia (FCD), Type IIb suspected

2. Video-EEG Monitoring — 10/05-10/12/2023 (7 days)
   EEG Lab Director: Dr. Lindgren (see above)
   Technologist: Brian Murphy, R.EEG T., b.murphy@chop.edu, (215) 555-0220
   Results: 47 electroclinical seizures captured, all arising from left temporal region (T3/T5),
   consistent with MRI lesion. Interictal: Left temporal sharp waves, intermittent rhythmic
   delta activity.

3. PET Scan — 11/01/2023
   Nuclear Medicine: Dr. Andrew Park, MD, a.park@chop.edu, (215) 555-0230
   Findings: Left temporal hypometabolism concordant with MRI and EEG findings

4. Neuropsychological Evaluation — 12/04-12/05/2023
   Examiner: Dr. Santos (see above)
   Results: FSIQ 95 (Average), significant weakness in verbal memory and processing speed,
   reading at kindergarten level (below grade expectation). Social-emotional: elevated anxiety
   per parent report (CBCL Internalizing T-score: 68).

5. Genetic Testing — 12/15/2023
   Ordered by: Katherine Chen, CGC
   Lab: GeneDx, 207 Perry Parkway, Gaithersburg, MD 20877
   Contact: (301) 555-0500, clientservices@genedx.com
   Test: Epilepsy Panel (500+ genes), Chromosomal Microarray
   Results (received 01/29/2024): Heterozygous pathogenic variant in DEPDC5 (c.865C>T, p.Arg289*)
   Confirmed by Sanger sequencing. Parental testing pending (samples collected 02/01/2024).

SURGICAL CANDIDACY DISCUSSION:
Dr. Okafor reviewed the presurgical workup and confirmed concordance across all modalities
(MRI, EEG, PET, semiology) pointing to the left temporal FCD as the epileptogenic zone.
Recommended: Left temporal lesionectomy with intraoperative electrocorticography.
Surgical risk discussion documented separately (consent form signed by both parents on 02/08/2024).
Surgical coordinator: Patricia Doyle, RN, (215) 555-0250, p.doyle@chop.edu

SOCIAL WORK UPDATE:
Ms. Abramowitz reported that the family has adequate support systems. Sophia attends Greenfield
Elementary School, 1300 Lombard Street, Philadelphia, PA 19147. School contact: Principal
Dr. Howard Blake, (215) 555-0350, h.blake@philasd.org. IEP in place since 09/2022, reviewed
01/2024 with special education coordinator Maria Fontaine, m.fontaine@philasd.org.
Family has applied for SSI disability benefits, application#: SSA-2024-PHI-08821, case worker
Angela Torres, (800) 555-0772, a.torres@ssa.gov. Ronald McDonald House reserved for
post-surgical recovery, confirmation#: RMH-CHOP-2024-1134.

PHARMACY REVIEW:
Mr. Brennan confirmed no drug interactions between current ASMs and anesthetic agents planned for
surgery. Recommended pre-op labs: CBC, CMP, Lacosamide trough level, Clobazam/N-desmethylclobazam
levels. Lab orders sent to CHOP Clinical Lab, Contact: Supervisor Diana Ross, (215) 555-0260,
d.ross@chop.edu.

PLAN:
1. Proceed with left temporal lesionectomy, target date: 03/11/2024
2. Pre-surgical MRI with thin cuts on 02/26/2024
3. Pre-op clinic visit on 03/04/2024 with Dr. Okafor and anesthesia
4. Continue current ASM regimen through surgery
5. Post-op EEG monitoring planned for 72 hours minimum
6. Neuropsychological re-evaluation at 6 months post-surgery
7. Genetic counseling follow-up for parental testing results

Next MDT Conference: 03/07/2024 at 08:00 AM, same location
Minutes distributed to all attendees and filed in patient chart.
Report finalized by: Dr. Elena Petrov, MD, 02/08/2024 11:45 AM EST
"""

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

SINGLE_CASES = [
    ("~400 tokens", TEXT_400),
    ("~700 tokens", TEXT_700),
    ("~1000 tokens", TEXT_1000),
    ("~1300 tokens", TEXT_1300),
    ("~1500 tokens", TEXT_1500),
]


def call_single(text, confidence=0.5, smart_merge=True):
    start = time.perf_counter()
    resp = requests.post(
        f"{BASE_URL}/extract_pii",
        json={"text": text, "confidence_threshold": confidence, "use_smart_merging": smart_merge},
    )
    round_trip_ms = (time.perf_counter() - start) * 1000
    data = resp.json()
    return {
        "status": resp.status_code,
        "entity_count": data["entity_count"],
        "server_ms": data["processing_time_ms"],
        "round_trip_ms": round(round_trip_ms, 2),
        "entities": data["entities"],
    }


def call_batch(texts, confidence=0.5, smart_merge=True):
    start = time.perf_counter()
    resp = requests.post(
        f"{BASE_URL}/batch_extract_pii",
        json={"texts": texts, "confidence_threshold": confidence, "use_smart_merging": smart_merge},
    )
    round_trip_ms = (time.perf_counter() - start) * 1000
    data = resp.json()
    return {
        "status": resp.status_code,
        "total_items": data["total_items"],
        "successful": data["successful_items"],
        "failed": data["failed_items"],
        "server_ms": data["total_processing_time_ms"],
        "round_trip_ms": round(round_trip_ms, 2),
        "items": data["items"],
    }


# ─────────────────────────────────────────────────────────────────────────────
# 0. Warm-up (health check)
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 90)
print("WARM-UP — Health Check")
print("=" * 90)
start = time.perf_counter()
resp = requests.get(f"{BASE_URL}/")
ms = (time.perf_counter() - start) * 1000
print(f"Status: {resp.status_code} | {resp.json()} | Latency: {ms:.1f}ms\n")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Single Text — All Sizes
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 90)
print("SINGLE TEXT PII EXTRACTION — Varying Token Sizes")
print("=" * 90)

single_results = []
for label, text in SINGLE_CASES:
    print(f"\n--- {label} ---")
    r = call_single(text)
    single_results.append((label, r))
    print(f"  Entities: {r['entity_count']}")
    print(f"  Server time:     {r['server_ms']:>10.1f} ms")
    print(f"  Round-trip time: {r['round_trip_ms']:>10.1f} ms")
    for e in r["entities"][:5]:
        print(f"    [{e['label']:20s}] '{e['text']}'")
    if r["entity_count"] > 5:
        print(f"    ... and {r['entity_count'] - 5} more")

print(f"\n{'=' * 90}")
print(f"{'SINGLE EXTRACTION TIMING SUMMARY':^90}")
print(f"{'=' * 90}")
print(f"{'Size':<15} {'Entities':>10} {'Server (ms)':>15} {'Round-trip (ms)':>18}")
print(f"{'-' * 90}")
for label, r in single_results:
    print(f"{label:<15} {r['entity_count']:>10} {r['server_ms']:>15.1f} {r['round_trip_ms']:>18.1f}")
print(f"{'=' * 90}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Batch Processing — Same 5 texts in one call
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{'=' * 90}")
print("BATCH PROCESSING — 5 texts (same as single tests)")
print("=" * 90)

batch_texts = [text for _, text in SINGLE_CASES]
r_combined = call_batch(batch_texts)
print(f"  Total items:      {r_combined['total_items']}")
print(f"  Successful:       {r_combined['successful']}")
print(f"  Failed:           {r_combined['failed']}")
print(f"  Server time:      {r_combined['server_ms']:.1f} ms")
print(f"  Round-trip time:  {r_combined['round_trip_ms']:.1f} ms")

print(f"\n{'=' * 90}")
print(f"{'BATCH EXTRACTION TIMING SUMMARY':^90}")
print(f"{'=' * 90}")
print(f"{'Size':<15} {'Entities':>10} {'Server (ms)':>15} {'Round-trip (ms)':>18}")
print(f"{'-' * 90}")
for idx, (label, _) in enumerate(SINGLE_CASES):
    item = r_combined["items"][idx]
    # No per-item server time from batch, so just show entity count
    print(f"{label:<15} {item['entity_count']:>10}")
print(f"{'-' * 90}")
print(f"{'TOTAL':.<15} {sum(it['entity_count'] for it in r_combined['items']):>10} {r_combined['server_ms']:>15.1f} {r_combined['round_trip_ms']:>18.1f}")
print(f"{'=' * 90}")

print("\nDone!")
