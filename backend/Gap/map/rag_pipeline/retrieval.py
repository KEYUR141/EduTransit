"""Scenario-scoped and new-case hybrid retrieval backed by pgvector."""

from collections import defaultdict

from django.db import connection
from pgvector.django import CosineDistance

from ..models import EvidenceChunk, TransitionScenario
from .confidence import assess_confidence
from .config import MAX_CANDIDATES
from .embeddings import embed_query, expand_terms, tokenize
from .guardrails import approved_evidence_queryset, chunk_integrity_valid
from .scoring import score_chunk


def _rank_candidates(queryset, embedding_result):
    candidates = list(queryset[:MAX_CANDIDATES])
    database_scores = {}
    if connection.vendor == "postgresql":
        ranked = list(
            queryset.filter(embedding_model=embedding_result.backend)
            .exclude(embedding__isnull=True)
            .annotate(
                vector_distance=CosineDistance("embedding", embedding_result.vector)
            )
            .order_by("vector_distance")[:MAX_CANDIDATES]
        )
        by_id = {chunk.pk: chunk for chunk in candidates}
        by_id.update({chunk.pk: chunk for chunk in ranked})
        candidates = list(by_id.values())
        for chunk in ranked:
            database_scores[chunk.pk] = max(
                0.0, min(1.0, 1.0 - float(chunk.vector_distance))
            )
    return candidates, database_scores


def _score_candidates(query, query_terms, embedding_result, candidates, db_scores):
    valid = [chunk for chunk in candidates if chunk_integrity_valid(chunk)]
    hits = [
        score_chunk(
            query,
            query_terms,
            embedding_result.vector,
            embedding_result.backend,
            chunk,
            db_scores.get(chunk.pk),
        )
        for chunk in valid
    ]
    hits = [hit for hit in hits if hit.score > 0]
    hits.sort(key=lambda hit: (-hit.score, hit.chunk.chunk_id))
    return hits


def _discover_scenario(hits):
    grouped = defaultdict(list)
    for hit in hits:
        if hit.chunk.scenario_id:
            grouped[hit.chunk.scenario_id].append(hit)
    ranked = []
    for scenario_pk, scenario_hits in grouped.items():
        scores = [hit.score for hit in scenario_hits[:3]]
        group_score = scores[0] + (0.15 * sum(scores[1:]))
        ranked.append((group_score, scenario_pk, scenario_hits))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    if not ranked:
        return None, hits, 0.0
    best_score, scenario_pk, scenario_hits = ranked[0]
    second_score = ranked[1][0] if len(ranked) > 1 else 0.0
    scenario = TransitionScenario.objects.get(pk=scenario_pk)
    return scenario, scenario_hits, max(0.0, best_score - second_score)


def retrieve_evidence(*, query, scenario_id=None, top_k=5):
    query = (query or "").strip()
    if len(query) < 3:
        raise ValueError("Query must contain at least 3 characters.")
    top_k = max(1, min(int(top_k), 10))
    discovery_mode = not scenario_id

    scenario = None
    if scenario_id:
        try:
            scenario = TransitionScenario.objects.get(
                scenario_id=scenario_id, is_active=True
            )
        except TransitionScenario.DoesNotExist as error:
            raise ValueError("Unknown or inactive scenario.") from error

    query_terms = expand_terms(tokenize(query))
    embedding_result = embed_query(query)
    queryset = EvidenceChunk.objects.filter(scenario__is_active=True)
    if scenario:
        queryset = queryset.filter(scenario=scenario)
    queryset = approved_evidence_queryset(queryset).select_related("source", "scenario")

    candidates, database_scores = _rank_candidates(queryset, embedding_result)
    hits = _score_candidates(
        query, query_terms, embedding_result, candidates, database_scores
    )
    discovery_margin = 0.0
    if discovery_mode:
        scenario, hits, discovery_margin = _discover_scenario(hits)

    assessment = assess_confidence(
        hits=hits,
        query_terms=query_terms,
        scenario=scenario,
        discovery_margin=discovery_margin,
    )
    if discovery_mode and assessment["confidence"]["level"] == "low":
        matched_scenario = None
        assessment["review"]["required"] = True
        assessment["review"]["route"] = "instructor_review"
    else:
        matched_scenario = scenario

    return {
        "query": query,
        "scenario_id": scenario.scenario_id
        if scenario and not discovery_mode
        else None,
        "discovery_mode": discovery_mode,
        "matched_scenario": (
            {
                "scenario_id": matched_scenario.scenario_id,
                "title": matched_scenario.title,
                "rarity": matched_scenario.rarity,
            }
            if matched_scenario
            else None
        ),
        "retrieval_mode": (
            "hybrid_pgvector" if connection.vendor == "postgresql" else "hybrid_offline"
        ),
        "embedding_backend": embedding_result.backend,
        **assessment,
        "guardrails": {
            "scenario_scope_enforced": not discovery_mode,
            "cross_scenario_discovery": discovery_mode,
            "approved_chunks_only": True,
            "integrity_checksum_verified": True,
            "embedding_model_match_enforced": True,
            "maximum_results": 10,
            "model_decision_allowed": False,
        },
        "count": min(len(hits), top_k),
        "results": [hit.as_dict() for hit in hits[:top_k]],
    }
