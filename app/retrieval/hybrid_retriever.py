from app.retrieval.vector_retriever import VectorRetriever
from app.retrieval.graph_retriever import GraphRetriever


class HybridRetriever:

    def __init__(self):
        self.vector = VectorRetriever()
        self.graph = GraphRetriever()

    def close(self):
        self.vector.close()
        self.graph.close()

    def search(
        self,
        question: str,
        top_k: int = 5
    ):
        """
        Performs hybrid retrieval by:
        1. Finding the most relevant chunks using vector search.
        2. Expanding each chunk with graph context.
        """

        vector_results = self.vector.search(
            question=question,
            top_k=top_k
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