from decimal import Decimal

from django.core.management.base import BaseCommand

from map.models import (
    Concept,
    ConceptMapping,
    Curriculum,
    CurriculumConcept,
    DiagnosticItem,
    LearnerProfile,
    PrerequisiteEdge,
    SupportCase,
)


class Command(BaseCommand):
    help = "Create the small, reviewed dataset used in the GapMap hackathon demo."

    def handle(self, *args, **options):
        source, _ = Curriculum.objects.update_or_create(
            board="Maharashtra State Board",
            grade=8,
            subject="Mathematics",
            medium="Marathi",
            version="2026-demo",
            defaults={"source_url": "https://ebalbharati.in/"},
        )
        destination, _ = Curriculum.objects.update_or_create(
            board="CBSE",
            grade=9,
            subject="Mathematics",
            medium="English",
            version="2026-demo",
            defaults={"source_url": "https://ncert.nic.in/textbook.php"},
        )

        concept_data = {
            "number-sense": (
                "Signed number sense",
                "Compare signed numbers and interpret distance from zero.",
            ),
            "integer-operations": (
                "Integer operations",
                "Add and subtract positive and negative integers.",
            ),
            "ratio-proportion": (
                "Ratio and proportion",
                "Use proportional reasoning to determine an unknown quantity.",
            ),
            "algebraic-expressions": (
                "Algebraic expressions",
                "Combine like terms and apply the distributive property.",
            ),
            "linear-equations": (
                "Linear equations",
                "Solve one-variable linear equations while preserving equality.",
            ),
        }
        concepts = {}
        for code, (name, description) in concept_data.items():
            concepts[code], _ = Concept.objects.update_or_create(
                code=code, defaults={"name": name, "description": description}
            )

        source_codes = [
            "number-sense",
            "integer-operations",
            "ratio-proportion",
            "algebraic-expressions",
        ]
        for code in source_codes:
            CurriculumConcept.objects.update_or_create(
                curriculum=source,
                concept=concepts[code],
                defaults={
                    "local_term": concept_data[code][0],
                    "learning_outcome": concept_data[code][1],
                    "coverage_depth": 1,
                },
            )
        for code in concept_data:
            CurriculumConcept.objects.update_or_create(
                curriculum=destination,
                concept=concepts[code],
                defaults={
                    "local_term": concept_data[code][0],
                    "learning_outcome": concept_data[code][1],
                    "coverage_depth": 2 if code in {"algebraic-expressions", "linear-equations"} else 1,
                },
            )

        edges = [
            ("number-sense", "integer-operations", "Signed number sense supports reliable integer operations."),
            ("integer-operations", "algebraic-expressions", "Combining terms requires correct signed arithmetic."),
            ("ratio-proportion", "algebraic-expressions", "Proportional relationships prepare learners to express unknowns."),
            ("algebraic-expressions", "linear-equations", "Equation solving depends on simplifying expressions first."),
        ]
        for prerequisite, dependent, rationale in edges:
            PrerequisiteEdge.objects.update_or_create(
                curriculum=destination,
                prerequisite=concepts[prerequisite],
                dependent=concepts[dependent],
                defaults={
                    "rationale": rationale,
                    "approved": True,
                    "reviewed_by": "GapMap demo content",
                },
            )

        for code in source_codes:
            ConceptMapping.objects.update_or_create(
                source_curriculum=source,
                destination_curriculum=destination,
                source_concept=concepts[code],
                destination_concept=concepts[code],
                defaults={
                    "relation": "partial" if code == "algebraic-expressions" else "equivalent",
                    "confidence": Decimal("0.950"),
                    "rationale": "Demo mapping reviewed against the stated learning outcomes.",
                    "approved": True,
                },
            )
        ConceptMapping.objects.update_or_create(
            source_curriculum=source,
            destination_curriculum=destination,
            source_concept=None,
            destination_concept=concepts["linear-equations"],
            defaults={
                "relation": "missing",
                "confidence": Decimal("0.900"),
                "rationale": "The destination expects a deeper equation-solving outcome.",
                "approved": True,
            },
        )

        items = [
            ("linear-equations", "hi", "3x + 5 = 20 में x का मान क्या है?", ["3", "5", "8", "15"], "5", "दोनों तरफ से 5 घटाएँ, फिर 3 से भाग दें।", 1),
            ("linear-equations", "en", "Solve x / 2 - 3 = 4.", ["2", "8", "14", "16"], "14", "Add 3 to both sides, then multiply by 2.", 2),
            ("algebraic-expressions", "hi", "3a + 2a को सरल कीजिए।", ["5a", "6a", "5a²", "a"], "5a", "समान पदों के गुणांक जोड़ें।", 1),
            ("algebraic-expressions", "en", "Expand 2(x + 3).", ["2x + 3", "2x + 5", "2x + 6", "x + 6"], "2x + 6", "Distribute 2 to both terms inside the bracket.", 2),
            ("integer-operations", "hi", "-7 + 12 का मान क्या है?", ["-19", "-5", "5", "19"], "5", "12 में से 7 घटाने पर 5 बचता है।", 1),
            ("integer-operations", "en", "Calculate 6 - (-4).", ["2", "-2", "10", "-10"], "10", "Subtracting a negative is addition.", 2),
            ("ratio-proportion", "hi", "अनुपात 2:3 में पहली संख्या 8 है। दूसरी संख्या क्या है?", ["6", "10", "12", "16"], "12", "2 को 4 से गुणा किया गया है, इसलिए 3 को भी 4 से गुणा करें।", 1),
            ("ratio-proportion", "en", "Five pens cost ₹40. What do eight pens cost at the same rate?", ["₹48", "₹56", "₹64", "₹80"], "₹64", "One pen costs ₹8, so eight cost ₹64.", 2),
            ("number-sense", "hi", "कौन-सी संख्या बड़ी है: -3 या -8?", ["-8", "-3", "दोनों बराबर", "कह नहीं सकते"], "-3", "संख्या रेखा पर -3, -8 के दाईं ओर है।", 1),
            ("number-sense", "en", "What is the absolute value of -9?", ["-9", "0", "9", "18"], "9", "Absolute value is distance from zero.", 2),
        ]
        for code, language, prompt, choices, answer, explanation, difficulty in items:
            DiagnosticItem.objects.update_or_create(
                curriculum=destination,
                concept=concepts[code],
                prompt=prompt,
                defaults={
                    "language": language,
                    "options": choices,
                    "correct_answer": answer,
                    "explanation": explanation,
                    "difficulty": difficulty,
                    "approved": True,
                    "source_reference": "GapMap reviewed demo item",
                },
            )

        learner, _ = LearnerProfile.objects.update_or_create(
            display_name="Aarav Demo",
            defaults={
                "source_curriculum": source,
                "destination_curriculum": destination,
                "preferred_language": "hi",
            },
        )

        SupportCase.objects.update_or_create(
            reference="GM-2048",
            defaults={
                "title": "B.Pharm to Master of Data Science",
                "requester_name": "Ananya Rao",
                "requester_role": "student",
                "category": "study-abroad",
                "summary": "I completed B.Pharm in India and need to understand my academic readiness for a Master of Data Science programme.",
                "source_label": "PCI B.Pharm",
                "source_location": "India",
                "destination_label": "Master of Data Science",
                "destination_location": "UBC, Canada",
                "status": "gap_analysis",
                "progress_stage": 3,
                "is_demo": True,
            },
        )
        self.stdout.write(self.style.SUCCESS("GapMap demo data is ready."))
        self.stdout.write(f"Learner ID: {learner.id}")
        self.stdout.write(f"Recommended target ID: {concepts['linear-equations'].id}")
        self.stdout.write("Open /api/demo-context/ to discover IDs from the frontend.")
