"""Seed 60 diverse GapMap transition scenarios.

Run from backend/Gap with: python seed_data.py
The script is idempotent. All learner identities and evidence records are synthetic.
"""

import os

import django
from django.core.management import call_command
from django.db import transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Gap.settings")
django.setup()


NAMES = [
    "Aarav",
    "Aditi",
    "Aisha",
    "Akash",
    "Ananya",
    "Arjun",
    "Avni",
    "Dev",
    "Diya",
    "Farhan",
    "Gauri",
    "Harsh",
    "Ira",
    "Ishaan",
    "Jaya",
    "Kabir",
    "Kavya",
    "Kiran",
    "Leena",
    "Manav",
    "Meera",
    "Mohit",
    "Nandini",
    "Neha",
    "Nikhil",
    "Noor",
    "Om",
    "Pooja",
    "Pranav",
    "Priya",
    "Rahul",
    "Rhea",
    "Rohan",
    "Sahil",
    "Sana",
    "Sara",
    "Shreya",
    "Siddharth",
    "Simran",
    "Tara",
    "Tanvi",
    "Uday",
    "Varun",
    "Ved",
    "Vidya",
    "Vikram",
    "Yash",
    "Zara",
    "Aman",
    "Bhavna",
    "Charu",
    "Darsh",
    "Esha",
    "Firoz",
    "Geeta",
    "Hina",
    "Imran",
    "Juhi",
    "Krish",
    "Lakshmi",
]

REASONS = {
    "satisfied": "Recent verified evidence meets the stated competency and depth.",
    "partial": "Relevant learning exists, but one or more destination outcomes need focused support.",
    "missing": "No adequate verified evidence covers this destination competency.",
    "uncertain": "Available evidence cannot establish current competency or depth.",
    "document_required": "This requirement needs accepted official evidence and cannot be replaced by a diagnostic.",
    "external_requirement": "Only the authorised institution or regulator can make this decision.",
}

STATUS_TO_PROGRESS = {
    "satisfied": ("readiness_review", 5),
    "partial": ("roadmap", 4),
    "missing": ("roadmap", 4),
    "uncertain": ("evidence_review", 2),
    "document_required": ("evidence_review", 2),
    "external_requirement": ("evidence_review", 2),
}

# Each archetype has four genuinely different education-domain variants.
# Tuple: source, destination, location.
ARCHETYPES = [
    {
        "code": "same-ready",
        "title": "Same-standard learner already ready",
        "level": "school",
        "kind": "same_standard_ready",
        "rarity": "common",
        "results": [("Current-topic readiness", "satisfied")],
        "steps": [],
        "guardrails": [
            "Do not generate remedial work solely because the institution changed."
        ],
        "variants": [
            (
                "CBSE Grade 9 Mathematics",
                "CBSE Grade 9 Mathematics",
                "Delhi to Karnataka",
            ),
            (
                "ICSE Grade 8 Science",
                "ICSE Grade 8 Science",
                "West Bengal to Maharashtra",
            ),
            (
                "State Board Grade 7 Social Science",
                "Same State Board Grade 7 Social Science",
                "District transfer",
            ),
            ("CBSE Grade 10 English", "CBSE Grade 10 English", "School transfer"),
        ],
    },
    {
        "code": "same-mastery",
        "title": "Same syllabus but current mastery gap",
        "level": "school",
        "kind": "mastery_not_curriculum",
        "rarity": "common",
        "results": [
            ("Curriculum alignment", "satisfied"),
            ("Current mastery", "partial"),
        ],
        "steps": [
            ("diagnose", "Focused current-topic diagnostic"),
            ("learn", "Nearest weak prerequisite bridge"),
        ],
        "guardrails": ["Separate curriculum equivalence from individual mastery."],
        "variants": [
            ("CBSE Grade 8 Mathematics", "CBSE Grade 9 Mathematics", "India"),
            ("ICSE Grade 9 Physics", "ICSE Grade 10 Physics", "India"),
            ("State Board Grade 6 English", "State Board Grade 7 English", "India"),
            ("CBSE Grade 11 Chemistry", "CBSE Grade 12 Chemistry", "India"),
        ],
    },
    {
        "code": "language",
        "title": "Competency hidden by academic-language difficulty",
        "level": "school",
        "kind": "language_access",
        "rarity": "common",
        "results": [
            ("Underlying subject competency", "satisfied"),
            ("Destination terminology", "partial"),
        ],
        "steps": [("practice", "Bilingual terminology bridge")],
        "guardrails": [
            "Use equivalent assessments across languages.",
            "Never convert language difficulty into conceptual failure.",
        ],
        "variants": [
            (
                "Hindi-medium Grade 8 Mathematics",
                "English-medium Grade 9 Mathematics",
                "Uttar Pradesh",
            ),
            (
                "Marathi-medium Grade 9 Science",
                "English-medium Grade 10 Science",
                "Maharashtra",
            ),
            (
                "Bengali-medium Grade 7 Geography",
                "Hindi-medium Grade 8 Geography",
                "Interstate move",
            ),
            (
                "Tamil-medium Grade 11 Biology",
                "English-medium Grade 12 Biology",
                "Tamil Nadu",
            ),
        ],
    },
    {
        "code": "sequence",
        "title": "Cross-board prerequisite sequencing mismatch",
        "level": "school",
        "kind": "curriculum_sequence",
        "rarity": "common",
        "results": [
            ("Earlier outcomes", "satisfied"),
            ("Destination prerequisite", "partial"),
        ],
        "steps": [
            ("learn", "Missing prerequisite micro-bridge"),
            ("diagnose", "Destination-topic reassessment"),
        ],
        "guardrails": [
            "Use approved prerequisite edges.",
            "Do not prescribe the entire destination syllabus.",
        ],
        "variants": [
            (
                "Maharashtra Grade 8 Mathematics",
                "CBSE Grade 9 Mathematics",
                "Maharashtra to Delhi",
            ),
            ("State Board Grade 9 Physics", "ICSE Grade 10 Physics", "Interstate move"),
            ("CBSE Grade 7 Science", "IB Middle Years Science", "India"),
            (
                "Cambridge Lower Secondary Mathematics",
                "CBSE Grade 9 Mathematics",
                "International return",
            ),
        ],
    },
    {
        "code": "interruption",
        "title": "Education interruption with stale evidence",
        "level": "school",
        "kind": "learning_interruption",
        "rarity": "uncommon",
        "results": [
            ("Historical achievement", "satisfied"),
            ("Current readiness", "uncertain"),
        ],
        "steps": [
            ("diagnose", "Low-stakes retention diagnostic"),
            ("review", "Educator-supported re-entry plan"),
        ],
        "guardrails": [
            "Do not infer the reason for absence.",
            "Do not treat old grades as current mastery.",
        ],
        "variants": [
            ("Grade 8 after 10-month break", "Grade 9 re-entry", "India"),
            ("ITI first year after family-care break", "ITI second year", "India"),
            ("First-year B.Com after two-year pause", "B.Com continuation", "India"),
            ("Open-school secondary study", "Regular Grade 10 entry", "India"),
        ],
    },
    {
        "code": "cross-domain",
        "title": "Interdisciplinary higher-study transition",
        "level": "postgraduate",
        "kind": "cross_domain",
        "rarity": "uncommon",
        "results": [
            ("Domain foundation", "satisfied"),
            ("Quantitative foundation", "partial"),
            ("Programming foundation", "missing"),
        ],
        "steps": [
            ("diagnose", "Quantitative depth diagnostic"),
            ("learn", "Focused programming foundation"),
            ("practice", "Cross-domain mini-project"),
        ],
        "guardrails": [
            "Preserve existing domain expertise.",
            "Do not infer depth from course titles alone.",
        ],
        "variants": [
            ("PCI B.Pharm", "Master of Data Science", "India to Canada"),
            ("B.Sc. Agriculture", "Precision Agriculture PG", "India"),
            ("B.A. Economics", "Business Analytics MSc", "India to UK"),
            ("B.Sc. Biology", "Bioinformatics MSc", "India"),
        ],
    },
    {
        "code": "international-docs",
        "title": "International transition with documentary requirements",
        "level": "postgraduate",
        "kind": "study_abroad_documents",
        "rarity": "common",
        "results": [
            ("Academic preparation", "partial"),
            ("Language evidence", "document_required"),
            ("Admission eligibility", "external_requirement"),
        ],
        "steps": [
            ("verify", "Upload detailed course outlines"),
            ("document", "Provide accepted language evidence"),
            ("review", "Destination-institution review"),
        ],
        "guardrails": [
            "A diagnostic cannot replace an official document.",
            "Never make an admission decision.",
        ],
        "variants": [
            (
                "Indian B.Tech Computer Science",
                "German Data Engineering MSc",
                "India to Germany",
            ),
            ("Indian B.Com", "Canadian Finance master's", "India to Canada"),
            ("Indian B.Arch", "UK Urban Planning master's", "India to UK"),
            (
                "Indian B.Sc. Psychology",
                "Australian Psychology master's",
                "India to Australia",
            ),
        ],
    },
    {
        "code": "ambiguous-title",
        "title": "Ambiguous course title without verifiable content",
        "level": "undergraduate",
        "kind": "unverifiable_evidence",
        "rarity": "rare",
        "results": [("Named course competency", "uncertain")],
        "steps": [
            ("verify", "Request official syllabus and credit record"),
            ("diagnose", "Optional readiness diagnostic"),
        ],
        "guardrails": [
            "Never infer content or depth from a title alone.",
            "Return uncertainty instead of guessing.",
        ],
        "variants": [
            (
                "Course titled Applied Computing",
                "University-level programming",
                "India",
            ),
            ("Course titled Quantitative Methods", "Statistics prerequisite", "India"),
            ("Course titled Life Sciences", "Molecular biology prerequisite", "India"),
            (
                "Course titled Professional Practice",
                "Clinical placement requirement",
                "India",
            ),
        ],
    },
    {
        "code": "version",
        "title": "Same qualification name, different curriculum version",
        "level": "undergraduate",
        "kind": "curriculum_version_conflict",
        "rarity": "rare",
        "results": [
            ("Shared core", "satisfied"),
            ("Version-specific outcomes", "partial"),
        ],
        "steps": [
            ("verify", "Confirm curriculum edition"),
            ("diagnose", "Test only newly introduced outcomes"),
        ],
        "guardrails": [
            "Filter retrieval by curriculum version.",
            "Same programme name does not prove identical content.",
        ],
        "variants": [
            (
                "B.Sc. Computer Science 2017 syllabus",
                "B.Sc. Computer Science 2025 continuation",
                "India",
            ),
            (
                "Diploma Mechanical 2015 scheme",
                "B.Tech lateral entry 2026 scheme",
                "India",
            ),
            (
                "B.Pharm 2016 scheme",
                "Updated pharmacy postgraduate prerequisite",
                "India",
            ),
            (
                "Grade 10 legacy state syllabus",
                "Revised Grade 11 state syllabus",
                "India",
            ),
        ],
    },
    {
        "code": "informal-credit",
        "title": "Demonstrated skill conflicts with formal-credit policy",
        "level": "postgraduate",
        "kind": "competency_credit_conflict",
        "rarity": "rare",
        "results": [
            ("Practical competency", "satisfied"),
            ("Academic credit recognition", "external_requirement"),
        ],
        "steps": [("review", "Institutional evidence-policy review")],
        "guardrails": [
            "Keep demonstrated competency separate from credit recognition.",
            "Never convert a certificate into academic credit.",
        ],
        "variants": [
            (
                "Economics degree plus Python MOOC",
                "Analytics postgraduate programme",
                "India",
            ),
            ("Self-taught web portfolio", "MCA prerequisite review", "India"),
            ("Industry CAD certification", "Mechanical degree lateral entry", "India"),
            ("Community health experience", "Public Health master's", "India"),
        ],
    },
    {
        "code": "accessibility",
        "title": "Assessment accessibility mistaken for a learning gap",
        "level": "school",
        "kind": "accessibility_not_mastery",
        "rarity": "rare",
        "results": [
            ("Subject competency", "satisfied"),
            ("Accessible delivery support", "partial"),
        ],
        "steps": [("review", "Accessibility support review")],
        "guardrails": [
            "Do not diagnose a disability.",
            "Compare equivalent accessible and standard-format evidence.",
        ],
        "variants": [
            (
                "Dense visual mathematics worksheet",
                "Structured accessible mathematics assessment",
                "India",
            ),
            ("Audio-only language exercise", "Captioned language assessment", "India"),
            (
                "Timed handwritten science test",
                "Approved accessible-format science test",
                "India",
            ),
            (
                "Colour-dependent geography chart",
                "Pattern-labelled geography chart",
                "India",
            ),
        ],
    },
    {
        "code": "regulatory",
        "title": "Academic comparison reaches a regulated-profession boundary",
        "level": "professional",
        "kind": "regulated_profession_boundary",
        "rarity": "boundary",
        "results": [
            ("Academic foundation", "partial"),
            ("Professional eligibility", "external_requirement"),
        ],
        "steps": [
            ("verify", "Collect destination-specific academic evidence"),
            ("review", "Refer to authorised regulator"),
        ],
        "guardrails": [
            "Never claim licensing eligibility.",
            "Keep educational guidance separate from regulatory approval.",
        ],
        "variants": [
            ("Indian pharmacy degree", "Overseas pharmacist pathway", "International"),
            ("Indian nursing degree", "Overseas nursing registration", "International"),
            (
                "Indian architecture degree",
                "Foreign architect registration",
                "International",
            ),
            ("Indian law degree", "Foreign legal-practice pathway", "International"),
        ],
    },
    {
        "code": "conflicting-records",
        "title": "Records conflict across transcript, syllabus and learner statement",
        "level": "undergraduate",
        "kind": "conflicting_evidence",
        "rarity": "rare",
        "results": [
            ("Record consistency", "uncertain"),
            ("Destination competency", "uncertain"),
        ],
        "steps": [
            ("verify", "Resolve evidence conflict with issuing institution"),
            ("diagnose", "Measure readiness without claiming equivalence"),
        ],
        "guardrails": [
            "Do not choose the most favourable document silently.",
            "Expose conflicting evidence to human review.",
        ],
        "variants": [
            (
                "Transcript shows 4 credits; syllabus shows 2",
                "Statistics requirement",
                "India",
            ),
            (
                "Course code reused for different subjects",
                "Programming requirement",
                "India",
            ),
            (
                "Grade sheet and certificate dates conflict",
                "Lateral-entry review",
                "India",
            ),
            (
                "Translated syllabus differs from original",
                "International prerequisite review",
                "International",
            ),
        ],
    },
    {
        "code": "lateral-entry",
        "title": "Transferred credits do not prove destination readiness",
        "level": "undergraduate",
        "kind": "lateral_entry",
        "rarity": "common",
        "results": [
            ("Practical credits", "satisfied"),
            ("Theory prerequisite depth", "partial"),
        ],
        "steps": [
            ("diagnose", "Destination-depth diagnostic"),
            ("learn", "Focused theory bridge"),
        ],
        "guardrails": ["Credit acceptance and present readiness are separate facts."],
        "variants": [
            (
                "Mechanical engineering diploma",
                "Second-year B.Tech Mechanical",
                "India",
            ),
            ("Computer engineering diploma", "Second-year B.Tech CSE", "India"),
            ("Civil engineering diploma", "Second-year B.Tech Civil", "India"),
            (
                "Electrical engineering diploma",
                "Second-year B.Tech Electrical",
                "India",
            ),
        ],
    },
    {
        "code": "practice-theory",
        "title": "Strong practical performance with weak theory evidence",
        "level": "undergraduate",
        "kind": "practice_theory_mismatch",
        "rarity": "uncommon",
        "results": [
            ("Practical competency", "satisfied"),
            ("Theory explanation", "partial"),
        ],
        "steps": [
            ("diagnose", "Oral and written theory diagnostic"),
            ("practice", "Evidence-backed concept explanation"),
        ],
        "guardrails": [
            "Do not discard practical evidence.",
            "Do not infer theoretical mastery from task completion alone.",
        ],
        "variants": [
            (
                "Experienced laboratory technician",
                "B.Sc. laboratory science entry",
                "India",
            ),
            (
                "Working software developer",
                "Computer science degree continuation",
                "India",
            ),
            ("Experienced farm practitioner", "Agriculture diploma entry", "India"),
            ("Industrial electrician", "Electrical engineering diploma", "India"),
        ],
    },
]

CATEGORY_BY_KIND = {
    "same_standard_ready": "school-change",
    "mastery_not_curriculum": "school-change",
    "language_access": "language",
    "curriculum_sequence": "school-change",
    "learning_interruption": "learning-break",
    "study_abroad_documents": "study-abroad",
    "regulated_profession_boundary": "study-abroad",
}


def build_scenarios():
    scenarios = []
    number = 1
    for archetype in ARCHETYPES:
        for variant_number, (source, destination, location) in enumerate(
            archetype["variants"], 1
        ):
            scenario_id = f"S{number:03d}"
            evidence = []
            results = []
            requirements = []
            for result_number, (name, status) in enumerate(archetype["results"], 1):
                requirement_id = f"{scenario_id.lower()}-r{result_number}"
                evidence_id = f"{scenario_id.lower()}-e{result_number}"
                requirements.append(
                    {
                        "requirement_id": requirement_id,
                        "name": name,
                        "type": "document"
                        if status == "document_required"
                        else "external"
                        if status == "external_requirement"
                        else "academic",
                        "mandatory": True,
                    }
                )
                evidence_ids = []
                if status not in {
                    "missing",
                    "document_required",
                    "external_requirement",
                }:
                    evidence.append(
                        {
                            "evidence_id": evidence_id,
                            "type": "reviewed_demo_evidence",
                            "verified": status != "uncertain",
                            "competencies": [name.lower().replace(" ", "-")],
                            "synthetic": True,
                        }
                    )
                    evidence_ids = [evidence_id]
                results.append(
                    {
                        "requirement_id": requirement_id,
                        "status": status,
                        "reason": REASONS[status],
                        "evidence_ids": evidence_ids,
                        "requires_human_review": status
                        in {"uncertain", "external_requirement"},
                    }
                )

            scenarios.append(
                {
                    "scenario_id": scenario_id,
                    "title": f"{archetype['title']}: {destination}",
                    "description": f"{source} to {destination}. This {archetype['rarity']} scenario tests {archetype['kind'].replace('_', ' ')}.",
                    "education_level": archetype["level"],
                    "case_type": archetype["kind"],
                    "rarity": archetype["rarity"],
                    "learner": {
                        "name": f"{NAMES[number - 1]} Demo",
                        "preferred_language": "hi" if number % 4 == 0 else "en",
                        "context": f"Synthetic variant {variant_number} for {archetype['code']}",
                    },
                    "source_program": {"name": source, "location": location},
                    "destination_program": {"name": destination, "location": location},
                    "learner_evidence": evidence,
                    "destination_requirements": requirements,
                    "expected_results": results,
                    "expected_roadmap": [
                        {
                            "order": order,
                            "action": action,
                            "title": title,
                            "reason": f"Required by the {archetype['code']} decision pattern.",
                        }
                        for order, (action, title) in enumerate(archetype["steps"], 1)
                    ],
                    "source_documents": [],
                    "guardrails": archetype["guardrails"],
                    "tags": [
                        archetype["code"],
                        archetype["rarity"],
                        archetype["level"],
                    ],
                    "synthetic_fields": [
                        "learner identity",
                        "evidence records",
                        "results",
                    ],
                    "review_status": "reviewed_demo"
                    if archetype["code"]
                    in {"same-ready", "same-mastery", "language", "sequence"}
                    else "illustrative",
                    "is_active": True,
                }
            )
            number += 1
    return scenarios


def validate_scenarios(scenarios):
    if len(scenarios) < 50:
        raise ValueError(
            "The demonstration dataset must contain at least 50 scenarios."
        )

    scenario_ids = [item["scenario_id"] for item in scenarios]
    if len(scenario_ids) != len(set(scenario_ids)):
        raise ValueError("Scenario IDs must be unique.")

    allowed_statuses = set(REASONS)
    for scenario in scenarios:
        requirement_ids = {
            item["requirement_id"] for item in scenario["destination_requirements"]
        }
        evidence_ids = {item["evidence_id"] for item in scenario["learner_evidence"]}
        result_ids = {item["requirement_id"] for item in scenario["expected_results"]}
        if requirement_ids != result_ids:
            raise ValueError(
                f"{scenario['scenario_id']} must have exactly one result per requirement."
            )
        for result_item in scenario["expected_results"]:
            if result_item["status"] not in allowed_statuses:
                raise ValueError(
                    f"{scenario['scenario_id']} has an unsupported result status."
                )
            if not set(result_item["evidence_ids"]).issubset(evidence_ids):
                raise ValueError(
                    f"{scenario['scenario_id']} references unknown evidence."
                )


@transaction.atomic
def seed():
    from map.models import SupportCase, TransitionScenario
    from map.rag_pipeline import upsert_scenario_evidence

    call_command("seed_gapmap_demo", verbosity=0)
    scenarios = build_scenarios()
    validate_scenarios(scenarios)

    for data in scenarios:
        transition, _ = TransitionScenario.objects.update_or_create(
            scenario_id=data["scenario_id"],
            defaults={
                key: value for key, value in data.items() if key != "scenario_id"
            },
        )

        upsert_scenario_evidence(transition, data)
        statuses = [item["status"] for item in data["expected_results"]]
        priority = (
            "missing",
            "partial",
            "uncertain",
            "document_required",
            "external_requirement",
        )
        primary = next((item for item in priority if item in statuses), "satisfied")
        status, stage = STATUS_TO_PROGRESS[primary]
        kind = data["case_type"]
        category = CATEGORY_BY_KIND.get(
            kind,
            "higher-education"
            if data["education_level"]
            in {"undergraduate", "postgraduate", "professional"}
            else "unsure",
        )
        SupportCase.objects.update_or_create(
            reference=f"GM-{data['scenario_id']}",
            defaults={
                "title": data["title"],
                "requester_name": data["learner"]["name"],
                "requester_role": "student",
                "category": category,
                "summary": data["description"],
                "source_label": data["source_program"]["name"],
                "source_location": data["source_program"]["location"],
                "destination_label": data["destination_program"]["name"],
                "destination_location": data["destination_program"]["location"],
                "status": status,
                "progress_stage": stage,
                "is_demo": True,
            },
        )

    ids = [item["scenario_id"] for item in scenarios]
    return {
        "scenarios": TransitionScenario.objects.filter(scenario_id__in=ids).count(),
        "rare": TransitionScenario.objects.filter(
            scenario_id__in=ids, rarity="rare"
        ).count(),
        "boundary": TransitionScenario.objects.filter(
            scenario_id__in=ids, rarity="boundary"
        ).count(),
        "support_cases": SupportCase.objects.filter(
            reference__in=[f"GM-{item}" for item in ids]
        ).count(),
    }


if __name__ == "__main__":
    counts = seed()
    print("GapMap seed data is ready.")
    print(f"Transition scenarios: {counts['scenarios']}")
    print(f"Rare scenarios: {counts['rare']}")
    print(f"Guardrail-boundary scenarios: {counts['boundary']}")
    print(f"Linked support cases: {counts['support_cases']}")
