# PostgreSQL pgvector HNSW cosine index; state-only on non-PostgreSQL databases.

import pgvector.django.indexes
from django.db import migrations

INDEX_NAME = "map_evidence_embedding_hnsw"


def create_hnsw_index(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute(
            f"CREATE INDEX IF NOT EXISTS {INDEX_NAME} "
            "ON map_evidencechunk USING hnsw "
            "(embedding vector_cosine_ops) "
            "WITH (m = 16, ef_construction = 64)"
        )


def drop_hnsw_index(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute(f"DROP INDEX IF EXISTS {INDEX_NAME}")


class Migration(migrations.Migration):
    dependencies = [
        ("map", "0004_academicsource_evidencechunk"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(create_hnsw_index, drop_hnsw_index),
            ],
            state_operations=[
                migrations.AddIndex(
                    model_name="evidencechunk",
                    index=pgvector.django.indexes.HnswIndex(
                        ef_construction=64,
                        fields=["embedding"],
                        m=16,
                        name=INDEX_NAME,
                        opclasses=["vector_cosine_ops"],
                    ),
                ),
            ],
        ),
    ]
