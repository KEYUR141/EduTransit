# GapMap RAG pipeline

This package owns the complete retrieval pipeline used by the prototype.

1. `ingestion.py` converts a validated transition scenario into small, traceable evidence chunks, creates a reviewed source, embeds every chunk, records the embedding model, and stores a SHA-256 integrity checksum.
2. `embeddings.py` produces normalized 384-dimensional Sentence Transformer vectors. Its deterministic hash fallback is only for offline prototype resilience and is clearly reported in API output.
3. `guardrails.py` permits only approved chunks from reviewed, approved, or explicitly illustrative sources and rejects altered chunk text.
4. `retrieval.py` enforces the selected scenario, performs pgvector cosine retrieval on PostgreSQL (or application-side similarity for SQLite), and returns citations.
5. `scoring.py` combines lexical/canonical matching (48%), vector similarity (32%), exact phrases (15%), and competency-code matching (5%). It also explains why each result was retrieved.

The pipeline retrieves evidence; it does not decide equivalence, admission, or eligibility. Those decisions remain rule- and human-governed.

Public imports are exposed by `rag_pipeline/__init__.py`:

```python
from map.rag_pipeline import retrieve_evidence, upsert_scenario_evidence
```
