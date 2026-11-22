from app.agent.tools.base_tool import BaseTool
from app.retrieval.hybrid_retriever import HybridRetriever


class RetrievalTool(BaseTool):

    name = "retrieval"

    description = (
        "Searches the knowledge base using semantic search and the knowledge graph."
    )

    def __init__(self):
        self.retriever = HybridRetriever()

    def execute(
        self,
        question,
        top_k=20
    ):

        print("RetrievalTool.execute()")

        return self.retriever.search(
            question=question,
            top_k=top_k
        )

    def close(self):
        self.retriever.close()