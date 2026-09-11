"""Rebuild the pgvector embeddings stored on evidence chunks."""

import hashlib

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from map.models import EvidenceChunk
from map.rag_pipeline import embed_documents


class Command(BaseCommand):
    help = "Generate Sentence Transformer embeddings and store them in pgvector."

    def add_arguments(self, parser):
        parser.add_argument(
            "--scenario",
            help="Rebuild only one TransitionScenario scenario_id.",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=32,
            help="Documents encoded per batch (default: 32).",
        )
        parser.add_argument(
            "--only-missing",
            action="store_true",
            help="Skip chunks that already have an embedding and model identifier.",
        )

    def handle(self, *args, **options):
        batch_size = options["batch_size"]
        if not 1 <= batch_size <= 256:
            raise CommandError("--batch-size must be between 1 and 256.")

        queryset = EvidenceChunk.objects.order_by("pk")
        scenario_id = options.get("scenario")
        if scenario_id:
            queryset = queryset.filter(scenario__scenario_id=scenario_id)
            if not queryset.exists():
                raise CommandError(
                    f"No evidence chunks found for scenario {scenario_id}."
                )
        if options["only_missing"]:
            queryset = queryset.filter(
                Q(embedding__isnull=True) | Q(embedding_model="")
            )

        total = queryset.count()
        if total == 0:
            self.stdout.write(self.style.SUCCESS("No embeddings need rebuilding."))
            return

        rebuilt = 0
        batch = []
        for chunk in queryset.iterator(chunk_size=batch_size):
            batch.append(chunk)
            if len(batch) == batch_size:
                rebuilt += self._persist_batch(batch)
                batch = []
                self.stdout.write(f"Embedded {rebuilt}/{total} chunks")
        if batch:
            rebuilt += self._persist_batch(batch)

        self.stdout.write(
            self.style.SUCCESS(f"Stored {rebuilt} embeddings in the database.")
        )

    @staticmethod
    def _persist_batch(chunks):
        results = embed_documents(chunk.text for chunk in chunks)
        updated_at = timezone.now()
        for chunk, result in zip(chunks, results, strict=True):
            chunk.embedding = result.vector
            chunk.embedding_model = result.backend
            chunk.checksum = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()
            chunk.updated_at = updated_at
        with transaction.atomic():
            EvidenceChunk.objects.bulk_update(
                chunks,
                ["embedding", "embedding_model", "checksum", "updated_at"],
            )
        return len(chunks)
