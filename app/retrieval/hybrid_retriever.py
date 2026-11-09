from app.retrieval.vector_retriever import VectorRetriever
from app.retrieval.graph_retriever import GraphRetriever


class HybridRetriever:

    def __init__(self):
        self.vector = VectorRetriever()
        self.graph = GraphRetriever()

    def close(self):
        self.vector.close()
        self.graph.close()

    def _extract_technologies(self, question: str):

        technologies = []

        q = question.lower()

        for tech in [
            "spark",
            "airflow",
            "dbt",
            "iceberg",
            "trino"
        ]:
            if tech in q:
                technologies.append(tech.title())

        return technologies

    def _limit_chunks_per_document(
        self,
        results,
        max_chunks_per_document=2
        ):

        counts = {}
        filtered = []

        for result in results:

            document = result["url"]

            if counts.get(document, 0) < max_chunks_per_document:

                filtered.append(result)
                counts[document] = counts.get(document, 0) + 1

        return filtered

    def search(
        self,
        question: str,
        top_k: int = 50
        ):
        """
        Performs hybrid retrieval by:
        1. Finding the most relevant chunks using vector search.
        2. Expanding each chunk with graph context.
        """

        technologies = self._extract_technologies(question)


        vector_results = self.vector.search(
            question=question,
            top_k=top_k,
            technologies=technologies
        )

        vector_results = self._limit_chunks_per_document(
            vector_results,
            max_chunks_per_document=2
        )

        results = []

        for chunk in vector_results:

            graph_context = self.graph.expand_chunk(
                chunk["chunk_id"]
            )

            if graph_context:

                graph_context["score"] = chunk["score"]

                results.append(graph_context)

        return results