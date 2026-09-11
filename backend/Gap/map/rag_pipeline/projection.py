"""Safe 3D projection of stored evidence embeddings for the demo explorer."""

from __future__ import annotations

import numpy as np

from ..models import EvidenceChunk


def build_embedding_map(max_points: int = 300) -> dict:
    """Project approved vectors to 3D without returning the source embeddings."""
    limit = max(10, min(int(max_points), 500))
    chunks = list(
        EvidenceChunk.objects.filter(
            approved=True,
            embedding__isnull=False,
        )
        .select_related("source", "scenario")
        .order_by("chunk_id")[:limit]
    )
    if not chunks:
        return {"projection": "pca_svd", "source_dimensions": 384, "dimensions": 3,
                "embedding_model": "", "count": 0,
                "explained_variance": [0.0, 0.0, 0.0], "points": []}

    matrix = np.asarray([list(chunk.embedding) for chunk in chunks], dtype=np.float32)
    centered = matrix - matrix.mean(axis=0, keepdims=True)
    _, singular_values, components = np.linalg.svd(centered, full_matrices=False)
    coordinates = centered @ components[: min(3, len(components))].T
    if coordinates.shape[1] < 3:
        coordinates = np.pad(coordinates, ((0, 0), (0, 3 - coordinates.shape[1])))
    scale = np.max(np.abs(coordinates), axis=0)
    scale[scale < 1e-8] = 1.0
    coordinates = coordinates / scale * 8.0

    variance = singular_values**2
    total_variance = float(variance.sum())
    explained = variance[:3] / total_variance if total_variance else np.zeros(3)
    explained = np.pad(explained, (0, max(0, 3 - len(explained))))[:3]

    points = []
    for chunk, position in zip(chunks, coordinates, strict=True):
        scenario = chunk.scenario
        points.append({
            "chunk_id": chunk.chunk_id, "x": round(float(position[0]), 5),
            "y": round(float(position[1]), 5), "z": round(float(position[2]), 5),
            "section": chunk.section,
            "scenario": ({"scenario_id": scenario.scenario_id, "title": scenario.title,
                          "rarity": scenario.rarity} if scenario else None),
            "review_status": chunk.source.review_status,
        })

    models = sorted({chunk.embedding_model for chunk in chunks if chunk.embedding_model})
    return {
        "projection": "pca_svd", "source_dimensions": matrix.shape[1], "dimensions": 3,
        "embedding_model": ", ".join(models), "count": len(points),
        "explained_variance": [round(float(value), 5) for value in explained],
        "points": points,
    }