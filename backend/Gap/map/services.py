from collections import deque
from dataclasses import dataclass

import networkx as nx
from django.db import transaction
from django.db.models import Case, IntegerField, Value, When
from django.utils import timezone

from .models import (
    Attempt,
    BridgePlan,
    BridgeStep,
    Concept,
    DiagnosticItem,
    DiagnosticSession,
    PrerequisiteEdge,
)


@dataclass(frozen=True)
class MasteryEvidence:
    concept_id: int
    correct: int
    total: int
    probability: float
    status: str


def mastery_for_session(session: DiagnosticSession) -> dict[int, MasteryEvidence]:
    """Return transparent, lightweight mastery estimates from this session's answers."""
    evidence: dict[int, list[bool]] = {}
    for attempt in session.attempts.select_related("item__concept"):
        evidence.setdefault(attempt.item.concept_id, []).append(attempt.is_correct)

    result = {}
    for concept_id, values in evidence.items():
        correct = sum(values)
        total = len(values)
        # Beta(1, 1) prior avoids claiming 0% or 100% from a tiny sample.
        probability = (correct + 1) / (total + 2)
        if probability >= 0.66:
            status = "mastered"
        elif probability <= 0.40:
            status = "gap"
        else:
            status = "uncertain"
        result[concept_id] = MasteryEvidence(
            concept_id=concept_id,
            correct=correct,
            total=total,
            probability=round(probability, 3),
            status=status,
        )
    return result


def prerequisite_ids(curriculum_id: int, dependent_id: int) -> list[int]:
    return list(
        PrerequisiteEdge.objects.filter(
            curriculum_id=curriculum_id,
            dependent_id=dependent_id,
            approved=True,
        )
        .order_by("id")
        .values_list("prerequisite_id", flat=True)
    )


def next_diagnostic_item(session: DiagnosticSession) -> DiagnosticItem | None:
    """Select a target question, then walk backwards only when evidence exposes a gap."""
    if session.status != "active" or session.attempts.count() >= session.max_questions:
        return None

    curriculum_id = session.learner.destination_curriculum_id
    mastery = mastery_for_session(session)
    attempted_item_ids = set(session.attempts.values_list("item_id", flat=True))
    queue = deque([session.target_concept_id])
    visited = set()

    while queue:
        concept_id = queue.popleft()
        if concept_id in visited:
            continue
        visited.add(concept_id)
        concept_evidence = mastery.get(concept_id)

        if concept_evidence and concept_evidence.status == "mastered":
            continue
        if concept_evidence and concept_evidence.status == "gap":
            parents = prerequisite_ids(curriculum_id, concept_id)
            if parents:
                queue.extend(parents)
                continue

        item = (
            DiagnosticItem.objects.filter(
                curriculum_id=curriculum_id,
                concept_id=concept_id,
                approved=True,
            )
            .exclude(id__in=attempted_item_ids)
            .annotate(
                language_rank=Case(
                    When(language=session.learner.preferred_language, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField(),
                )
            )
            .order_by("language_rank", "difficulty", "id")
            .first()
        )
        if item:
            return item
        queue.extend(prerequisite_ids(curriculum_id, concept_id))

    return None


@transaction.atomic
def record_answer(
    session: DiagnosticSession,
    item: DiagnosticItem,
    answer: str,
    response_time_ms: int | None = None,
) -> Attempt:
    if session.status != "active":
        raise ValueError("This diagnostic session is no longer active.")
    if item.curriculum_id != session.learner.destination_curriculum_id:
        raise ValueError("The item does not belong to the learner's destination curriculum.")
    if session.attempts.filter(item=item).exists():
        raise ValueError("This diagnostic item has already been answered.")

    attempt = Attempt.objects.create(
        session=session,
        item=item,
        answer=answer.strip(),
        is_correct=answer.strip().casefold() == item.correct_answer.strip().casefold(),
        response_time_ms=response_time_ms,
    )

    if session.attempts.count() >= session.max_questions or next_diagnostic_item(session) is None:
        session.status = "review"
        session.completed_at = timezone.now()
        session.save(update_fields=["status", "completed_at"])
    return attempt


def close_if_exhausted(session: DiagnosticSession) -> None:
    if session.status == "active" and next_diagnostic_item(session) is None:
        session.status = "review"
        session.completed_at = timezone.now()
        session.save(update_fields=["status", "completed_at"])


def gap_map(session: DiagnosticSession) -> dict:
    curriculum_id = session.learner.destination_curriculum_id
    mastery = mastery_for_session(session)
    concept_ids = {session.target_concept_id}
    queue = deque([session.target_concept_id])
    edges = []

    while queue:
        dependent_id = queue.popleft()
        for edge in PrerequisiteEdge.objects.filter(
            curriculum_id=curriculum_id,
            dependent_id=dependent_id,
            approved=True,
        ).select_related("prerequisite", "dependent"):
            edges.append(
                {
                    "prerequisite": edge.prerequisite_id,
                    "dependent": edge.dependent_id,
                    "rationale": edge.rationale,
                }
            )
            if edge.prerequisite_id not in concept_ids:
                concept_ids.add(edge.prerequisite_id)
                queue.append(edge.prerequisite_id)

    nodes = []
    for concept in Concept.objects.filter(id__in=concept_ids).order_by("name"):
        item = mastery.get(concept.id)
        nodes.append(
            {
                "id": concept.id,
                "code": concept.code,
                "name": concept.name,
                "is_target": concept.id == session.target_concept_id,
                "status": item.status if item else "untested",
                "mastery_probability": item.probability if item else None,
                "evidence_count": item.total if item else 0,
            }
        )

    return {"session_id": session.id, "nodes": nodes, "edges": edges}


@transaction.atomic
def generate_bridge_plan(session: DiagnosticSession) -> BridgePlan:
    graph_data = gap_map(session)
    graph = nx.DiGraph()
    for node in graph_data["nodes"]:
        graph.add_node(node["id"], **node)
    for edge in graph_data["edges"]:
        graph.add_edge(edge["prerequisite"], edge["dependent"])

    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError("The approved prerequisite graph contains a cycle.")

    # Do not prescribe every untested topic. Use evidenced gaps plus the learning target.
    needed_ids = {
        node_id
        for node_id, data in graph.nodes(data=True)
        if data["status"] in {"gap", "uncertain"}
    }
    needed_ids.add(session.target_concept_id)
    ordered_ids = [node_id for node_id in nx.topological_sort(graph) if node_id in needed_ids]

    plan, _ = BridgePlan.objects.get_or_create(session=session)
    plan.steps.all().delete()
    concepts = Concept.objects.in_bulk(ordered_ids)
    for order, concept_id in enumerate(ordered_ids, start=1):
        concept = concepts[concept_id]
        BridgeStep.objects.create(
            plan=plan,
            concept=concept,
            order=order,
            activity=f"Complete a focused worked example and practice set on {concept.name}.",
            duration_minutes=20,
            evidence_prompt=f"Solve one new {concept.name} problem and explain the method.",
        )
    return plan
