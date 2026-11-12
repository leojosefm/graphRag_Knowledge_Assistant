from app.embedding.embedding_service import EmbeddingService
from app.neo4j_connection import Neo4jConnection


class VectorRetriever:

    def __init__(self):
        self.db = Neo4jConnection()
        self.embedding_service = EmbeddingService()

    def close(self):
        self.db.close()

    def search(
        self,
        question: str,
        top_k: int = 20,
        technologies: list[str] | None = None
    ):
        """
        Returns the top_k most similar chunks.
        """

        embedding = self.embedding_service.embed(question)

        #Search my Vector Index in Neo4j - top K elements ANN 
        # if technolgies is not None, filter by technology
        query = """
        CALL db.index.vector.queryNodes(
            'chunk_embedding_index',
            $top_k,
            $embedding
        )
        YIELD node, score

        MATCH (d:Document)-[:HAS_CHUNK]->(node)
        MATCH  (t:Technology)-[:HAS_DOCUMENT]->(d)
        WHERE
            $technologies IS NULL
            OR size($technologies) = 0
            OR t.name IN $technologies

        RETURN
            t.name as technology,
            d.title as document,
            d.url as url,
            node.id AS chunk_id,
            node.chunk_number AS chunk_number,
            node.text AS text,
            score

        ORDER BY score DESC
        """

        return self.db.execute_query(
            query,
            {
                "top_k": top_k,
                "embedding": embedding,
                "technologies": technologies
            }
        )