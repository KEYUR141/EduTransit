"""Sentence Transformer embeddings with an explicit offline fallback."""

import hashlib
import math
from functools import lru_cache

from django.conf import settings

from .config import EMBEDDING_DIMENSIONS, SYNONYMS, TOKEN_PATTERN
from .types import EmbeddingResult


def tokenize(text):
    return set(TOKEN_PATTERN.findall((text or "").lower()))


def expand_terms(tokens):
    expanded = set(tokens)
    for token in tokens:
        expanded.update(SYNONYMS.get(token, set()))
        for canonical, related in SYNONYMS.items():
            if token in related:
                expanded.add(canonical)
                expanded.update(related)
    return expanded


def hashed_embedding(text, dimensions=EMBEDDING_DIMENSIONS):
    """Return a deterministic fallback when the configured model is unavailable."""
    vector = [0.0] * dimensions
    for token in sorted(expand_terms(tokenize(text))):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign
    norm = math.sqrt(sum(value * value for value in vector))
    return [value / norm for value in vector] if norm else vector


@lru_cache(maxsize=1)
def _sentence_transformer_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(
        settings.RAG_EMBEDDING_MODEL,
        device=settings.RAG_EMBEDDING_DEVICE,
        local_files_only=settings.RAG_EMBEDDING_LOCAL_ONLY,
    )


def _encode_many(texts, task):
    texts = list(texts)
    if not texts:
        return []
    try:
        model = _sentence_transformer_model()
        encoder = model.encode_query if task == "query" else model.encode_document
        encoded = encoder(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        vectors = encoded.tolist()
        if any(len(vector) != EMBEDDING_DIMENSIONS for vector in vectors):
            raise ValueError(
                f"Embedding model output must have {EMBEDDING_DIMENSIONS} dimensions."
            )
        return [
            EmbeddingResult(vector, settings.RAG_EMBEDDING_MODEL) for vector in vectors
        ]
    except Exception as error:
        if not settings.RAG_ALLOW_EMBEDDING_FALLBACK:
            raise RuntimeError("Sentence Transformer embedding failed.") from error
        return [
            EmbeddingResult(hashed_embedding(text), "fallback-hash-v1")
            for text in texts
        ]


def embed_query(text):
    return _encode_many([text], "query")[0]


def embed_document(text):
    return _encode_many([text], "document")[0]


def embed_documents(texts):
    return _encode_many(texts, "document")


def cosine_similarity(left, right):
    if not left or not right:
        return 0.0
    return max(
        0.0,
        min(1.0, sum(float(a) * float(b) for a, b in zip(left, right))),
    )
