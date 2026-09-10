from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Concept, DiagnosticItem, LearnerProfile, SupportCase


class GapMapPrototypeApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_gapmap_demo", verbosity=0)
        cls.learner = LearnerProfile.objects.get(display_name="Aarav Demo")
        cls.target = Concept.objects.get(code="linear-equations")

    def create_session(self, max_questions=6):
        response = self.client.post(
            "/api/diagnostic-sessions/",
            {
                "learner": self.learner.id,
                "target_concept": self.target.id,
                "max_questions": max_questions,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        return response.data["id"]

    def test_health_and_demo_context_are_frontend_ready(self):
        health = self.client.get("/api/health/")
        context = self.client.get("/api/demo-context/")

        self.assertEqual(health.status_code, status.HTTP_200_OK)
        self.assertEqual(health.data["status"], "ok")
        self.assertEqual(context.status_code, status.HTTP_200_OK)
        self.assertEqual(context.data["learner"]["id"], self.learner.id)
        self.assertEqual(context.data["recommended_target_code"], "linear-equations")

    def test_wrong_target_answer_moves_to_nearest_prerequisite(self):
        session_id = self.create_session()
        first = self.client.get(f"/api/diagnostic-sessions/{session_id}/next-question/")
        self.assertEqual(first.data["question"]["concept_name"], "Linear equations")
        self.assertEqual(first.data["question"]["language"], "hi")

        answer = self.client.post(
            f"/api/diagnostic-sessions/{session_id}/answer/",
            {"item_id": first.data["question"]["id"], "answer": "3", "response_time_ms": 4200},
            format="json",
        )

        self.assertEqual(answer.status_code, status.HTTP_201_CREATED, answer.data)
        self.assertFalse(answer.data["attempt"]["is_correct"])
        self.assertEqual(answer.data["next_question"]["concept_name"], "Algebraic expressions")

        gap = self.client.get(f"/api/diagnostic-sessions/{session_id}/gap-map/")
        target_node = next(node for node in gap.data["nodes"] if node["is_target"])
        self.assertEqual(target_node["status"], "gap")
        self.assertEqual(target_node["evidence_count"], 1)

    def test_bridge_plan_contains_only_evidenced_gaps_in_dependency_order(self):
        session_id = self.create_session()
        target_question = self.client.get(
            f"/api/diagnostic-sessions/{session_id}/next-question/"
        ).data["question"]
        algebra_question = self.client.post(
            f"/api/diagnostic-sessions/{session_id}/answer/",
            {"item_id": target_question["id"], "answer": "wrong"},
            format="json",
        ).data["next_question"]
        next_answer = self.client.post(
            f"/api/diagnostic-sessions/{session_id}/answer/",
            {"item_id": algebra_question["id"], "answer": "wrong"},
            format="json",
        )
        self.assertEqual(next_answer.data["next_question"]["concept_name"], "Integer operations")

        response = self.client.post(f"/api/diagnostic-sessions/{session_id}/bridge-plan/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(
            [step["concept_code"] for step in response.data["steps"]],
            ["algebraic-expressions", "linear-equations"],
        )
        self.assertTrue(all(step["activity"] for step in response.data["steps"]))
        self.assertTrue(all(step["evidence_prompt"] for step in response.data["steps"]))

    def test_rejects_repeated_or_wrong_curriculum_items(self):
        session_id = self.create_session()
        question = self.client.get(
            f"/api/diagnostic-sessions/{session_id}/next-question/"
        ).data["question"]
        first = self.client.post(
            f"/api/diagnostic-sessions/{session_id}/answer/",
            {"item_id": question["id"], "answer": "wrong"},
            format="json",
        )
        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        duplicate = self.client.post(
            f"/api/diagnostic-sessions/{session_id}/answer/",
            {"item_id": question["id"], "answer": "wrong"},
            format="json",
        )
        self.assertEqual(duplicate.status_code, status.HTTP_400_BAD_REQUEST)

        source_item = DiagnosticItem.objects.create(
            curriculum=self.learner.source_curriculum,
            concept=self.target,
            prompt="Source-only item",
            options=["a", "b"],
            correct_answer="a",
            approved=True,
        )
        wrong_curriculum = self.client.post(
            f"/api/diagnostic-sessions/{session_id}/answer/",
            {"item_id": source_item.id, "answer": "a"},
            format="json",
        )
        self.assertEqual(wrong_curriculum.status_code, status.HTTP_400_BAD_REQUEST)

class SupportCaseApiTests(APITestCase):
    def test_creates_and_lists_a_support_case(self):
        created = self.client.post(
            "/api/support-cases/",
            {
                "title": "Help with a programme transition",
                "requester_name": "Demo Student",
                "requester_role": "student",
                "category": "study-abroad",
                "summary": "I need help comparing my completed programme with a destination course.",
                "source_label": "Current programme",
                "source_location": "India",
                "destination_label": "Destination programme",
                "destination_location": "Canada",
            },
            format="json",
        )

        self.assertEqual(created.status_code, status.HTTP_201_CREATED, created.data)
        self.assertTrue(created.data["reference"].startswith("GM-"))
        self.assertEqual(created.data["status"], "received")
        self.assertEqual(created.data["progress_stage"], 1)
        self.assertFalse(created.data["is_demo"])

        listed = self.client.get("/api/support-cases/")
        self.assertEqual(listed.status_code, status.HTTP_200_OK)
        self.assertEqual(listed.data["count"], 1)
        self.assertEqual(listed.data["results"][0]["id"], SupportCase.objects.get().id)

    def test_rejects_an_unhelpfully_short_summary(self):
        response = self.client.post(
            "/api/support-cases/",
            {
                "requester_role": "student",
                "category": "unsure",
                "summary": "Need help",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("summary", response.data)
