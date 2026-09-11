import hashlib

from rest_framework import status
from rest_framework.test import APITestCase

from .models import AcademicSource, EvidenceChunk, TransitionScenario
from .rag_pipeline import hashed_embedding


class RagRetrievalApiTests(APITestCase):
    def setUp(self):
        base = {
            "description": "Synthetic retrieval test",
            "education_level": "postgraduate",
            "case_type": "cross_domain",
            "rarity": "uncommon",
            "learner": {"name": "Demo Learner"},
            "source_program": {"name": "B.Pharm"},
            "destination_program": {"name": "Data Science"},
            "learner_evidence": [],
            "destination_requirements": [],
            "expected_results": [],
            "expected_roadmap": [],
            "source_documents": [],
            "guardrails": [],
            "tags": [],
            "synthetic_fields": ["all"],
            "review_status": "reviewed_demo",
        }
        self.scenario = TransitionScenario.objects.create(
            scenario_id="RAG01", title="Pharmacy to data science", **base
        )
        other = TransitionScenario.objects.create(
            scenario_id="RAG02", title="Unrelated transition", **base
        )
        source = AcademicSource.objects.create(
            source_id="rag-reviewed",
            title="Reviewed programme evidence",
            organisation="GapMap tests",
            source_type="reviewed_fixture",
            review_status="reviewed",
        )
        unreviewed = AcademicSource.objects.create(
            source_id="rag-proposed",
            title="Unreviewed evidence",
            organisation="GapMap tests",
            source_type="reviewed_fixture",
            review_status="proposed",
        )
        self._chunk(
            "programming",
            source,
            self.scenario,
            "Destination requires Python programming foundations and data structures.",
            ["programming", "python", "data-structures"],
        )
        self._chunk(
            "statistics",
            source,
            self.scenario,
            (
                "Verified biostatistics covers probability, regression and "
                "hypothesis testing."
            ),
            ["statistics", "probability", "regression"],
        )
        self._chunk(
            "other-scenario",
            source,
            other,
            "Advanced Python programming and algorithms.",
            ["programming", "python"],
        )
        self._chunk(
            "unapproved-chunk",
            source,
            self.scenario,
            "Python programming evidence that has not been approved.",
            ["programming", "python"],
            approved=False,
        )
        self._chunk(
            "unreviewed-source",
            unreviewed,
            self.scenario,
            "Python programming evidence from a proposed source.",
            ["programming", "python"],
        )

    @staticmethod
    def _chunk(chunk_id, source, scenario, text, terms, approved=True):
        return EvidenceChunk.objects.create(
            chunk_id=chunk_id,
            source=source,
            scenario=scenario,
            section="test",
            text=text,
            canonical_terms=terms,
            embedding=hashed_embedding(text),
            embedding_model="fallback-hash-v1",
            checksum=hashlib.sha256(text.encode("utf-8")).hexdigest(),
            approved=approved,
        )

    def test_retrieval_is_ranked_cited_and_scenario_scoped(self):
        response = self.client.post(
            "/api/rag/retrieve/",
            {
                "query": "Do I have Python programming foundations?",
                "scenario_id": self.scenario.scenario_id,
                "top_k": 10,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        chunk_ids = [item["chunk_id"] for item in response.data["results"]]
        self.assertEqual(chunk_ids[0], "programming")
        self.assertNotIn("other-scenario", chunk_ids)
        self.assertNotIn("unapproved-chunk", chunk_ids)
        self.assertNotIn("unreviewed-source", chunk_ids)
        self.assertTrue(response.data["guardrails"]["scenario_scope_enforced"])
        self.assertTrue(response.data["guardrails"]["approved_chunks_only"])
        self.assertEqual(
            response.data["results"][0]["citation"]["source_id"], "rag-reviewed"
        )

    def test_unknown_scenario_and_oversized_top_k_are_rejected(self):
        missing = self.client.post(
            "/api/rag/retrieve/",
            {"query": "programming", "scenario_id": "MISSING", "top_k": 3},
            format="json",
        )
        oversized = self.client.post(
            "/api/rag/retrieve/",
            {"query": "programming", "scenario_id": "RAG01", "top_k": 50},
            format="json",
        )

        self.assertEqual(missing.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(oversized.status_code, status.HTTP_400_BAD_REQUEST)

    def test_response_exposes_confidence_and_instructor_route(self):
        self.scenario.rarity = "boundary"
        self.scenario.save(update_fields=["rarity"])

        response = self.client.post(
            "/api/rag/retrieve/",
            {
                "query": "Python programming foundations",
                "scenario_id": self.scenario.scenario_id,
                "top_k": 3,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertIn(response.data["confidence"]["level"], {"high", "medium", "low"})
        self.assertFalse(response.data["confidence"]["is_eligibility_probability"])
        self.assertTrue(response.data["review"]["required"])
        self.assertEqual(response.data["review"]["route"], "specialist_escalation")
        self.assertIn(
            "regulated_or_policy_boundary", response.data["review"]["reason_codes"]
        )

    def test_missing_scenario_enters_dynamic_discovery_mode(self):
        response = self.client.post(
            "/api/rag/retrieve/",
            {"query": "B.Pharm student needs Python programming", "top_k": 3},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertTrue(response.data["discovery_mode"])
        self.assertIsNone(response.data["scenario_id"])
        self.assertTrue(response.data["guardrails"]["cross_scenario_discovery"])
        self.assertFalse(response.data["guardrails"]["scenario_scope_enforced"])
        self.assertIn("confidence", response.data)
        self.assertIn("review", response.data)
