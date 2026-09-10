# GapMap

## Curriculum Transition and Learning Recovery System

GapMap helps students who enter a new curriculum but cannot follow the current classroom because some prerequisite concepts are missing or expressed in an unfamiliar academic language.

The system compares the learner's source and destination curricula, runs a short adaptive diagnostic, traces mistakes through a concept dependency graph and creates the minimum bridge path required for the current topic. A teacher reviews the path, and the learner is reassessed until classroom readiness improves.

## The Problem

A student may change state board, medium of instruction or institution, or return after a long absence. Admission and academic records may transfer successfully while learning readiness does not. A low test score shows that the learner is struggling, but it rarely shows the earliest missing prerequisite or whether unfamiliar terminology caused the error.

## Core Workflow

```text
Select source and destination curriculum
        ↓
Map equivalent learning outcomes and prerequisites
        ↓
Run a short adaptive diagnostic
        ↓
Separate likely language difficulty from concept difficulty
        ↓
Identify the earliest missing prerequisites
        ↓
Generate a minimum teacher-reviewed bridge path
        ↓
Reassess readiness for the current classroom topic
```

## Prototype Scope

The hackathon prototype will demonstrate:

- one curriculum transition in Class 8 to 9 mathematics;
- approximately 25 prerequisite concepts;
- English and Hindi diagnostic prompts;
- a source-to-destination curriculum comparison;
- adaptive prerequisite traversal;
- a student gap map and bridge plan;
- teacher review and reassessment;
- synthetic learner profiles and clearly labelled demonstration results.

## Project Boundaries

GapMap does not replace APAAR, UDISE+, DIKSHA, PRABANDH or a school ERP.

- APAAR carries identity, credentials and academic credits.
- UDISE+ records education-management data.
- PRABANDH tracks out-of-school learners until mainstreaming.
- DIKSHA provides curriculum content, quizzes and learning resources.
- GapMap diagnoses readiness for a destination curriculum and sequences the missing prerequisites.

## Documentation

- [Unique selling proposition](USP.md)
- [Product and delivery plan](plan.md)
- [Technical architecture](tech.md)
- `documents/presentation/GapMap-SIH26207-Presentation-v2.pptx`
- `documents/presentation/gapmap-workflow.png`

## Project Status

- [x] Problem direction selected
- [x] Existing public education systems compared
- [x] GapMap presentation prepared
- [x] Initial product and technical plan prepared
- [ ] Mathematics transition scope finalised with a teacher
- [ ] Curriculum concept graph created
- [ ] Diagnostic question bank prepared and reviewed
- [ ] Backend and frontend scaffolded
- [ ] Adaptive diagnostic implemented
- [ ] Bridge-path generation implemented
- [ ] Teacher dashboard completed
- [ ] Prototype tested on prepared transition scenarios

## Official References

- Ministry of Education, ABSS 2025 Outcome Document: https://www.education.gov.in/sites/upload_files/mhrd/files/nep/ABSS_2025_Outcome_Document.pdf
- NCERT: https://www.ncert.nic.in/
- DIKSHA: https://diksha.gov.in/about-us/
- APAAR: https://apaar.education.gov.in/
- UDISE+: https://www.udiseplus.gov.in/

Public-platform scope can change. Recheck all comparisons before the final submission.
