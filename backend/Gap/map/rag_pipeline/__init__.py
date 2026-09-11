"""Public interface for the GapMap retrieval-augmented generation pipeline."""

from .embeddings import (
    embed_document,
    embed_documents,
    embed_query,
    hashed_embedding,
)
from .ingestion import build_scenario_chunk_records, upsert_scenario_evidence
from .retrieval import retrieve_evidence

__all__ = [
    "build_scenario_chunk_records",
    "embed_document",
    "embed_documents",
    "embed_query",
    "hashed_embedding",
    "retrieve_evidence",
    "upsert_scenario_evidence",
]
