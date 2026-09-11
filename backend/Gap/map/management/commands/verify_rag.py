"""Verify persisted embeddings, guardrails, index, and live retrieval."""

import hashlib

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from map.models import EvidenceChunk, TransitionScenario
from map.rag_pipeline import retrieve_evidence


class Command(BaseCommand):
    help = "Run an end-to-end health check of the persisted RAG pipeline."

    def handle(self, *args, **options):
        chunks = list(EvidenceChunk.objects.select_related("source"))
        if not chunks:
            raise CommandError("No evidence chunks exist. Run seed_data.py first.")

        expected_model = settings.RAG_EMBEDDING_MODEL
        failures = {
            "missing_vectors": sum(chunk.embedding is None for chunk in chunks),
            "wrong_dimensions": sum(
                chunk.embedding is not None and len(chunk.embedding) != 384
                for chunk in chunks
            ),
            "wrong_model": sum(
                chunk.embedding_model != expected_model for chunk in chunks
            ),
            "invalid_checksums": sum(
                hashlib.sha256(chunk.text.encode("utf-8")).hexdigest() != chunk.checksum
                for chunk in chunks
            ),
            "unapproved_chunks": sum(not chunk.approved for chunk in chunks),
        }
        if any(failures.values()):
            raise CommandError(f"RAG data verification failed: {failures}")

        scenario_ids = ["S001", "S021", "S029", "S045"]
        available = set(
            TransitionScenario.objects.filter(scenario_id__in=scenario_ids).values_list(
                "scenario_id", flat=True
            )
        )
        queries = {
            "S001": "mathematics readiness and prerequisites",
            "S021": "programming statistics data science prerequisites",
            "S029": "ambiguous course title programming evidence",
            "S045": "overseas pharmacist registration requirement",
        }
        for scenario_id in scenario_ids:
            if scenario_id not in available:
                continue
            result = retrieve_evidence(
                query=queries[scenario_id], scenario_id=scenario_id, top_k=3
            )
            if not result["results"]:
                raise CommandError(f"No retrieval results for {scenario_id}.")
            first = result["results"][0]
            self.stdout.write(
                f"{scenario_id}: {result['retrieval_mode']} -> "
                f"{first['chunk_id']} ({first['citation']['source_id']})"
            )

        index_present = connection.vendor != "postgresql"
        if connection.vendor == "postgresql":
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM pg_indexes WHERE tablename = %s AND indexname = %s",
                    ["map_evidencechunk", "map_evidence_embedding_hnsw"],
                )
                index_present = cursor.fetchone() is not None
        if not index_present:
            raise CommandError("The PostgreSQL HNSW embedding index is missing.")

        self.stdout.write(
            self.style.SUCCESS(
                f"RAG verified: {len(chunks)} vectors, 384 dimensions, "
                f"model={expected_model}, database={connection.vendor}, "
                f"hnsw_index={index_present}."
            )
        )
