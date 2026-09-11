"""Data transfer objects returned by the RAG pipeline."""

from dataclasses import dataclass

from ..models import EvidenceChunk


@dataclass(frozen=True)
class EmbeddingResult:
    vector: list[float]
    backend: str


@dataclass(frozen=True)
class RetrievalHit:
    chunk: EvidenceChunk
    score: float
    lexical_score: float
    vector_score: float
    matched_terms: list[str]
    retrieval_reasons: list[str]

    def as_dict(self):
        return {
            "chunk_id": self.chunk.chunk_id,
            "score": round(self.score, 4),
            "lexical_score": round(self.lexical_score, 4),
            "vector_score": round(self.vector_score, 4),
            "matched_terms": self.matched_terms,
            "retrieval_reasons": self.retrieval_reasons,
            "text": self.chunk.text,
            "section": self.chunk.section,
            "page": self.chunk.page,
            "metadata": self.chunk.metadata,
            "citation": {
                "source_id": self.chunk.source.source_id,
                "title": self.chunk.source.title,
                "organisation": self.chunk.source.organisation,
                "url": self.chunk.source.url,
                "version": self.chunk.source.version,
                "review_status": self.chunk.source.review_status,
            },
        }
