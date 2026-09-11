"""Integrity and source-approval guardrails for retrieved evidence."""

import hashlib

from .config import ALLOWED_REVIEW_STATUSES


def chunk_integrity_valid(chunk):
    if not chunk.checksum:
        return False
    expected = hashlib.sha256(chunk.text.encode("utf-8")).hexdigest()
    return expected == chunk.checksum


def approved_evidence_queryset(queryset):
    """Apply the non-negotiable evidence publication boundary."""
    return queryset.filter(
        approved=True,
        source__review_status__in=ALLOWED_REVIEW_STATUSES,
    )
