# GapMap: Domain Scalability and Standardised-Education Strategy

## Purpose

This note answers two important evaluation questions:

1. How can GapMap work across school education, engineering, pharmacy, agriculture and foreign higher education?
2. If education is standardised, what gap is left for GapMap to identify?

## Core Positioning

> GapMap measures the difference between a learner's demonstrated readiness and the competencies required at their next academic destination.

It does not depend only on differences between two syllabus documents.

```text
Destination expectations
          minus
Verified learner evidence
          equals
Actionable transition gap
```

## 1. Scaling Across Educational Domains

A fixed roadmap cannot represent every programme. GapMap therefore uses a common competency model with separate, expert-reviewed domain packs.

### Shared system model

Every domain is represented using the same structure:

```text
Programme
   -> Courses or modules
      -> Learning outcomes
         -> Canonical competencies
            -> Prerequisite relationships
```

The software remains common. Only the reviewed academic data changes between domains.

### Domain packs

| Domain | Example competencies and evidence |
|---|---|
| School education | Grade-level concepts, board outcomes and academic terminology |
| Engineering | Mathematics, design, programming, simulation and laboratory work |
| Pharmacy | Chemistry, pharmacology, biostatistics, clinical and laboratory experience |
| Agriculture | Soil science, crop science, fieldwork, environmental science and statistics |
| International education | Programme prerequisites, course depth, credits, language and documentary evidence |

### What is compared

GapMap compares learning outcomes rather than relying on course names.

Two courses with different names may cover equivalent competencies. Two courses with the same name may differ in depth, credits or practical work.

The result for each destination requirement is classified as:

- satisfied;
- partially satisfied;
- missing;
- uncertain;
- document verification required; or
- external institutional requirement.

### International transition example

A synthetic Indian B.Pharm graduate wants to enter a foreign Master of Data Science programme.

| Destination requirement | Source evidence | GapMap result |
|---|---|---|
| Probability and statistics | Biostatistics and Research Methodology | Satisfied |
| Programming | Computer Applications in Pharmacy | Partial: course title and credits exist, but programming depth is uncertain |
| Calculus or linear algebra | Remedial Mathematics | Needs review because content and accepted credit equivalence may differ |
| English-language proficiency | No recognised certificate uploaded | Document required |

GapMap diagnoses academic uncertainty, but it does not claim authority over admission, licensing or official credit transfer.

### Domain-scaling workflow

```text
Official curriculum and programme documents
                    -> AI proposes structured outcomes
                    -> Domain expert reviews mappings
                    -> Approved, versioned competency graph
                    -> Learner evidence is compared
                    -> Minimum transition roadmap is generated
```

AI accelerates document interpretation. Approved evidence and deterministic rules control the final roadmap.

## 2. GapMap Under Standardised Education

Standardisation defines what should be taught. It does not guarantee that every learner received, retained or mastered it.

```text
Prescribed curriculum != delivered coverage != demonstrated mastery
```

### Gaps that remain under one standard

| Gap | Example |
|---|---|
| Mastery gap | A learner attended the algebra unit but cannot manipulate negative numbers |
| Coverage gap | A class did not finish the final unit |
| Sequence gap | The destination class reached a topic earlier than the source class |
| Interruption gap | Illness, migration or absence caused missed learning |
| Retention gap | A prerequisite was passed previously but is no longer usable |
| Language gap | The concept is understood but unfamiliar terminology causes failure |
| Depth gap | A topic was introduced, while the destination expects application or analysis |
| Evidence gap | Knowledge may exist, but sufficient academic or practical proof is unavailable |

### Two operating modes

#### Mode A: Different curricula

```text
Map source outcomes to destination outcomes
                    -> identify curriculum differences
                    -> diagnose uncertain competencies
                    -> generate bridge path
```

#### Mode B: Same standardised curriculum

```text
Reuse the common competency graph
                    -> compare learner evidence with target prerequisites
                    -> diagnose only uncertain areas
                    -> generate a bridge only for confirmed gaps
```

If the learner demonstrates all required competencies, GapMap must return:

> No significant gap detected. The learner is ready for the target topic.

This prevents unnecessary intervention and makes the result trustworthy.

## 3. How the Roadmap Is Produced

The roadmap is not generated freely by a language model.

1. Read the destination programme's mandatory and recommended competencies.
2. Collect verified learner evidence from courses, assessments, projects and practical work.
3. Use AI to propose semantic matches and explain possible differences.
4. Apply deterministic rules for credits, depth, prerequisites and document requirements.
5. Run short diagnostics only for uncertain academic competencies.
6. Traverse the approved prerequisite graph to locate the earliest confirmed gaps.
7. Generate the minimum ordered learning and verification plan.
8. Present the evidence, confidence and source for human review.

## 4. What AI Does and Does Not Do

### AI assists with

- extracting learning outcomes from curriculum documents;
- normalising different academic terminology;
- proposing source-to-destination competency matches;
- identifying partial overlap;
- generating evidence-grounded explanations; and
- creating candidate diagnostic items for review.

### Deterministic software controls

- credit and depth validation;
- prerequisite traversal;
- mandatory versus recommended requirements;
- diagnostic scoring;
- roadmap ordering;
- approval status; and
- the separation of academic and documentary gaps.

### Human reviewers control

- publishing curriculum mappings;
- accepting ambiguous equivalence;
- verifying practical, laboratory or clinical evidence; and
- making official academic or admission decisions.

## 5. Suggested Presentation Slide

### Title

**One Engine, Multiple Domains, Individual Readiness**

### Main visual

```text
School | Engineering | Pharmacy | Agriculture | Foreign Programme
                              |
                    Reviewed domain packs
                              |
                  Common competency graph
                              |
                 Learner-specific evidence
                              |
            Satisfied | Partial | Missing | Verify
                              |
                Minimum transition roadmap
```

### Supporting statement

> Standardisation gives GapMap a reusable reference graph; personal evidence reveals where each learner is actually ready, uncertain or blocked.

## 6. Short Answers for Judges

### Question: How will this scale to many domains?

> We do not manually create a roadmap for every course or student. Every programme is decomposed into learning outcomes and mapped to canonical competencies. Engineering, pharmacy and agriculture are added as reviewed domain packs using the same data model and roadmap engine. The learner-specific path is calculated dynamically from verified evidence and destination requirements.

### Question: What happens if education is standardised?

> A standard curriculum states what should be taught, not what every learner has mastered. When curricula are identical, GapMap skips curriculum alignment and compares the learner's demonstrated competencies with the target topic's prerequisites. It may find a mastery, coverage, interruption, language or depth gap—or correctly return that no bridge is required.

### Question: Is GapMap deciding foreign admission or credit equivalence?

> No. GapMap is a readiness and evidence-support system. It identifies academic overlap, uncertainty and preparation needs while clearly separating official credit transfer, licensing, language certification and admission decisions for authorised institutions.

## Final Position

> GapMap does not merely compare curricula. It converts destination expectations and learner evidence into an explainable, minimum transition plan across institutions, domains and education systems.
