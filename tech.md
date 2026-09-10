# EduSure Technical Plan

## 1. Product Goal

Build a software prototype that converts a student's risk of educational interruption into a trackable **Education Continuity Case**. The prototype must demonstrate the complete journey from reporting a barrier to confirming that support was delivered and education became stable.

EduSure is not a scholarship directory, an academic-record repository or an AI chatbot. It is a case-management and support-orchestration platform.

## 2. Hackathon Demonstration Scope

The prototype should prove one closed-loop workflow:

```text
Student/teacher reports concern
        ↓
Barrier assessment and risk triage
        ↓
Verified support recommendations
        ↓
Application checklist and case-owner assignment
        ↓
Status, deadline and intervention tracking
        ↓
Continuity outcome confirmed
        ↘ unresolved → reassessment and follow-up
```

### Must-have features

1. Student sign-in and a simple assisted concern form.
2. Barrier assessment covering fees, transport, device, documents, migration and family-income disruption.
3. Explainable support matching from a small verified dataset.
4. A ranked recommendation page showing eligibility reason, required documents, deadline and official source.
5. A continuity case with tasks, status history and an assigned counsellor.
6. Counsellor dashboard for prioritisation and follow-up.
7. Outcome recording: support received, attendance stable, unresolved or escalated.
8. Audit trail showing who performed each important action.

### Good additions after the core works

- multilingual form and simplified explanations;
- OCR-assisted document checklist;
- deadline reminders;
- consent-based parent/guardian access;
- anonymised institution-level barrier analytics;
- low-bandwidth progressive web application support.

### Do not build for the first prototype

- a new national student ID;
- live APAAR, Aadhaar, DigiLocker or government-portal integration;
- automated scholarship submission without official APIs and authorisation;
- a large web-scraping pipeline;
- AI-based final eligibility, dropout or fraud decisions;
- complex predictive ML requiring unavailable historical student data.

## 3. Recommended Stack

| Layer | Technology | Reason |
|---|---|---|
| Web client | React + Vite + TypeScript | Fast to build, presentation-friendly and suitable for student/counsellor dashboards. |
| Styling | Tailwind CSS | Rapid, consistent responsive UI. |
| Backend API | Django + Django REST Framework | Strong authentication, admin panel, ORM and rapid case-management development. |
| Database | PostgreSQL | Reliable relational model for cases, eligibility rules, tasks and audit history. |
| Authentication | Django session/JWT with role-based access | Supports student, counsellor and administrator roles. |
| Background jobs | Celery + Redis, only if required | Suitable for reminders and document processing; omit during the first vertical slice if time is short. |
| File storage | Local development storage; S3-compatible storage later | Keeps the prototype simple while preserving a production path. |
| AI service | Backend adapter for an approved LLM | Allows the provider or local model to change without rewriting business logic. |
| Semantic retrieval | PostgreSQL + pgvector, optional | Retrieves relevant verified scheme passages when keyword/rule matching is insufficient. |
| OCR | Tesseract or PaddleOCR, optional | Extracts fields for user confirmation; never treats OCR output as verified evidence automatically. |
| API documentation | OpenAPI/Swagger through DRF tooling | Makes the architecture easy to demonstrate and test. |
| Testing | Pytest, Django tests and Vitest | Covers eligibility rules, permissions and critical UI logic. |
| Deployment | Docker Compose; Render/Railway/Azure/AWS for demo hosting | Reproducible setup and straightforward demonstration deployment. |

## 4. Why Django Is a Strong Fit

EduSure's core is structured workflow rather than model training. Django gives the team authentication, permissions, relational data, validation and an administrator interface quickly. The Django admin can also serve as an internal data-entry tool for verified schemes during the hackathon, reducing the amount of custom interface work.

## 5. System Architecture

```text
React PWA
   │ HTTPS/JSON
   ▼
Django REST API
   ├── Identity and role service
   ├── Continuity case service
   ├── Eligibility and support-matching engine
   ├── Task, escalation and notification service
   ├── Outcome and audit service
   └── AI assistance adapter
          ├── structured concern extraction
          ├── plain-language explanation
          └── retrieval from verified programme content
   │
   ├── PostgreSQL / optional pgvector
   └── File storage
```

The matching engine remains rule-first and deterministic. AI may interpret a student's free-text concern and explain results, but database rules decide whether an opportunity is potentially applicable.

## 6. Core Data Model

| Entity | Important fields |
|---|---|
| User | role, language, contact preference, active status |
| StudentProfile | education level, institution, location, household context, consent flags |
| ContinuityCase | student, reporter, status, priority, assigned counsellor, opened/closed dates |
| Barrier | case, category, severity, description, evidence status |
| SupportProgramme | provider, coverage, eligibility rules, deadline, required documents, verified source, last reviewed |
| Recommendation | case, programme, match reasons, missing conditions, confidence/provenance |
| CaseTask | owner, action, due date, status, completion evidence |
| Application | programme, stage, submission date, reference, last update |
| Intervention | type, provider, promised/received dates, amount or service details |
| ContinuityOutcome | attendance status, support received, resolution state, follow-up date |
| AuditEvent | actor, action, entity, timestamp, before/after metadata |

Avoid collecting Aadhaar, APAAR or unnecessary identity documents in the prototype. Use synthetic student profiles and document placeholders.

## 7. Support-Matching Logic

Use a hybrid approach:

1. **Hard filters:** geography, education level, age, income ceiling, category and application window.
2. **Rule score:** count satisfied and missing conditions using explicit programme rules.
3. **Barrier relevance:** prioritise support that addresses the student's recorded barriers.
4. **Semantic retrieval:** optionally retrieve relevant passages from verified programme descriptions.
5. **Explainability:** show matched conditions, missing information, official source and last verification date.
6. **Human review:** mark every result as a recommendation, not an approval guarantee.

Do not let an LLM invent schemes, deadlines or eligibility conditions.

## 8. Responsible AI Design

### Appropriate AI tasks

- convert free-text or speech into structured barrier categories;
- translate and simplify verified programme information;
- retrieve relevant support content with citations;
- prepare a counsellor case summary;
- suggest a next-action checklist;
- detect missing fields and approaching deadlines.

### Tasks requiring rules or humans

- final eligibility confirmation;
- case priority when consequences are serious;
- approval or rejection of assistance;
- verification of documents;
- closure of a continuity case;
- sharing sensitive student information.

Every AI response should retain source provenance and allow correction.

## 9. User Interfaces

### Student view

- calm landing page with **Get Support** as the main action;
- conversational multi-step concern form;
- case timeline with the next required action;
- matched-support cards with clear reasons;
- document and deadline checklist;
- visible counsellor/escalation status.

### Counsellor view

- queue ordered by urgency and overdue action;
- filters for barrier type, institution, status and assignee;
- complete case history and student contact preference;
- assign, escalate, request document and record intervention actions;
- outcome form and next follow-up date.

### Administrator view

- verify and update support programmes;
- manage eligibility rules and source dates;
- manage roles and institutions;
- view anonymised service-performance metrics.

## 10. Security and Privacy

- collect only data required for the demonstrated workflow;
- use synthetic data during the hackathon;
- require explicit consent before sharing case information;
- implement role-based permissions and institution-level isolation;
- encrypt transport using HTTPS and protect stored secrets;
- maintain audit records for sensitive actions;
- separate identity data from analytics where practical;
- never expose student cases in public dashboards;
- define retention and deletion rules before real deployment.

## 11. Prototype API Surface

```text
POST   /api/cases/
GET    /api/cases/{id}/
POST   /api/cases/{id}/barriers/
POST   /api/cases/{id}/assess/
GET    /api/cases/{id}/recommendations/
POST   /api/cases/{id}/assign/
POST   /api/cases/{id}/tasks/
PATCH  /api/tasks/{id}/
POST   /api/cases/{id}/interventions/
POST   /api/cases/{id}/outcome/
GET    /api/counsellor/queue/
GET    /api/dashboard/impact/
```

## 12. Suggested Repository Structure

```text
edusure/
├── backend/
│   ├── config/
│   ├── accounts/
│   ├── students/
│   ├── cases/
│   ├── programmes/
│   ├── matching/
│   ├── interventions/
│   └── audit/
├── frontend/
│   └── src/
│       ├── pages/
│       ├── components/
│       ├── features/
│       └── services/
├── data/
│   ├── demo/
│   └── programme-sources/
├── documents/
│   └── presentation/
├── tests/
├── docker-compose.yml
├── README.md
├── USP.md
├── plan.md
└── tech.md
```

## 13. Build Order

### Milestone 1 — Vertical slice

- create database models;
- seed 10–15 verified sample support programmes;
- submit one student concern;
- generate rule-based recommendations;
- assign a case owner;
- record one intervention and outcome.

### Milestone 2 — Presentable workflow

- student case timeline;
- counsellor queue and task management;
- explainable match cards;
- status transitions and audit events;
- responsive visual polish.

### Milestone 3 — AI and accessibility

- structured extraction from free text;
- source-grounded plain-language explanations;
- multilingual interface for selected languages;
- optional document checklist/OCR demonstration.

### Milestone 4 — Evidence and pitch

- measure matching precision on prepared scenarios;
- test permissions and status workflow;
- prepare synthetic impact dashboard;
- rehearse the complete case story and failure recovery.

## 14. Demo Story

Use one realistic synthetic student rather than many disconnected features:

> A first-generation Class 11 student from a daily-wage household is missing classes because transport costs increased and an income certificate is incomplete. A teacher raises a concern. EduSure identifies both barriers, matches verified financial and transport support, creates a documentation task, assigns a counsellor, tracks the intervention and confirms that attendance stabilised. A second scenario shows the feedback loop when support is not delivered.

## 15. Definition of Prototype Success

The prototype is successful when judges can see that:

- the platform understands more than one barrier;
- recommendations are traceable to verified sources;
- a person owns the next action;
- the system follows the case beyond form submission;
- an unresolved case cannot silently disappear;
- educational continuity is recorded as the final outcome.
