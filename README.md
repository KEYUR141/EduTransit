<div align="center">

# GapMap

### Evidence-grounded support for education transitions

GapMap identifies unresolved learning evidence when a student changes a board, programme, discipline, language, institution, or country—and routes uncertain cases to an instructor instead of forcing an answer.

**Smart India Hackathon 2026 · Problem Statement SIH26207 · Working Prototype**

![React](https://img.shields.io/badge/React-19-151515?logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-6-151515?logo=typescript&logoColor=3178C6)
![Django](https://img.shields.io/badge/Django-5-151515?logo=django&logoColor=44B78B)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-151515?logo=postgresql&logoColor=4169E1)
![Sentence Transformers](https://img.shields.io/badge/Embeddings-Sentence%20Transformers-151515)
![Three.js](https://img.shields.io/badge/Visualisation-Three.js-151515?logo=threedotjs&logoColor=white)
![Tests](https://img.shields.io/badge/tests-15%20passing-d9ff67?labelColor=151515)

</div>

## Team

<table>
  <tr>
    <td align="center" width="33%">
      <img src="documents/team/profile-pending.svg" width="96" height="96" alt="AI engineering contributor profile pending" /><br />
      <strong>Profile pending</strong><br />
      <sub>AI Engineering &amp; System Design</sub><br />
      <sub>RAG architecture, embeddings, guardrails, backend integration and overall system design</sub><br />
      <sub>GitHub link pending</sub>
    </td>
    <td align="center" width="33%">
      <a href="https://github.com/divyalonare"><img src="https://github.com/divyalonare.png?size=160" width="96" height="96" alt="Divya Lonare" /></a><br />
      <strong>Divya Lonare</strong><br />
      <sub>Research &amp; Evidence</sub><br />
      <sub>Real-world problem research, evidence discovery and scenario formulation</sub><br />
      <a href="https://github.com/divyalonare"><sub>@divyalonare</sub></a>
    </td>
    <td align="center" width="33%">
      <a href="https://github.com/dongrehimanshu02-art"><img src="https://github.com/dongrehimanshu02-art.png?size=160" width="96" height="96" alt="Himanshu Dongre" /></a><br />
      <strong>Himanshu Dongre</strong><br />
      <sub>Documentation &amp; Presentation</sub><br />
      <sub>Project documentation, presentation narrative and PPT content development</sub><br />
      <a href="https://github.com/dongrehimanshu02-art"><sub>@dongrehimanshu02-art</sub></a>
    </td>
  </tr>
</table>

## What GapMap solves

Education may be standardised at the certificate level while actual readiness still differs. Topic sequence, terminology, depth, assessment style, interrupted study, cross-domain entry, and international prerequisites can leave a learner with a specific unresolved gap.

A marksheet confirms what was completed. GapMap investigates a different question:

> What destination requirement is still unsupported by verified learner evidence, and what is the smallest responsible next step?

GapMap does not replace APAAR, DIKSHA, UDISE+, admission authorities, teachers, or institutional policy. It works as an explainable support layer between a learner's existing evidence and the intended destination.

## Working prototype

| Capability | What the prototype demonstrates |
|---|---|
| Support cases | Students, parents, or educators can describe an education transition without knowing its category |
| Evidence retrieval | Hybrid retrieval combines pgvector similarity, lexical matching, canonical terms, and exact phrases |
| Dynamic discovery | A new case can be compared across scenarios when no scenario ID is known |
| Confidence and guardrails | Low-confidence, rare, conflicting, and policy-boundary cases are routed to instructor review |
| Gap formulation | The dashboard explains requirement − verified evidence coverage = unresolved evidence gap |
| Evidence report | Every retrieved result includes its source, review state, match signals, and retrieval explanation |
| Embedding explorer | Three.js displays approved evidence as an interactive 3D semantic map |
| Diagnostic pathway | The backend supports prerequisite diagnostics, gap maps, bridge steps, and reassessment |
| Demonstration data | 60+ differentiated synthetic transition scenarios include rare and boundary situations |

## How it works

```mermaid
flowchart LR
    A[Raise support case] --> B[Understand transition context]
    B --> C[Retrieve approved evidence]
    C --> D[Compare requirements and learner evidence]
    D --> E{Evidence sufficient?}
    E -->|Yes| F[Explain unresolved gaps]
    E -->|No or uncertain| G[Instructor review]
    F --> H[Order the next support steps]
    G --> H
    H --> I[Reassess readiness]
```

### Gap formulation

For the presentation layer, the unresolved evidence gap is shown as:

```text
Unresolved evidence gap = Destination evidence requirement − Verified evidence coverage
```

| Unresolved portion | Prototype label |
|---:|---|
| 0–15% | Evidence satisfied |
| 16–40% | Partial evidence gap |
| 41–100% | Significant evidence gap |
| Insufficient or conflicting evidence | Instructor review |

This is an evidence-completeness signal—not a student mark, intelligence score, disability inference, admission probability, or final equivalence decision. Embedding similarity is used for retrieval and is never treated as proof of competency.

## RAG and evidence engineering

1. Validated scenarios are divided into traceable evidence chunks.
2. `paraphrase-multilingual-MiniLM-L12-v2` generates normalized 384-dimensional embeddings.
3. PostgreSQL stores embeddings through pgvector and an HNSW cosine index.
4. Retrieval combines semantic, lexical, phrase, and canonical-term signals.
5. Checksums, source status, scenario scope, and approval flags protect retrieval integrity.
6. The confidence layer reports evidence quality and selects the appropriate human-review route.

The pipeline retrieves and explains evidence. It does not autonomously approve credits, eligibility, admission, or curriculum equivalence.

## 3D embedding map

The navbar's **Embedding map** opens a Three.js explorer of approved evidence chunks.

- PCA computed through NumPy SVD projects 384 dimensions into three display coordinates.
- Nearby points represent approximately similar semantic content.
- Colours distinguish evidence categories.
- Lines connect chunks belonging to the same transition scenario.
- Selecting a point reveals its scenario and review status.
- Raw vectors and full evidence text remain on the backend.

The 3D projection is explanatory. Actual retrieval continues to compare the complete 384-dimensional vectors.

## Architecture

```mermaid
flowchart TB
    UI[React + TypeScript portal] -->|JSON / Fetch API| API[Django REST API]
    UI --> MAP[Three.js embedding explorer]
    API --> CASES[Support case and diagnostic services]
    API --> RAG[Hybrid RAG pipeline]
    API --> GUARD[Confidence and guardrails]
    RAG --> MODEL[Sentence Transformer]
    RAG --> DB[(PostgreSQL + pgvector)]
    MAP -->|Safe 3D coordinates| API
    GUARD --> REVIEW[Instructor review queue]
```

## Technology used

- **Frontend:** React 19, TypeScript, Vite, CSS/Tailwind foundation, Lucide React and Three.js
- **Backend:** Python, Django and Django REST Framework
- **Data:** PostgreSQL, Psycopg and pgvector
- **AI retrieval:** Sentence Transformers with hybrid explainable ranking
- **Projection:** NumPy PCA/SVD
- **API documentation:** drf-spectacular and OpenAPI/Swagger
- **Testing:** Django tests, Vitest, Testing Library, TypeScript and Oxlint

See [tech.md](tech.md) for the technical design and [AI_Engineer_plan.md](AI_Engineer_plan.md) for the AI-engineering strategy.

## Run locally

### Prerequisites

- Python 3.13
- Node.js 20 or newer
- PostgreSQL with permission to enable the `vector` extension

### 1. Backend environment

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item backend\Gap\.env.example backend\Gap\.env
```

Update `backend/Gap/.env` with your local database values:

```env
DATABASE_URL=postgresql://username:password@127.0.0.1:5432/database
RAG_EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
RAG_EMBEDDING_DEVICE=cpu
RAG_EMBEDDING_LOCAL_ONLY=False
RAG_ALLOW_EMBEDDING_FALLBACK=True
```

Use `RAG_EMBEDDING_LOCAL_ONLY=False` once to download the model. After it is cached, change it to `True` for an offline demonstration.

### 2. Prepare Django and the data

```powershell
cd backend\Gap
python manage.py migrate
python manage.py seed_gapmap_demo
python seed_data.py
python manage.py rebuild_rag_embeddings --batch-size 32
python manage.py verify_rag
python manage.py runserver
```

The migration enables the PostgreSQL `vector` extension when necessary.

### 3. Start the frontend

In a second terminal:

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Open [http://127.0.0.1:5173](http://127.0.0.1:5173). API documentation is available at [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/).

## Demonstration path

1. Open the learner workspace and select or raise a transition case.
2. Generate the evidence report and show its citations and match reasons.
3. Explain the evidence-confidence signal and instructor-review route.
4. Walk through the transparent gap formulation.
5. Open **Embedding map**, rotate the evidence space, and inspect a scenario cluster.

## Main API routes

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/api/health/` | Frontend connectivity check |
| `GET/POST` | `/api/support-cases/` | List or create support cases |
| `POST` | `/api/support-cases/{id}/analyse/` | Retrieve evidence and persist confidence/review results |
| `POST` | `/api/rag/retrieve/` | Scenario-scoped or dynamic hybrid retrieval |
| `GET` | `/api/rag/embedding-map/` | Safe 3D coordinates and presentation labels |
| `GET` | `/api/demo-context/` | Discover seeded demonstration IDs |
| `GET/POST` | `/api/diagnostic-sessions/` | Run the adaptive diagnostic workflow |

## Verification

```powershell
# Backend
python backend\Gap\manage.py check
python backend\Gap\manage.py test map
python backend\Gap\manage.py spectacular --file schema.yml --validate

# Frontend
cd frontend
npm run typecheck
npm run lint
npm test -- --run
npm run build
```

Current readiness check: **12 backend tests and 3 frontend tests passing**. PostgreSQL must be running before `verify_rag` and the live pgvector demonstration.

## Safety and prototype boundaries

- All included learner identities and evidence records are synthetic.
- Do not enter Aadhaar, APAAR IDs, official marksheets, or sensitive personal information.
- Only approved evidence participates in published retrieval results.
- Low-confidence and policy-boundary cases are escalated instead of force-matched.
- Human review remains mandatory for consequential academic decisions.
- Authentication and role-based permissions must be added before deployment with real learners.

## Project documents

- [Unique selling proposition](USP.md)
- [Product plan](plan.md)
- [Technical architecture](tech.md)
- [AI engineering plan](AI_Engineer_plan.md)
- [Domain and standardisation strategy](GapMap-Domain-and-Standardisation-Strategy.md)
- [Sample transition scenarios](GapMap-Sample-Data-Scenarios.md)
- [Backend and RAG guide](backend/README.md)
---

GapMap is a hackathon prototype designed to make education-transition uncertainty visible, explainable, and reviewable.