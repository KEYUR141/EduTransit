# GapMap Product and Delivery Plan

## 1. Objective

Build a software prototype that diagnoses curriculum-transition gaps and generates a minimum teacher-reviewed learning bridge. The project will prove the complete loop from curriculum comparison to classroom-readiness reassessment.

## 2. Target Transition

The initial prototype will focus on one bounded transition:

- subject: mathematics;
- stage: Class 8 prerequisites required for selected Class 9 topics;
- curriculum comparison: CBSE/NCERT and one selected state-board curriculum;
- languages: English and Hindi;
- graph size: approximately 25 concepts;
- users: transitioning student and mathematics teacher.

The team should confirm the exact state board and target mathematics unit with a teacher before entering curriculum data.

## 3. Product Boundary

GapMap owns four tasks:

1. compare source and destination learning outcomes;
2. identify root prerequisite and possible terminology gaps;
3. create an ordered minimum bridge path;
4. collect teacher review and readiness evidence.

GapMap does not:

- issue or replace a student identity;
- store official credentials or academic credits;
- transfer admission records;
- provide a generic content library;
- replace school examinations;
- predict dropout;
- diagnose learning disabilities;
- make promotion or retention decisions.

## 4. Existing-System Comparison

| System | Published purpose | GapMap boundary |
|---|---|---|
| APAAR and ABC | Academic identity, records, achievements and credit mobility | GapMap assesses readiness for a destination topic; it stores no official credits or credentials |
| UDISE+ | Education-management data for schools, teachers and students | GapMap uses only prototype learner and curriculum data |
| PRABANDH OoSC module | Tracks out-of-school children and mainstreaming progress | GapMap begins after entry or re-entry and addresses curriculum readiness |
| DIKSHA | Curriculum content, courses, quizzes, translations and digital learning resources | GapMap may link to reviewed resources after diagnosing the prerequisite path |
| School ERP or Shala Darpan | Attendance, report cards and administration | GapMap explains a learning gap through curriculum dependencies |
| PRASHAST | School screening and referral related to disability conditions | GapMap performs academic prerequisite diagnosis and makes no disability inference |

### Judge-ready distinction

> **Existing systems can carry the student, record the student or provide content. GapMap determines the smallest learning bridge the student needs to understand the destination curriculum.**

## 5. User Journey

### Teacher setup

1. Select source board, destination board, grade, subject and languages.
2. Select the destination unit currently taught in class.
3. Review the mapped learning outcomes and prerequisite graph.
4. Assign the transition diagnostic.

### Student diagnostic

1. Answer one destination-level question.
2. If the answer is incorrect, receive a prerequisite question.
3. Continue only along branches where mastery remains uncertain.
4. Complete equivalent or language-adjusted items when terminology may affect the result.
5. Receive a short reviewed bridge plan rather than a final label.

### Recovery and reassessment

1. Work through ordered prerequisite activities.
2. Record evidence for each concept.
3. Retake a different item for the original destination outcome.
4. Return unresolved branches to the teacher.

## 6. Delivery Stages

### Stage 1: Curriculum and teacher validation

- choose the state board and mathematics unit;
- collect official learning outcomes and authorised curriculum references;
- define approximately 25 concepts;
- ask a mathematics teacher to review prerequisite links;
- prepare two learner scenarios.

**Exit:** The team has a reviewed concept graph on paper or in JSON.

### Stage 2: Working vertical slice

- scaffold the backend, frontend and database;
- import curriculum, concept and prerequisite data;
- create one student and teacher workflow;
- implement a deterministic diagnostic traversal;
- display a basic gap map and bridge sequence.

**Exit:** One learner can complete diagnosis and receive a reviewed bridge path.

### Stage 3: Language-aware diagnostic

- add English and Hindi versions of selected items;
- tag items by concept, representation and language demand;
- compare performance across equivalent items;
- report terminology difficulty as evidence, not a diagnosis.

**Exit:** The demo can distinguish the prepared concept-gap and terminology-gap scenarios.

### Stage 4: Teacher workflow and reassessment

- add curriculum-map approval;
- allow teachers to edit the bridge path;
- record activity completion and evidence;
- reassess the destination outcome;
- show cohort-level recurring gaps.

**Exit:** The prototype demonstrates the complete recovery loop.

### Stage 5: AI assistance and presentation polish

- suggest candidate curriculum equivalences for teacher approval;
- generate question variants from reviewed templates;
- retrieve approved explanations and resources;
- produce a concise teacher summary with evidence links;
- finish responsive and accessible UI states.

**Exit:** AI reduces preparation work while teachers retain control.

### Stage 6: Evaluation and pitch

- test known gap scenarios;
- compare adaptive question count with a fixed diagnostic;
- collect teacher agreement on inferred gaps and bridge order;
- test permissions and data minimisation;
- rehearse a three-to-five-minute demonstration;
- align every pitch claim with a visible prototype action.

**Exit:** The team can demonstrate one success path and one correction path.

## 7. Team Workstreams

| Workstream | Responsibilities |
|---|---|
| Curriculum research | Official sources, outcome mapping, teacher review and question-bank provenance |
| Backend and graph | Data model, APIs, diagnostic traversal, mastery updates and bridge ordering |
| Frontend | Student diagnostic, concept map, bridge path, teacher review and reassessment screens |
| AI and language | Candidate mapping, bilingual evidence, grounded explanations and evaluation |
| QA and pitch | Test scenarios, accessibility, deployment, slide alignment and demo rehearsal |

## 8. Demonstration Script

1. A teacher selects a Class 8 state-board background and a Class 9 CBSE algebra topic.
2. GapMap displays the mapped prerequisites and highlights curriculum differences.
3. The student answers the current algebra item incorrectly.
4. Adaptive traversal tests ratios, integers and negative-number operations.
5. A bilingual pair shows that ratio understanding exists while English terminology remains unfamiliar.
6. GapMap identifies negative-number operations as the earliest concept gap.
7. The teacher reviews a short ordered bridge and assigns it.
8. The student completes the bridge and answers a new algebra item.
9. The dashboard records improved readiness and keeps uncertain branches open.

## 9. Evaluation Plan

### Diagnostic validity

- percentage of prepared scenarios where GapMap finds the intended root gap;
- mathematics-teacher agreement with the identified gap;
- false-gap rate on concepts the learner already knows.

### Efficiency

- questions asked by the adaptive diagnostic versus a fixed test;
- concepts assigned in the bridge versus the full remedial unit;
- time from assessment start to teacher-reviewed plan.

### Learning evidence

- mastery change on bridge concepts;
- performance change on the destination outcome;
- number of reassessment cycles before the case reaches ready or needs teacher action.

## 10. Risks and Controls

| Risk | Control |
|---|---|
| Incorrect curriculum equivalence | Teacher approves every mapping used in the prototype |
| Hallucinated questions or explanations | Use reviewed templates and retrieve only from approved sources |
| Language gap misclassified as a concept gap | Use equivalent bilingual and low-language-demand items; present uncertainty |
| Student receives a permanent negative label | Store concept evidence and confidence, not intelligence or ability labels |
| Diagnostic becomes too long | Traverse prerequisites adaptively and stop when evidence is sufficient |
| Copyright or licence misuse | Store metadata and links unless the source licence permits local use |
| Prototype claims unsupported impact | Label personas and results as synthetic and define a future pilot |

## 11. Immediate Actions

1. Select the state board and one Class 9 mathematics unit.
2. Recruit one mathematics teacher or faculty reviewer.
3. Draft the 25-node concept dependency graph.
4. Prepare two questions per concept and record their source or reviewer.
5. Create two bilingual terminology-check pairs.
6. Scaffold the database and diagnostic API.
7. Build the student diagnostic before adding an LLM.

## 12. Official References

- Ministry of Education, ABSS 2025 Outcome Document: https://www.education.gov.in/sites/upload_files/mhrd/files/nep/ABSS_2025_Outcome_Document.pdf
- NCERT Learning Outcomes and curriculum resources: https://www.ncert.nic.in/
- DIKSHA official overview: https://diksha.gov.in/about-us/
- APAAR official portal: https://apaar.education.gov.in/
- UDISE+ official portal: https://www.udiseplus.gov.in/
- Samagra Shiksha: https://samagra.education.gov.in/about.html
- PRASHAST: https://prashast.education.gov.in/

References and platform scopes checked on 10 September 2026. Recheck them before final submission.
