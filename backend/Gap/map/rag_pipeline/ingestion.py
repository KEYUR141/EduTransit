"""Build, embed, and persist evidence chunks for a transition scenario."""

import hashlib
import json

from ..models import AcademicSource, EvidenceChunk
from .embeddings import embed_documents


def build_scenario_chunk_records(data):
    """Create auditable chunk records from one validated scenario dictionary."""
    context_text = (
        f"Source programme: {data['source_program']['name']}. "
        f"Destination programme: {data['destination_program']['name']}. "
        f"Situation: {data['description']}"
    )
    records = [
        (
            "context",
            context_text,
            ["transition", data["case_type"], data["education_level"]],
            {"kind": "transition_context"},
        )
    ]
    for evidence in data["learner_evidence"]:
        records.append(
            (
                evidence["evidence_id"],
                "Learner evidence: " + json.dumps(evidence, sort_keys=True),
                evidence.get("competencies", []),
                {"kind": "learner_evidence", "evidence_id": evidence["evidence_id"]},
            )
        )

    results_by_requirement = {
        item["requirement_id"]: item for item in data["expected_results"]
    }
    for requirement in data["destination_requirements"]:
        decision = results_by_requirement[requirement["requirement_id"]]
        requirement_text = (
            f"Destination requirement: {requirement['name']}. "
            f"Expected guarded result: {decision['status']}. "
            f"Reason: {decision['reason']}"
        )
        records.append(
            (
                requirement["requirement_id"],
                requirement_text,
                [
                    requirement["name"].lower().replace(" ", "-"),
                    decision["status"],
                ],
                {
                    "kind": "destination_requirement",
                    "requirement_id": requirement["requirement_id"],
                    "expected_status": decision["status"],
                },
            )
        )
    return records


def upsert_scenario_evidence(transition, data):
    """Embed and idempotently store all RAG evidence for one scenario."""
    source, _ = AcademicSource.objects.update_or_create(
        source_id=f"fixture-{data['scenario_id'].lower()}",
        defaults={
            "title": f"{data['title']} reviewed demonstration evidence",
            "organisation": "GapMap prototype dataset",
            "source_type": "synthetic_fixture",
            "version": "2026-demo",
            "review_status": (
                "reviewed"
                if data["review_status"] == "reviewed_demo"
                else "illustrative"
            ),
        },
    )
    records = build_scenario_chunk_records(data)
    embeddings = embed_documents(record[1] for record in records)
    for (suffix, text, terms, metadata), embedding in zip(
        records, embeddings, strict=True
    ):
        EvidenceChunk.objects.update_or_create(
            chunk_id=f"{data['scenario_id'].lower()}-{suffix}",
            defaults={
                "source": source,
                "scenario": transition,
                "section": metadata["kind"],
                "text": text,
                "canonical_terms": terms,
                "metadata": {**metadata, "synthetic": True},
                "embedding": embedding.vector,
                "embedding_model": embedding.backend,
                "checksum": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "approved": True,
            },
        )
    return len(records)
