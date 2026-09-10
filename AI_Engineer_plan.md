# GapMap AI Engineering Plan

## 1. Objective

Build an explainable AI-assisted pipeline that converts curriculum documents, destination requirements and learner evidence into a structured competency comparison.

The language model does not make admission decisions and does not freely generate the final roadmap. It extracts, normalises and proposes mappings. Reviewed data and deterministic rules decide the result and roadmap order.

```text
Official academic documents
          +
Verified learner evidence
          ↓
AI-assisted extraction and semantic alignment
          ↓
Evidence and rule validation
          ↓
Satisfied | Partial | Missing | Uncertain | Document required
          ↓
Deterministic prerequisite planner
          ↓
Explainable minimum transition roadmap
```

## 2. Prototype Scope

### In scope

- prepared text extracted from selected official curriculum documents;
- structured extraction of courses, learning outcomes and requirements;
- mapping different academic terminology to canonical competencies;
- evidence-grounded classification of requirement coverage;
- explicit uncertainty and document requirements;
- short diagnostics for uncertain academic competencies;
- deterministic prerequisite traversal and roadmap generation;
- source citations and reasoning visible to reviewers;
- cached AI results when no model connection is available;
- the six priority scenarios defined in `GapMap-Sample-Data-Scenarios.md`.

### Out of scope for the first prototype

- production transcript OCR;
- unrestricted document uploads;
- automatic credit-transfer or admission decisions;
- professional licensing equivalence;
- a universal competency ontology;
- automatic publication of AI-generated mappings;
- training or fine-tuning a model;
- a generic chatbot;
- a vector database deployment solely for the demonstration.

## 3. Product Principle

The system must distinguish three types of intelligence.

| Layer | Responsibility |
|---|---|
| AI assistance | Extract outcomes, normalise terminology, propose matches and explain evidence |
| Deterministic engine | Check credits, mandatory conditions, prerequisites, evidence status and roadmap order |
| Human authority | Approve ambiguous mappings and make institutional, admission or licensing decisions |

AI output is always a proposal until it passes validation and, where necessary, review.

## 4. Initial Data Sources

The first higher-education demonstration uses:

- Pharmacy Council of India B.Pharm syllabus;
- UBC Master of Data Science admission requirements;
- UBC prerequisite-course descriptions;
- a clearly labelled synthetic learner transcript based on real PCI course codes;
- manually reviewed expected results for scenario S05.

The school demonstration continues using the prepared Maharashtra Grade 8 to CBSE Grade 9 mathematics graph.

Every extracted fact must store:

- document title;
- organisation;
- source URL;
- document or curriculum version;
- page number or webpage section;
- exact supporting excerpt;
- retrieval date;
- extraction method; and
- review status.

## 5. Canonical Data Model

The current `Concept` model represents a canonical competency. Higher-education documents require additional structured records around it.

### Source record

```json
{
  "source_id": "pci-bpharm-2016",
  "title": "B.Pharm Scheme and Syllabus",
  "organisation": "Pharmacy Council of India",
  "source_type": "official_pdf",
  "url": "https://pci.nic.in/pdf/Syllabus_B_Pharm.pdf",
  "version": "implemented-2016-17",
  "retrieved_at": "YYYY-MM-DD"
}
```

### Extracted course

```json
{
  "course_code": "BP801T",
  "title": "Biostatistics and Research Methodology",
  "credits": 4,
  "level": "undergraduate",
  "topics": [
    "probability theory",
    "regression",
    "hypothesis testing",
    "ANOVA"
  ],
  "learning_outcomes": [],
  "evidence": {
    "source_id": "pci-bpharm-2016",
    "page": 158,
    "excerpt": "..."
  },
  "extraction_status": "reviewed"
}
```

### Destination requirement

```json
{
  "requirement_id": "ubc-mds-statistics",
  "name": "University-level probability or statistics",
  "requirement_type": "academic",
  "mandatory": true,
  "minimum_credits": 3,
  "accepted_alternatives_group": null,
  "expected_competencies": [
    "probability",
    "statistical inference"
  ],
  "evidence": {
    "source_id": "ubc-mds-admissions",
    "section": "Admission Requirements",
    "excerpt": "..."
  }
}
```

### Learner evidence

```json
{
  "evidence_id": "ananya-bp801t",
  "learner_id": "ananya-demo",
  "evidence_type": "completed_course",
  "course_code": "BP801T",
  "grade": "A",
  "credits": 4,
  "verified": true,
  "document_reference": "synthetic-transcript-row-18"
}
```

### Competency match

```json
{
  "requirement_id": "ubc-mds-statistics",
  "source_evidence_ids": ["ananya-bp801t"],
  "status": "satisfied",
  "matched_competencies": [
    "probability",
    "regression",
    "hypothesis testing"
  ],
  "missing_competencies": [],
  "credit_check": "passed",
  "model_confidence": 0.93,
  "reason": "The verified four-credit course covers the core statistical topics.",
  "citations": [],
  "requires_human_review": false,
  "decision_source": "rules_after_ai_proposal"
}
```

## 6. AI Pipeline

### Stage 1 — Controlled ingestion

For the first prototype, curriculum text is extracted before the demonstration and stored as reviewed fixtures.

```text
PDF or official webpage
        ↓
Text extraction
        ↓
Section and page boundaries retained
        ↓
Reviewed document chunks
```

This avoids depending on slow parsing, website availability or OCR during judging.

### Stage 2 — Structured academic extraction

The extraction model receives one bounded course or requirement section. It returns JSON matching a strict schema.

Extracted fields include:

- course code and title;
- credits or hours;
- learning outcomes;
- topics;
- competency verbs;
- practical, laboratory or clinical requirements;
- mandatory or recommended status;
- alternatives; and
- supporting source span.

The output is rejected when:

- it is not valid JSON;
- required fields are absent;
- the cited excerpt is not present in the supplied chunk;
- credits were inferred without evidence; or
- a mandatory requirement was converted into a recommendation.

### Stage 3 — Competency normalisation

Different phrases are mapped to canonical competencies.

```text
“Biostatistical hypothesis testing”
“Statistical significance testing”
“Testing statistical hypotheses”
                    ↓
Canonical competency: hypothesis-testing
```

The system retains both the original phrase and canonical competency. Original institutional terminology is never discarded.

### Stage 4 — Candidate retrieval

The system retrieves plausible learner-evidence candidates for each destination requirement.

Prototype order:

1. exact course-code or reviewed mapping;
2. canonical competency overlap;
3. token and phrase similarity;
4. optional embedding similarity;
5. no candidate when evidence is too weak.

At prototype scale, reviewed mappings and simple similarity are sufficient. Embeddings and pgvector become useful when thousands of outcomes are loaded.

### Stage 5 — Evidence-grounded semantic verifier

The verifier receives only:

- one destination requirement;
- a small number of retrieved source courses;
- learner verification state;
- relevant source excerpts; and
- the allowed result labels.

It returns:

- matched topics;
- missing topics;
- possible depth mismatch;
- proposed status;
- concise reasoning;
- cited source IDs; and
- whether human review is required.

It is forbidden from using general model knowledge as evidence for curriculum equivalence.

### Stage 6 — Deterministic requirement engine

Rules can override an AI proposal when objective constraints fail.

Examples:

```text
AI proposes “satisfied”
but verified credits < minimum credits
                    ↓
Final status = partial or uncertain
```

```text
Requirement type = recognised language certificate
                    ↓
Final status = document_required
No diagnostic may replace it
```

```text
No verified learner evidence
                    ↓
Final status cannot be satisfied
```

### Stage 7 — Diagnostic routing

Diagnostics are created only for academic requirements with `partial` or `uncertain` status.

| Status | Diagnostic action |
|---|---|
| `satisfied` | Skip |
| `partial` | Test only uncovered or weak competencies |
| `missing` | Usually start the prerequisite bridge; optionally confirm entry level |
| `uncertain` | Request evidence or run a short diagnostic |
| `document_required` | Request document |
| `external_requirement` | Refer to authorised institution |

The existing adaptive service can then move backward through approved prerequisites.

### Stage 8 — Roadmap planning

The roadmap generator consumes final structured requirement results rather than raw model text.

```text
Confirmed academic gaps
        +
Partial competencies
        +
Approved prerequisite graph
        +
Document checklist
        ↓
Topologically ordered minimum plan
```

Roadmap items are separated into:

- `learn` — acquire a missing competency;
- `practice` — strengthen partial mastery;
- `diagnose` — resolve academic uncertainty;
- `verify` — supply academic evidence;
- `document` — upload required official proof; and
- `review` — obtain an institutional decision.

### Stage 9 — Explanation generation

The explanation layer converts structured results into student-friendly and reviewer-facing language.

It may explain the roadmap but cannot add, remove or reorder mandatory steps. Every explanation must reference the structured decision and its evidence.

## 7. Role of RAG

RAG is useful for retrieving the correct evidence from long curriculum documents. It is not the roadmap decision-maker.

```text
Question: Does BP205T satisfy the programming requirement?
                         ↓
Retrieve BP205T topics + destination programming description
                         ↓
Model compares only retrieved evidence
                         ↓
Rules validate credits, verification and requirement type
```

RAG provides grounding and citations. The rule engine provides consistency.

## 8. Prompt Contracts

Use separate prompts for separate tasks. Do not ask one model call to extract documents, compare programmes and write the roadmap simultaneously.

### Extraction prompt contract

```text
System role: Academic document extractor
Input: One document chunk and source metadata
Output: ExtractionSchema JSON only
Rules:
- use only supplied text;
- preserve original terminology;
- do not invent credits or outcomes;
- include supporting spans;
- return an uncertainty flag where text is ambiguous.
```

### Mapping prompt contract

```text
System role: Evidence-grounded competency alignment assistant
Input: One destination requirement and retrieved learner evidence
Output: MappingProposalSchema JSON only
Allowed relations: equivalent, partial, unrelated, uncertain
Rules:
- distinguish topic overlap from credit equivalence;
- list missing topics;
- cite supplied evidence IDs;
- never make an admission decision.
```

### Explanation prompt contract

```text
System role: Student transition-plan explainer
Input: Final rule-engine result and approved roadmap
Output: Plain-language explanation
Rules:
- do not change statuses or steps;
- explain why each step exists;
- label institutional decisions clearly.
```

## 9. Confidence and Decision Policy

Model confidence alone must not determine the final status.

| Condition | Final handling |
|---|---|
| Reviewed exact mapping and verified evidence | Rules may mark satisfied |
| Strong semantic match but insufficient credits | Partial or human review |
| Strong topic match but evidence is unverified | Uncertain |
| Weak or conflicting match | Uncertain |
| No evidence | Missing or document required, depending on requirement type |
| Regulatory, licensing or admission decision | External requirement |

Confidence is displayed as supporting metadata, not as an official equivalence probability.

## 10. Human Review States

Every AI-created academic record has one of these states:

```text
proposed -> reviewed -> approved
                └----> rejected
```

Only approved prerequisite edges and mappings can affect a published roadmap. The demo may use manually reviewed fixtures labelled `demo_reviewed`.

## 11. Planned Backend Components

No implementation is required before the frontend prototype, but the eventual structure should be:

```text
backend/Gap/map/ai_engineering/
├── __init__.py
├── adapters.py       # provider-neutral model interface
├── schemas.py        # Pydantic input and output contracts
├── extraction.py     # document-to-course/requirement extraction
├── retrieval.py      # evidence candidate retrieval
├── alignment.py      # semantic mapping proposals
├── rules.py          # credits, evidence and requirement policies
├── explanations.py   # grounded user-facing explanations
└── fixtures.py       # cached demonstration responses
```

The current graph logic in `map/services.py` remains deterministic and consumes approved results from this layer.

## 12. Proposed API Contract

### List demo scenarios

```http
GET /api/demo-scenarios/
```

Returns lightweight cards for S01, S02, S03, S04, S05 and S10.

### Analyse a transition

```http
POST /api/transitions/analyse/
```

```json
{
  "scenario_id": "S05",
  "execution_mode": "cached_demo"
}
```

Response:

```json
{
  "transition_id": "transition-s05-001",
  "execution_mode": "cached_demo",
  "source_program": {},
  "destination_program": {},
  "summary": {
    "satisfied": 1,
    "partial": 1,
    "uncertain": 1,
    "document_required": 1
  },
  "requirements": [],
  "provenance": [],
  "review_status": "demo_reviewed"
}
```

### Generate roadmap

```http
POST /api/transitions/{transition_id}/roadmap/
```

The endpoint reads the stored structured results and returns ordered roadmap items. It does not send the entire decision back to a model.

### Retrieve AI reasoning evidence

```http
GET /api/transitions/{transition_id}/evidence/
```

Returns the mapping explanation, supporting excerpts and decision source for the expandable reviewer view.

## 13. Offline and Failure Strategy

The judging demonstration must not depend on network access.

### Cached demo mode

- reviewed extraction and mapping outputs are stored locally;
- API responses use the same schema as live mode;
- the UI labels the result “Reviewed demonstration analysis”;
- deterministic roadmap generation still runs normally.

### Live AI mode

- enabled only when a provider key is configured;
- uses strict structured outputs;
- has a short timeout and limited retries;
- validates citations and schemas;
- falls back to cached mode on failure;
- never replaces the previously reviewed fixture silently.

### Failure states

| Failure | Behaviour |
|---|---|
| Model timeout | Use cached reviewed analysis |
| Invalid JSON | Reject response and use cached analysis |
| Unsupported citation | Mark proposal invalid |
| No matching evidence | Return uncertain, not satisfied |
| Cycle in prerequisite graph | Block roadmap generation and request review |
| Missing official source | Label scenario as illustrative only |

## 14. Security and Privacy

- Treat curriculum text and uploaded documents as untrusted data, not instructions.
- Do not place document text in system-level prompts.
- Remove unnecessary personal information before external model calls.
- Use synthetic learner identities in the demonstration.
- Store only the minimum evidence needed for the prototype.
- Never expose answer keys in question-delivery responses.
- Log model version, prompt version, execution mode and validation result.
- Do not log API keys, complete transcripts or sensitive identifiers.

## 15. Evaluation Plan

### Scenario-based evaluation

| Scenario | Required behaviour |
|---|---|
| S01 | Return no academic gap |
| S02 | Find a mastery gap despite identical curricula |
| S03 | Separate terminology difficulty from concept mastery |
| S04 | Find the nearest weak prerequisite |
| S05 | Separate satisfied, partial, uncertain and document-required results |
| S10 | Refuse unsupported equivalence and expose uncertainty |

### Extraction checks

- course codes match the source;
- credits match the source;
- every extracted outcome has a supporting span;
- no unsupported requirement is added;
- original terms are preserved.

### Mapping checks

- expected source evidence appears in the candidate set;
- missing topics are named;
- insufficient credits cannot produce `satisfied`;
- unverified evidence cannot produce `satisfied`;
- documentary requirements never become learning diagnostics.

### Roadmap checks

- satisfied competencies are excluded from mandatory learning steps;
- every learning step traces to a confirmed gap;
- prerequisite order is valid;
- uncertainty creates diagnosis or verification rather than forced learning;
- the same structured input produces the same roadmap.

## 16. Frontend Contract

The frontend should be built before live AI integration using the cached API response shapes in this plan.

### Screen 1 — Scenario selection

- six scenario cards;
- learner situation;
- source and destination;
- “Analyse transition” action;
- clear synthetic-data label.

### Screen 2 — Competency comparison

- summary counts by status;
- requirement cards;
- source evidence and target expectation;
- credit and depth checks;
- AI proposal versus final rule decision;
- expandable citations;
- review-required indicator.

### Screen 3 — Transition roadmap

- ordered academic steps;
- separate document checklist;
- reason for every step;
- linked destination requirement;
- estimated time;
- readiness reassessment;
- “No bridge required” state for S01.

### Screen 4 — How the analysis worked

A compact judge-facing panel:

```text
2 official sources
        ↓
7 course/requirement records extracted
        ↓
4 competency mappings proposed
        ↓
4 deterministic checks applied
        ↓
1 focused academic bridge + 1 document action
```

## 17. Demonstration Sequence

1. Open S01 and show that identical curricula plus strong evidence produce no gap.
2. Open S02 and show that identical curricula can still contain a learner mastery gap.
3. Open S05 and show the PCI and UBC source links.
4. Run the reviewed analysis.
5. Expand the programming requirement to show topic overlap but insufficient depth.
6. Expand the statistics requirement to show why it is satisfied.
7. Show that English evidence is kept outside the academic diagnostic.
8. Generate the minimum roadmap.
9. Open the “How it worked” panel and explain AI, rules and human-review boundaries.

## 18. Delivery Order

### Now: frontend prototype

1. Freeze the response contracts in this document.
2. Create local TypeScript fixtures for the six scenarios.
3. Build the four screens and all result states.
4. Connect the existing school diagnostic where practical.
5. Verify the complete judge demonstration without any model key.

### After the frontend works: AI adapter

1. Add Pydantic schemas.
2. Add cached fixture adapter.
3. Implement extraction for the selected official documents.
4. Add candidate retrieval.
5. Add one provider-backed structured mapping call.
6. Add rule validation and audit metadata.
7. Confirm live and cached modes return identical API shapes.

### After evaluation

- add reviewer workflow and authentication;
- add more verified domain packs;
- add document upload and controlled parsing;
- add embeddings only when corpus size justifies them;
- evaluate mappings with domain experts;
- add data-retention and consent controls.

## 19. Definition of Done for the Prototype

The prototype is successful when:

- six scenarios render through one common interface;
- both different-curriculum and same-standard cases work;
- S01 returns no unnecessary roadmap;
- S05 displays real official sources and synthetic learner labelling;
- each result shows the evidence and rule that produced it;
- academic and documentary actions are separated;
- roadmap generation is deterministic;
- cached mode works without internet;
- the team can explain AI, rules and human responsibility in under one minute.

## Final Engineering Position

> GapMap uses AI to understand heterogeneous academic language and retrieve comparable evidence. It uses deterministic policy and graph logic to decide what is satisfied, uncertain or missing and to produce the minimum roadmap. This makes the prototype intelligent without making it unaccountable.
