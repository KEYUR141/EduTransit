# GapMap Sample Data Scenarios

## Purpose

This is the review catalogue for the working prototype. It defines the learner input, transition context, expected reasoning and expected roadmap before we implement the AI layer or frontend.

The learner records are synthetic. Curriculum structures and destination requirements should come from public, official documents and retain their source links, sections and versions.

## Dataset Principles

Every scenario must demonstrate at least one of these outcomes:

- the learner is ready and needs no roadmap;
- a curriculum difference exists;
- the curriculum is identical but mastery differs;
- terminology or language is the main barrier;
- a course partially covers a destination requirement;
- knowledge may exist but acceptable evidence is missing;
- a requirement is administrative and must not be replaced by an AI quiz; or
- the available evidence is too uncertain for an automatic conclusion.

The system must never create a gap merely to produce a roadmap.

## Common Result Labels

| Label | Meaning | System action |
|---|---|---|
| `satisfied` | Verified evidence meets the requirement | Do not prescribe relearning |
| `partial` | Some topics, depth or credits match | Diagnose the uncertain portion or add a focused bridge |
| `missing` | No acceptable evidence covers the competency | Add prerequisite-aware bridge work |
| `uncertain` | Evidence is insufficient or conflicting | Request evidence or run a short diagnostic |
| `document_required` | Official proof is required | Add a document checklist, not a learning module |
| `external_requirement` | An institution must make the decision | Flag it and stop automatic reasoning |
| `not_applicable` | The requirement does not apply to this learner | Exclude it from the roadmap |

## Scenario Catalogue

### S01 — Same Standard, Fully Ready

**Purpose:** Prove that GapMap can return no gap.

| Field | Sample value |
|---|---|
| Learner | Meera Sharma |
| Source | CBSE Class 9 Mathematics |
| Destination | Another CBSE Class 9 school |
| Target | Linear equations in one variable |
| Existing evidence | Recent verified assessment covering integer operations, algebraic expressions and linear equations |
| Diagnostic evidence | Target and prerequisite questions answered correctly |
| Expected result | `satisfied` |
| Expected roadmap | No bridge plan; show “Ready for the target topic” |

**Judge point:** Standardisation supplies the common target graph, while learner evidence determines whether intervention is necessary.

---

### S02 — Same Standard, Interrupted Learning

**Purpose:** Demonstrate a mastery gap without a curriculum gap.

| Field | Sample value |
|---|---|
| Learner | Kabir Ansari |
| Source and destination | CBSE Class 9 Mathematics |
| Situation | Six-week medical absence during the algebra unit |
| Target | Linear equations |
| Diagnostic evidence | Incorrect linear-equation and algebraic-expression responses; correct integer operations |
| Expected result | Algebraic expressions: `missing`; integer operations: `satisfied` |
| Expected roadmap | Algebraic simplification → guided equation solving → reassessment |

**Judge point:** A standard syllabus describes expected coverage; it does not prove that an individual learner received or mastered it.

---

### S03 — Same Concept, Language and Terminology Barrier

**Purpose:** Prevent unnecessary reteaching when the concept is already understood.

| Field | Sample value |
|---|---|
| Learner | Sana Khan |
| Source | Hindi-medium Class 9 mathematics |
| Destination | English-medium Class 9 mathematics using the same board outcomes |
| Target | Arithmetic mean and data interpretation |
| Evidence | Correct calculation when shown symbolically; incorrect response when only unfamiliar English terminology is used |
| Expected result | Concept mastery: `satisfied`; academic terminology: `partial` |
| Expected roadmap | Bilingual terminology card → one contextual practice item → reassessment |

**Judge point:** GapMap distinguishes a language-access problem from a conceptual deficit.

---

### S04 — Cross-Board Sequence and Depth Gap

**Purpose:** Retain the original school-transition demonstration.

| Field | Sample value |
|---|---|
| Learner | Aarav Demo |
| Source | Maharashtra State Board Grade 8 Mathematics |
| Destination | CBSE Grade 9 Mathematics |
| Target | Linear equations |
| Evidence | Target response incorrect; algebraic expressions weak; integer operations strong |
| Expected result | Algebraic prerequisite gap |
| Expected roadmap | Algebraic expressions → linear equations → target reassessment |

**Judge point:** GapMap finds the earliest blocking prerequisite instead of recommending the entire previous grade.

---

### S05 — B.Pharm India to Foreign Data Science Programme

**Purpose:** Demonstrate a cross-domain, international higher-education transition.

| Field | Sample value |
|---|---|
| Learner | Ananya Rao |
| Source | Pharmacy Council of India B.Pharm curriculum |
| Destination | UBC Master of Data Science |
| Verified courses | BP205T Computer Applications in Pharmacy; BP801T Biostatistics and Research Methodology; BP106RMT Remedial Mathematics |
| Target requirements | Programming; probability/statistics; calculus or linear algebra; applicable English-language evidence |

Expected comparison:

| Requirement | Expected status | Reason |
|---|---|---|
| Probability and statistics | `satisfied` | Verified four-credit biostatistics course covers probability, regression and hypothesis testing |
| Programming | `partial` | Three credits exist, but the course does not clearly demonstrate the required program-design depth |
| Calculus or linear algebra | `uncertain` | Relevant topics exist, but the remedial course has limited credit weight and requires institutional review |
| English-language evidence | `document_required` | A platform quiz cannot replace recognised proof |

Expected roadmap:

1. Upload the detailed mathematics course outline for equivalence review.
2. Complete a short programming-readiness diagnostic.
3. If needed, complete Python control flow, functions and data-structure exercises.
4. Complete a small tabular-data analysis task.
5. Upload acceptable English-language evidence if required by the institution.

**Judge point:** Course title, topic coverage, credit depth and documentary requirements are handled separately.

---

### S06 — B.Pharm Internal Progression With Retention Gap

**Purpose:** Show that a standard professional curriculum can still contain learner-specific gaps.

| Field | Sample value |
|---|---|
| Learner | Rohan Patel |
| Programme | PCI B.Pharm |
| Current target | BP801T Biostatistics and Research Methodology |
| Earlier evidence | Mathematics course passed three years earlier |
| Diagnostic evidence | Descriptive statistics correct; probability distributions and hypothesis testing weak |
| Expected result | Probability foundations: `partial`; descriptive statistics: `satisfied` |
| Expected roadmap | Probability refresher → sampling distributions → hypothesis testing → pharmaceutical-data exercise |

**Judge point:** Passing a standard course in the past is evidence, not a permanent guarantee of usable mastery.

---

### S07 — Engineering Graduate With No Academic Gap

**Purpose:** Provide a higher-education no-gap control case.

| Field | Sample value |
|---|---|
| Learner | Vikram Iyer |
| Source | AICTE-aligned Electronics and Communication Engineering degree |
| Destination | UBC Master of Data Science |
| Verified evidence | University courses in programming, probability/statistics, calculus and linear algebra with sufficient credits |
| Academic result | Core academic prerequisites: `satisfied` |
| Remaining result | English evidence: `document_required`, when applicable |
| Expected roadmap | No academic bridge; show only the required application-document checklist |

**Judge point:** GapMap does not force a learning roadmap when verified evidence already meets the target.

---

### S08 — Agriculture Graduate Moving Toward Precision Agriculture

**Purpose:** Test a domain in which field knowledge is strong but digital preparation varies.

| Field | Sample value |
|---|---|
| Learner | Nandini Singh |
| Source | Indian B.Sc. Agriculture programme |
| Destination | Postgraduate precision-agriculture programme |
| Strong evidence | Crop science, soil science and field experimentation |
| Uncertain evidence | GIS, remote sensing, statistics and programming depth |
| Expected result | Domain knowledge: `satisfied`; GIS: `partial`; programming: `missing`; statistics: `uncertain` |
| Expected roadmap | Statistics diagnostic → GIS fundamentals → Python for geospatial data → crop-monitoring mini-project |

**Dataset status:** Extension scenario. Select official source and destination programme documents before presenting its result as real-world validated data.

---

### S09 — Diploma-to-Degree Lateral Entry

**Purpose:** Demonstrate that transferred credits do not automatically prove readiness for every destination topic.

| Field | Sample value |
|---|---|
| Learner | Dev Kumar |
| Source | Diploma in mechanical engineering |
| Destination | Second-year B.Tech mechanical engineering |
| Accepted evidence | Workshop practice and engineering drawing |
| Uncertain evidence | University-level calculus and differential equations |
| Expected result | Practical requirements: `satisfied`; mathematics depth: `partial` |
| Expected roadmap | Mathematics diagnostic → calculus bridge if required → differential-equation applications |

**Dataset status:** Extension scenario requiring an approved diploma and degree curriculum pair.

---

### S10 — Conflicting or Unverifiable Evidence

**Purpose:** Test safe failure instead of confident AI guessing.

| Field | Sample value |
|---|---|
| Learner | Priya Demo |
| Evidence | Transcript lists “Applied Computing,” but no syllabus, credit value or learning outcomes are available |
| Destination requirement | University-level programming |
| Expected result | `uncertain` |
| Expected roadmap | Request official course outline; optionally offer a readiness diagnostic |
| Forbidden result | Automatically declaring the course equivalent or missing |

**Judge point:** Uncertainty is an explicit product state, not something hidden behind an AI confidence score.

## Recommended Prototype Subset

Implement six selectable scenarios in the first frontend:

| Priority | Scenario | Why it is needed |
|---:|---|---|
| 1 | S04 Cross-board gap | Existing end-to-end diagnostic demonstration |
| 2 | S01 Same-standard ready | Proves that “no gap” is a valid result |
| 3 | S02 Same-standard interruption | Answers the standardisation objection |
| 4 | S03 Language barrier | Demonstrates targeted rather than generic intervention |
| 5 | S05 B.Pharm to UBC MDS | Main international and cross-domain demonstration |
| 6 | S10 Unverifiable evidence | Demonstrates trustworthy uncertainty handling |

S06 and S07 can be included if time permits because they reuse the same higher-education data. S08 and S09 should remain labelled future domain packs until their official curriculum pairs are reviewed.

## Minimal Scenario Data Contract

Each scenario should be stored in a predictable structure:

```json
{
  "scenario_id": "S05",
  "title": "B.Pharm India to UBC Master of Data Science",
  "learner": {},
  "source_program": {},
  "destination_program": {},
  "learner_evidence": [],
  "destination_requirements": [],
  "competency_matches": [],
  "diagnostic_evidence": [],
  "expected_requirement_results": [],
  "expected_roadmap": [],
  "source_documents": [],
  "synthetic_fields": [],
  "review_status": "team_review"
}
```

## Validation Rules

Before a scenario is accepted:

1. Every curriculum or programme claim must link to its source document.
2. Every synthetic field must be labelled.
3. Every result must cite the evidence used to produce it.
4. `document_required` items must not become diagnostic questions.
5. A satisfied competency must not appear as mandatory bridge work.
6. A partial match must identify exactly what is missing or uncertain.
7. Roadmap order must follow reviewed prerequisites.
8. The same input must produce the same rule-engine result.
9. The UI must allow a reviewer to inspect the reasoning.
10. At least one scenario must return no academic gap.

## Official Sources for the First Higher-Education Dataset

- Pharmacy Council of India B.Pharm syllabus: https://pci.nic.in/pdf/Syllabus_B_Pharm.pdf
- UBC Master of Data Science admission requirements: https://okanagan.calendar.ubc.ca/faculties-schools-and-colleges/college-graduate-studies/data-science/admission-requirements
- UBC explanation of acceptable prerequisite-course content: https://mds.ubc.ca/admissions/frequently-asked-questions
- AICTE revised ECE model curriculum: https://aicte-qa.aicte-india.org/sites/default/files/Final_ECE.pdf

## Review Decisions Needed Before Implementation

1. Confirm S05 as the primary higher-education presentation scenario.
2. Confirm whether the frontend should expose six or eight selectable scenarios.
3. Approve the common result labels.
4. Decide whether S03 should use Hindi and English or another language pair.
5. Review the expected roadmap for S05 so the AI-engineering contract can be written against it.

After these decisions, the next artifact should be the AI-engineering work plan: extraction schemas, mapping prompts, validation rules, fallback behaviour and API contracts. The frontend can then be implemented against stable sample responses before any live AI integration.
