"""Configuration shared by the GapMap RAG pipeline."""

import re

EMBEDDING_DIMENSIONS = 384
MAX_CANDIDATES = 160
ALLOWED_REVIEW_STATUSES = ("reviewed", "approved", "illustrative")
TOKEN_PATTERN = re.compile(r"[a-z0-9][a-z0-9+.#-]*")

SYNONYMS = {
    "statistics": {"probability", "inference", "regression", "anova"},
    "programming": {"coding", "python", "algorithm", "data-structures"},
    "mathematics": {"math", "quantitative", "calculus", "algebra"},
    "language": {"terminology", "medium", "english", "hindi"},
    "evidence": {"transcript", "syllabus", "certificate", "document"},
    "prerequisite": {"foundation", "readiness", "requirement"},
    "agriculture": {"crop", "soil", "gis", "remote-sensing"},
    "accessibility": {"accessible", "format", "accommodation"},
}
