"""Explainable hybrid scoring for retrieved evidence chunks."""

from .embeddings import cosine_similarity, expand_terms, tokenize
from .types import RetrievalHit


def score_chunk(
    query,
    query_terms,
    query_embedding,
    query_embedding_model,
    chunk,
    database_vector_score=None,
):
    chunk_terms = expand_terms(tokenize(chunk.text) | set(chunk.canonical_terms))
    matched = sorted(query_terms & chunk_terms)
    lexical = len(matched) / max(1, len(query_terms))
    phrase = 1.0 if query.lower().strip() in chunk.text.lower() else 0.0
    code_match = (
        1.0
        if any("-" in term and term in chunk.text.lower() for term in query_terms)
        else 0.0
    )
    if chunk.embedding_model != query_embedding_model:
        vector = 0.0
    elif database_vector_score is not None:
        vector = database_vector_score
    else:
        vector = cosine_similarity(query_embedding, chunk.embedding)

    score = (0.48 * lexical) + (0.32 * vector) + (0.15 * phrase) + (0.05 * code_match)
    reasons = []
    if matched:
        reasons.append("matched canonical or query terms")
    if vector >= 0.45:
        reasons.append("similar Sentence Transformer representation")
    if phrase:
        reasons.append("exact phrase present")
    if code_match:
        reasons.append("course or competency code matched")
    if chunk.embedding_model != query_embedding_model:
        reasons.append("vector skipped because embedding models differ")
    return RetrievalHit(chunk, score, lexical, vector, matched, reasons)
