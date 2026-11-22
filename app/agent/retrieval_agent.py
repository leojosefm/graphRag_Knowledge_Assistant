from app.agent.tools.tool_registry import ToolRegistry


class RetrievalAgent:

    def __init__(self):
        self.registry = ToolRegistry()

    def retrieve(
        self,
        question: str,
        top_k: int = 20
    ):

        vector_tool = self.registry.get("vector_search")
        graph_tool = self.registry.get("graph_search")

        chunks = vector_tool.execute(
            question=question,
            top_k=top_k
        )

        results = []

        for chunk in chunks:

            graph = graph_tool.execute(
                chunk["chunk_id"]
            )

            if graph:

                graph["score"] = chunk["score"]
                results.append(graph)

        return results