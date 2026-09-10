# GapMap Technical Architecture

## 1. Technical Objective

Build an explainable curriculum-transition diagnostic that:

1. represents learning outcomes as a prerequisite graph;
2. maps concepts between source and destination curricula;
3. selects diagnostic questions adaptively;
4. estimates concept mastery and uncertainty;
5. distinguishes likely terminology difficulty from concept difficulty;
6. returns the minimum ordered bridge path;
7. records teacher review and reassessment evidence.

The first release should prioritise a deterministic and inspectable graph workflow. Add a language model only where it reduces content-preparation or explanation work.

## 2. Prototype Architecture

```text
React web client
   │
   ├── Student diagnostic and bridge view
   └── Teacher curriculum map and review dashboard
   │ HTTPS/JSON
   ▼
Django REST API
   ├── Identity and permissions
   ├── Curriculum catalogue
   ├── Concept graph service
   ├── Adaptive diagnostic engine
   ├── Mastery evidence service
   ├── Bridge-path generator
   ├── Reassessment service
   └── AI assistance adapter
          ├── candidate concept mapping
          ├── bilingual terminology support
          └── grounded explanation retrieval
   │
   ├── PostgreSQL with optional pgvector
   └── Reviewed curriculum/question content
```

## 3. Recommended Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React + Vite + TypeScript | Student diagnostic and teacher review interfaces |
| Styling | Tailwind CSS | Fast responsive implementation with consistent states |
| Backend | Django + Django REST Framework | Authentication, validation, API development and administration |
| Database | PostgreSQL | Curricula, concepts, edges, questions, attempts and review history |
| Semantic retrieval | pgvector, optional for the first slice | Candidate curriculum matches and approved content retrieval |
| Graph logic | NetworkX in the prototype | Traversal, ancestor discovery and topological bridge ordering |
| Background tasks | Celery + Redis only if required | Offline curriculum parsing and long AI requests |
| AI integration | Provider-neutral backend adapter | Prevents business logic from depending on one model vendor |
| Testing | Pytest, Django tests and Vitest | Graph, diagnostic, permission and interface testing |
| API documentation | OpenAPI/Swagger | Demonstration and team integration |
| Packaging | Docker Compose | Reproducible local and hosted setup |
| Deployment | Render, Railway, Azure or AWS | Select one based on team access; do not design around a provider |

## 4. Why This Stack

Django fits the structured workflow, reviewer permissions and audit requirements. PostgreSQL keeps the prototype simple while pgvector provides an optional semantic layer. NetworkX allows the team to implement and inspect graph algorithms without deploying a separate graph database.

Neo4j is unnecessary for a 25-node prototype. Consider a graph database only after the data grows across many boards, subjects and versions.

## 5. Core Data Model

| Entity | Important fields |
|---|---|
| Curriculum | board, grade, subject, medium, version, source URL, licence notes |
| LearningOutcome | curriculum, code, description, unit, source reference |
| Concept | canonical name, description, subject, representation type |
| CurriculumConcept | curriculum, concept, local terminology, coverage depth |
| PrerequisiteEdge | prerequisite concept, dependent concept, rationale, reviewer, status |
| ConceptMapping | source concept, destination concept, relation, confidence, reviewer status |
| DiagnosticItem | concept, difficulty, language, representation, answer key, source/reviewer |
| LearnerProfile | prototype identifier, source curriculum, destination curriculum, preferred language |
| DiagnosticSession | learner, target outcomes, status, started/completed timestamps |
| Attempt | session, item, response, score, response time, evidence type |
| MasteryEstimate | session, concept, probability, evidence count, uncertainty |
| BridgePlan | session, version, teacher, approval status, target outcome |
| BridgeStep | plan, concept, order, resource link, completion evidence |
| Reassessment | plan, target item, result, teacher decision, timestamp |
| AuditEvent | actor, action, entity, timestamp, reason |

## 6. Concept Graph

Represent the curriculum as a directed acyclic graph for the prototype:

```text
integer operations
       ↓
negative-number operations
       ↓
algebraic simplification
       ↓
linear equations
```

An edge means that the first concept supports learning the second. Every edge used in the demonstration should include a short rationale and teacher-review status.

### Graph constraints

- block self-references;
- detect cycles before publishing a graph version;
- keep source provenance for each curriculum outcome;
- separate curriculum coverage from universal concept identity;
- version mappings when a board changes its curriculum;
- never treat an AI-suggested edge as approved until a reviewer confirms it.

## 7. Adaptive Diagnostic Algorithm

### Prototype method

1. Begin with an item for the destination learning outcome.
2. Record correctness, response time and selected evidence tags.
3. When evidence is weak or incorrect, choose a question from the nearest untested prerequisite.
4. When mastery is sufficiently supported, prune older ancestor branches.
5. Continue until the system finds the earliest weak prerequisite or reaches the question limit.
6. Present all inferences with confidence and evidence to the teacher.

### Simple mastery model

Use an explainable Beta-Binomial estimate for the first prototype:

```text
mastery_probability = (correct_evidence + prior_success) /
                      (all_evidence + prior_success + prior_failure)
```

Weight or separate evidence when items use different languages or representations. Do not convert one wrong answer into a firm gap.

The team may evaluate Item Response Theory or Bayesian Knowledge Tracing later. They are not required to prove the workflow.

## 8. Minimum Bridge-Path Generation

The bridge generator should:

1. collect weak or uncertain ancestors of the destination concept;
2. remove concepts already supported by sufficient evidence;
3. order remaining concepts by graph dependency;
4. attach one reviewed learning activity and one exit check to each step;
5. allow the teacher to add, remove or reorder steps;
6. reassess the destination outcome after the bridge.

The word "minimum" means the shortest defensible prerequisite sequence for the selected target, not the least possible teaching time.

## 9. Language-Aware Evidence

GapMap should avoid treating English difficulty as mathematics failure.

For selected concepts, prepare equivalent items with different language demands:

- symbolic or visual item with minimal text;
- item in the learner's familiar language;
- item using the destination classroom terminology.

If the learner solves the low-language and familiar-language versions but fails only on destination terminology, show **possible terminology barrier**. A teacher decides the next action. The system does not claim a medical or cognitive diagnosis.

## 10. AI Components

### Suitable uses

- extract candidate learning outcomes from authorised curriculum documents;
- suggest possible equivalences across boards and languages;
- produce reviewed question variants from a teacher-approved template;
- explain the same verified concept in the learner's selected language;
- retrieve a relevant approved textbook or DIKSHA resource;
- summarise diagnostic evidence for a teacher.

### Non-AI components

- prerequisite traversal;
- mastery calculation;
- bridge ordering;
- permissions and audit history;
- source and curriculum versioning;
- final teacher approval.

### Guardrails

- send only the minimum learner data to a model;
- never put names or government IDs in prompts;
- require structured JSON output and validate it;
- attach source references to curriculum claims;
- reject concepts or questions outside the approved graph;
- log the model, prompt version and reviewer decision;
- provide a deterministic fallback when the AI service fails.

## 11. API Outline

```text
GET    /api/curricula/
POST   /api/curricula/compare/
GET    /api/graphs/{curriculum_id}/
POST   /api/mappings/{id}/review/
POST   /api/diagnostic-sessions/
GET    /api/diagnostic-sessions/{id}/next-item/
POST   /api/diagnostic-sessions/{id}/attempts/
GET    /api/diagnostic-sessions/{id}/gap-map/
POST   /api/diagnostic-sessions/{id}/bridge-plan/
PATCH  /api/bridge-plans/{id}/
POST   /api/bridge-plans/{id}/approve/
POST   /api/bridge-plans/{id}/steps/{step_id}/complete/
POST   /api/bridge-plans/{id}/reassess/
GET    /api/teachers/cohort-gaps/
```

## 12. Interface Requirements

### Student diagnostic

- show one question at a time;
- offer language selection without changing the concept target;
- support keyboard navigation and clear focus states;
- explain that the assessment builds a support path, not a grade;
- show progress as a range when adaptive length varies;
- provide a pause and resume option.

### Student bridge view

- show the destination topic and ordered prerequisites;
- display one current step rather than the entire curriculum;
- link every activity to its source;
- show completed evidence and the next reassessment.

### Teacher dashboard

- inspect the source and destination curriculum map;
- see each inferred gap with supporting attempts;
- approve or reject AI-suggested mappings;
- edit and assign the bridge plan;
- view uncertainty and unresolved branches;
- group learners by shared prerequisite gap.

## 13. Privacy and Safety

- use synthetic learner data for the hackathon;
- do not collect Aadhaar, APAAR ID or official marksheets;
- use role-based access for student and teacher views;
- keep individual results out of public analytics;
- store only responses needed for diagnostic evidence;
- define deletion and retention settings before a real pilot;
- do not infer disability, intelligence or dropout risk;
- allow teachers and learners to correct profile and language information.

## 14. Data Required for the Prototype

The team needs:

- official learning outcomes for the chosen curricula;
- unit and topic metadata for the selected mathematics scope;
- a teacher-reviewed 25-node concept graph;
- approximately two reviewed diagnostic items per concept;
- at least two bilingual terminology-check pairs;
- one reviewed resource and exit check per bridge concept;
- two synthetic student scenarios with known intended gaps.

Use full textbook content only when its licence permits that use. Otherwise store citations, small necessary excerpts within applicable limits and links to the official resource.

## 15. Suggested Repository Structure

```text
gapmap/
├── backend/
│   ├── config/
│   ├── accounts/
│   ├── curricula/
│   ├── concepts/
│   ├── diagnostics/
│   ├── bridge_plans/
│   └── audit/
├── frontend/
│   └── src/
│       ├── student/
│       ├── teacher/
│       ├── components/
│       └── services/
├── data/
│   ├── curricula/
│   ├── concept_graphs/
│   ├── question_bank/
│   └── demo/
├── documents/
│   └── presentation/
├── tests/
├── docker-compose.yml
├── README.md
├── USP.md
├── plan.md
└── tech.md
```

## 16. Build Order

### Vertical slice

1. Create curriculum, concept, edge and question models.
2. Seed five concepts for one algebra dependency chain.
3. Implement target-to-prerequisite traversal.
4. Submit diagnostic attempts and calculate mastery.
5. Generate and display an ordered bridge path.
6. Let a teacher approve the plan.
7. Reassess the target concept.

### Expand after the slice works

1. Increase the graph to approximately 25 concepts.
2. Add the source-to-destination curriculum comparison.
3. Add English and Hindi evidence pairs.
4. Add candidate mapping and grounded explanation AI.
5. Add cohort analysis and presentation polish.

## 17. Testing Strategy

### Unit tests

- graph cycle rejection;
- ancestor traversal and branch pruning;
- mastery update calculations;
- bridge ordering;
- permissions and teacher approval;
- AI output schema rejection.

### Scenario tests

- root concept gap;
- known prerequisite gap;
- terminology-only difficulty;
- mixed terminology and concept difficulty;
- confident mastery that prunes unnecessary questions;
- uncertain evidence that routes to teacher review.

### Demonstration acceptance test

The team can start with a destination algebra item, identify a prepared negative-number gap, distinguish a prepared terminology issue, generate a reviewed bridge and show improved readiness after reassessment.

## 18. Technical Definition of Done

- the graph contains no cycles or unreviewed production edges;
- every diagnostic item has a concept tag and provenance;
- the adaptive path is reproducible from stored evidence;
- every inferred gap displays its supporting attempts;
- the bridge respects prerequisite order;
- a teacher can modify and approve the path;
- reassessment uses a different item for the same outcome;
- the interface contains no claim of disability or intelligence;
- the prototype works without APAAR or any private government API.
