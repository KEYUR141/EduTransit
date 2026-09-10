# EduSure Product and Delivery Plan

## 1. Product Statement

EduSure is a student-support orchestration platform for preventing avoidable interruption of education. It turns a reported financial or practical difficulty into an owned, trackable Education Continuity Case and follows it until support is delivered and the student's participation becomes stable.

**Positioning:** Scholarship portals process applications. EduSure manages educational continuity.

## 2. Problem Boundary

EduSure addresses the gap between a student experiencing a barrier and that barrier being resolved. It focuses on:

- early reporting of education-continuity risk;
- assessment of overlapping barriers;
- discovery of verified relevant support;
- application and documentation guidance;
- assignment of responsibility;
- intervention and deadline tracking;
- confirmation of the real educational outcome.

EduSure does not issue identity, store official academic credentials, award academic credit or approve government benefits.

## 3. APAAR and EduSure: Are They the Same?

No. They operate at different layers of the education ecosystem.

Official APAAR material describes APAAR as a permanent 12-digit student ID and lifelong academic passport. It consolidates academic records and achievements, works with DigiLocker and the Academic Bank of Credits, and supports academic mobility and credential verification.

EduSure does not reproduce those functions. It manages the operational response to a student's risk of leaving or interrupting education.

| Question | APAAR | EduSure |
|---|---|---|
| Primary purpose | Lifelong student identity and academic record/credit continuity | Intervention and support continuity when education is at risk |
| Central object | Permanent student ID and verified academic credentials | Time-bound Education Continuity Case |
| Typical information | Marksheets, certificates, credits, achievements and academic history | Current barriers, support matches, tasks, case owner, intervention status and outcome |
| Main users | Students, institutions, credential/credit ecosystem and authorised verifiers | Students, families, teachers, counsellors, institutions and support providers |
| Main workflow | Identify student, store/retrieve credentials, recognise and transfer credits | Report concern, assess barriers, match support, assign action, track delivery, verify stability |
| Success measure | Trusted, portable academic identity and records | Student receives suitable support and remains active in education |
| Decision role | Academic identity and credential infrastructure | Human-supervised case coordination; no official benefit approval |
| Relationship | Potential digital public infrastructure | Complementary application that may use authorised inputs in a future deployment |

### Simple explanation for judges

> **APAAR tells the education system who the learner is and carries the learner's academic record. EduSure determines what support action is needed when that learner is at risk and tracks whether the action worked.**

### Example

APAAR may show that a learner is enrolled and preserve academic achievements during an institutional transition. If that learner starts missing classes because transport is unaffordable and an income document is incomplete, EduSure opens a continuity case, finds relevant assistance, assigns follow-up tasks and verifies whether attendance stabilises.

### Integration position

For the hackathon, EduSure should use synthetic internal student IDs and should not claim live APAAR integration.

In a future authorised deployment, APAAR could be an optional consent-based identity or academic-context input. Such integration would require official APIs, permissions, purpose limitation, data minimisation and compliance review. EduSure must still work for a student without APAAR so that lack of an ID does not become another exclusion barrier.

## 4. Differentiation from Adjacent Solutions

| Existing solution | What it does well | Gap addressed by EduSure |
|---|---|---|
| Scholarship portal | Publishes schemes and accepts applications | Begins from the student's barriers and follows support through delivery and outcome |
| Search engine/chatbot | Answers questions and finds information | Creates responsibility, tasks, deadlines, escalation and an auditable case |
| School ERP/attendance system | Records attendance and administration | Connects a warning to external/internal support and tracks intervention effectiveness |
| NGO case register | Tracks cases within one organisation | Provides a shared, explainable support-matching and continuity workflow across providers |
| APAAR/DigiLocker/ABC | Identity, credentials, documents and academic credits | Coordinates present-tense action when a practical barrier threatens participation |

## 5. Target Users

### Primary beneficiaries

- students from low-income or unstable-income households;
- migrant and mobile families;
- first-generation learners;
- children of daily-wage and informal-sector workers;
- students affected by a sudden family financial shock;
- rural or remote students facing transport and connectivity barriers;
- students whose support is delayed by missing or inconsistent documentation.

### Operational users

- teachers who identify early warning signs;
- school/college counsellors and welfare officers;
- institution administrators;
- verified NGO or support-programme coordinators;
- authorised government users in a future deployment.

## 6. Core Product Principles

1. **No wrong door:** A student reports the problem once; the system organises the next steps.
2. **Barrier before scheme:** Start with the student's situation, not with a programme catalogue.
3. **One owned case:** Every unresolved case has a visible owner and next action.
4. **Verified, explainable help:** Recommendations show their source and match reasoning.
5. **Human responsibility:** AI supports people but does not approve, reject or close serious cases.
6. **Outcome over activity:** Form submission is not success; continuity is the outcome.
7. **Inclusive by design:** The workflow must support assisted, multilingual and low-bandwidth access.
8. **Minimal data:** Do not collect identity or documents that the workflow does not need.

## 7. Product Workflow

1. Student, parent, teacher or institution raises a concern.
2. A guided assessment records the student's barriers and urgency.
3. The system creates an Education Continuity Case.
4. Rule-based matching ranks verified support opportunities.
5. The student receives explanations and a required-action checklist.
6. A counsellor is assigned when follow-up or human judgement is needed.
7. Tasks, documents, applications and interventions are tracked.
8. The case owner records whether assistance was actually received.
9. Attendance/participation stability is confirmed.
10. An unresolved case is reassessed, escalated or matched to another intervention.

## 8. Prototype Scope and Scenarios

### Scenario A: Successful intervention

A teacher reports fee and transport difficulties. EduSure finds verified support, identifies missing documents, assigns a counsellor, tracks delivery and closes the case after attendance improves.

### Scenario B: Failed first intervention

A recommended benefit remains pending past its expected date. EduSure flags the overdue task, reopens assessment and routes the student toward an alternative institutional or local support option.

### Scenario C: Assisted access

A parent cannot comfortably navigate an English-only portal. A counsellor uses the guided multilingual workflow with consent and gives the family a simple action checklist.

## 9. Delivery Phases

### Phase 1 — Foundation

- confirm roles, statuses and case lifecycle;
- create the Django/React project structure;
- model students, barriers, programmes, cases, tasks and outcomes;
- prepare synthetic personas and 10–15 verified sample programmes.

**Exit:** One case can be created and viewed end to end.

### Phase 2 — Matching and case ownership

- implement deterministic eligibility filters;
- provide explainable match reasons;
- create counsellor queue and assignment;
- add task, deadline and audit tracking.

**Exit:** A case produces defensible recommendations and has a responsible owner.

### Phase 3 — Outcome loop

- record intervention delivery;
- add outcome verification and follow-up date;
- reopen or escalate unresolved cases;
- display the complete case timeline.

**Exit:** The prototype proves the closed loop that differentiates EduSure.

### Phase 4 — AI assistance and polish

- extract barrier fields from free text;
- generate source-grounded simple-language explanations;
- add a selected multilingual interface;
- polish responsive student and counsellor journeys.

**Exit:** AI improves accessibility without controlling eligibility or case outcomes.

### Phase 5 — Evaluation and pitch

- run prepared scenario tests;
- test access control and audit events;
- measure matching quality and workflow completion;
- rehearse a 3–5 minute demonstration;
- align the presentation with working screens.

**Exit:** Every major pitch claim is visible in the prototype.

## 10. Team Workstreams

| Workstream | Responsibilities |
|---|---|
| Product/research | User journeys, verified programme dataset, policy and presentation evidence |
| Backend | Data model, APIs, permissions, matching, workflow and audit log |
| Frontend | Student journey, counsellor dashboard, case timeline and accessibility |
| AI/data | Structured extraction, grounded retrieval, evaluation scenarios and guardrails |
| QA/presentation | Test cases, demo data, usability review, deployment and pitch rehearsal |

## 11. Hackathon Metrics

- time from concern submission to recommendation;
- percentage of recommendations with complete source and reasoning;
- percentage of open cases with an owner and next action;
- number of overdue tasks surfaced;
- case resolution/follow-up status;
- attendance or participation change in the synthetic scenario;
- successful completion of student and counsellor usability tasks.

Do not present invented prototype metrics as real social impact. Label simulated results clearly and explain how a pilot would validate them.

## 12. Risks and Controls

| Risk | Control |
|---|---|
| AI invents a scheme or condition | Retrieve only from curated sources; show source and last-reviewed date |
| Incorrect eligibility impression | Use deterministic rules and label results as potential matches pending authority verification |
| Sensitive student data exposure | Synthetic demo data, role permissions, minimal collection and audit logs |
| Stigma from a dropout-risk label | Use supportive barrier language and human review; avoid permanent risk labels |
| No official integration access | Demonstrate adapters with mock data and clearly disclose the boundary |
| Team overbuilds AI | Complete the rule-based closed loop before adding LLM features |
| Prototype looks like a portal | Centre the case owner, timeline, overdue actions and verified outcome in the demo |

## 13. Immediate Next Actions

1. Agree on the five case statuses: `NEW`, `ASSESSED`, `ACTION_IN_PROGRESS`, `FOLLOW_UP`, `STABLE/CLOSED`.
2. Finalise one primary synthetic persona and one failure-loop persona.
3. Define the minimum fields for barriers and support programmes.
4. Collect 10–15 official sample programme records with URLs and review dates.
5. Scaffold Django REST Framework, PostgreSQL and React/Vite.
6. Build the first vertical slice before adding AI.

## 14. Official APAAR References

- APAAR About: https://apaar.education.gov.in/about
- APAAR official portal and FAQ: https://apaar.education.gov.in/
- APAAR Terms of Use: https://apaar.education.gov.in/termsofuse
- Ministry of Education APAAR page: https://www.education.gov.in/apaar

Verified on 10 September 2026. The comparison should be rechecked before final submission because public-platform scope and policies can change.
