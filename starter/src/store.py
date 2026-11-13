"""Store and search vectors using PostgreSQL + pgvector."""
import json
import logging
from typing import Any
import psycopg
from .models import Chunk

logger = logging.getLogger(__name__)


class PgVectorStore:
    def __init__(self, database_url: str, dimensions: int) -> None:
        """Retain connection settings; validate model dimensions."""
        if dimensions <= 0:
            raise ValueError(f"dimensions must be a positive integer, got {dimensions}")

        self.database_url = database_url
        self.dimensions = dimensions

    def _get_connection(self) -> psycopg.Connection:
        return psycopg.connect(self.database_url)

    def create_schema(self) -> None:
        """Create table with vector column and source/page/filter metadata."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                # Ensure pgvector extension is enabled
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

                # Table structure with composite primary key (strategy, chunk_id)
                cur.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS chunks (
                        strategy VARCHAR(50) NOT NULL,
                        chunk_id VARCHAR(255) NOT NULL,
                        document_id VARCHAR(255) NOT NULL,
                        source TEXT NOT NULL,
                        page INT NOT NULL,
                        text TEXT NOT NULL,
                        metadata JSONB NOT NULL DEFAULT '{{}}'::jsonb,
                        embedding vector({self.dimensions}) NOT NULL,
                        PRIMARY KEY (strategy, chunk_id)
                    );
                    """
                )

                # Indexes for fast lookup, deletion, and metadata filtering
                cur.execute(
                    "CREATE INDEX IF NOT EXISTS idx_chunks_strat_doc ON chunks (strategy, document_id);"
                )
                cur.execute(
                    "CREATE INDEX IF NOT EXISTS idx_chunks_metadata ON chunks USING gin (metadata);"
                )

                # pgvector HNSW index supports up to 2000 dimensions; > 2000 uses exact search
                if self.dimensions <= 2000:
                    cur.execute(
                        """
                        CREATE INDEX IF NOT EXISTS idx_chunks_embedding
                        ON chunks USING hnsw (embedding vector_cosine_ops);
                        """
                    )
            conn.commit()

    def upsert(self, strategy: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        """Validate lengths/dimensions and write stable IDs without duplicates.

        When re-ingesting changed source documents, remove obsolete chunks too.
        """
        if len(chunks) != len(vectors):
            raise ValueError(
                f"Mismatch: received {len(chunks)} chunks and {len(vectors)} vectors"
            )

        if not chunks:
            return

        # Validate vector dimensions
        for i, vec in enumerate(vectors):
            if len(vec) != self.dimensions:
                raise ValueError(
                    f"Vector {i} dimension mismatch: expected {self.dimensions}, got {len(vec)}"
                )

        doc_ids = list({c.document_id for c in chunks})

        with self._get_connection() as conn:
            with conn.cursor() as cur:
                # Clean up existing/obsolete chunks for these documents under this strategy
                cur.execute(
                    "DELETE FROM chunks WHERE strategy = %s AND document_id = ANY(%s);",
                    (strategy, doc_ids),
                )

                # Insert new chunks
                insert_sql = """
                    INSERT INTO chunks (
                        strategy, chunk_id, document_id, source, page, text, metadata, embedding
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s::jsonb, %s::vector
                    )
                    ON CONFLICT (strategy, chunk_id) DO UPDATE SET
                        document_id = EXCLUDED.document_id,
                        source = EXCLUDED.source,
                        page = EXCLUDED.page,
                        text = EXCLUDED.text,
                        metadata = EXCLUDED.metadata,
                        embedding = EXCLUDED.embedding;
                """

                rows = [
                    (
                        strategy,
                        c.chunk_id,
                        c.document_id,
                        c.source,
                        c.page,
                        c.text,
                        json.dumps(c.metadata or {}),
                        "[" + ",".join(str(x) for x in v) + "]",
                    )
                    for c, v in zip(chunks, vectors)
                ]

                cur.executemany(insert_sql, rows)
            conn.commit()

    def search(
        self,
        strategy: str,
        query_vector: list[float],
        top_k: int = 3,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Filter permitted metadata in SQL, rank by cosine distance, return top-k.

        Return chunk ID, text, score and metadata. Parameterize user-supplied values.
        """
        if len(query_vector) != self.dimensions:
            raise ValueError(
                f"Query vector dimension mismatch: expected {self.dimensions}, got {len(query_vector)}"
            )

        vec_str = "[" + ",".join(str(x) for x in query_vector) + "]"

        where_clauses = ["strategy = %s"]
        where_params: list[Any] = [strategy]

        if filters:
            for key, val in filters.items():
                if val is None:
                    continue
                if key == "document_id":
                    where_clauses.append("document_id = %s")
                    where_params.append(str(val))
                elif key == "page":
                    where_clauses.append("page = %s")
                    where_params.append(int(val))
                elif key == "source":
                    where_clauses.append("source = %s")
                    where_params.append(str(val))
                else:
                    # Filter inside JSONB metadata safely using containment operator
                    where_clauses.append("metadata @> %s::jsonb")
                    where_params.append(json.dumps({key: val}))

        where_sql = " AND ".join(where_clauses)

        sql = f"""
            SELECT chunk_id, document_id, source, page, text, metadata,
                   (embedding <=> %s::vector) AS distance
            FROM chunks
            WHERE {where_sql}
            ORDER BY distance ASC
            LIMIT %s;
        """

        # Parameters must match SQL placeholder order:
        # 1. vec_str in SELECT clause
        # 2. where_params in WHERE clause
        # 3. top_k in LIMIT clause
        params = [vec_str] + where_params + [top_k]

        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                rows = cur.fetchall()

        results: list[dict[str, Any]] = []
        for r in rows:
            chunk_id, doc_id, source, page, text, meta, dist = r
            results.append(
                {
                    "chunk_id": chunk_id,
                    "document_id": doc_id,
                    "source": source,
                    "page": page,
                    "text": text,
                    "metadata": meta if isinstance(meta, dict) else {},
                    "score": float(dist),
                    "strategy": strategy,
                }
            )

        return results
