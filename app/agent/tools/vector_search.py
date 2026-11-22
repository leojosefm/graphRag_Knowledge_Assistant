from app.agent.tools.base_tool import BaseTool
from app.retrieval.vector_retriever import VectorRetriever


class VectorSearchTool(BaseTool):

    def __init__(self):
        self.retriever = VectorRetriever()

    @property
    def name(self):
        return "vector_search"

    @property
    def description(self):
        return "Searches documentation using semantic similarity."

    def execute(self, question, top_k=10, technologies=None):

        return self.retriever.search(
            question=question,
            top_k=top_k,
            technologies=technologies
        )