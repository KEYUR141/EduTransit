"""Transparent confidence signals and human-review routing."""


def assess_confidence(*, hits, query_terms, scenario=None, discovery_margin=0.0):
    top_score = hits[0].score if hits else 0.0
    matched_terms = set()
    for hit in hits[:3]:
        matched_terms.update(hit.matched_terms)
    term_coverage = len(matched_terms & query_terms) / max(1, len(query_terms))
    evidence_support = min(len(hits) / 3, 1.0)
    margin_strength = min(max(discovery_margin, 0.0) / 0.25, 1.0)
    score = min(
        1.0,
        (0.45 * top_score)
        + (0.30 * term_coverage)
        + (0.15 * evidence_support)
        + (0.10 * margin_strength),
    )

    if score >= 0.62:
        level = "high"
    elif score >= 0.38:
        level = "medium"
    else:
        level = "low"

    reason_codes = []
    if not hits:
        reason_codes.append("no_retrievable_evidence")
    if term_coverage < 0.5:
        reason_codes.append("limited_query_term_coverage")
    if len(hits) < 2:
        reason_codes.append("limited_supporting_evidence")
    if scenario is None:
        reason_codes.append("no_reliable_scenario_match")

    rarity = scenario.rarity if scenario else None
    if rarity == "boundary":
        route = "specialist_escalation"
        priority = "urgent"
        review_required = True
        reason_codes.append("regulated_or_policy_boundary")
    elif rarity == "rare" or level == "low":
        route = "instructor_review"
        priority = "high"
        review_required = True
        if rarity == "rare":
            reason_codes.append("rare_transition")
    elif level == "medium":
        route = "instructor_review"
        priority = "normal"
        review_required = True
    else:
        route = "provisional_guidance"
        priority = "low"
        review_required = False

    reasons = {
        "high": (
            "Strong retrieved evidence coverage; guidance may be shown provisionally."
        ),
        "medium": (
            "Useful evidence exists, but an instructor should resolve uncertainty."
        ),
        "low": (
            "Evidence is insufficient or weakly matched; do not infer a roadmap "
            "automatically."
        ),
    }
    return {
        "confidence": {
            "score": round(score, 4),
            "level": level,
            "signal": "retrieval_evidence_confidence",
            "top_result_score": round(top_score, 4),
            "matched_term_coverage": round(term_coverage, 4),
            "supporting_chunks": min(len(hits), 3),
            "discovery_margin": round(discovery_margin, 4),
            "explanation": reasons[level],
            "is_eligibility_probability": False,
        },
        "review": {
            "required": review_required,
            "route": route,
            "priority": priority,
            "reason_codes": sorted(set(reason_codes)),
            "publication_status": "provisional",
        },
    }
