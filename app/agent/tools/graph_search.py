from app.agent.tools.base_tool import BaseTool
from app.retrieval.graph_retriever import GraphRetriever


class GraphSearchTool(BaseTool):

    def __init__(self):
        self.retriever = GraphRetriever()

    @property
    def name(self):
        return "graph_search"

    @property
    def description(self):
        return "Expands a retrieved chunk using graph relationships."

    def execute(self, chunk_id):

        return self.retriever.expand_chunk(chunk_id)