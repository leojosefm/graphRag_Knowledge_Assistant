from app.neo4j_connection import Neo4jConnection


class GraphRetriever:

    def __init__(self):
        self.db = Neo4jConnection()

    def close(self):
        self.db.close()

    def expand_chunk(
        self,
        chunk_id: str
    ):
        """
        Expands a retrieved chunk into its surrounding graph context.
        """

        # find documents of a chunk id optional match (LEFT JOIN)
        # Collect neighbouting tecbnologies and their relationships
        query = """
        MATCH (t:Technology)-[:HAS_DOCUMENT]->(d:Document)-[:HAS_CHUNK]->(c:Chunk)
        WHERE c.id = $chunk_id

        OPTIONAL MATCH (t)-[r]->(related:Technology)

        RETURN
            t.name AS technology,
            d.title AS document,
            d.url AS url,
            c.chunk_number AS chunk_number,
            c.text AS text,
            collect(
                DISTINCT {
                    technology: related.name,
                    relationship: type(r)
                }
            ) AS related_technologies
        """

        results = self.db.execute_query(
            query,
            {
                "chunk_id": chunk_id
            }
        )

        return results[0] if results else None