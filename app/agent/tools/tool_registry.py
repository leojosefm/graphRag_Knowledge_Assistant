from app.agent.tools.vector_search import VectorSearchTool
from app.agent.tools.graph_search import GraphSearchTool


class ToolRegistry:

    def __init__(self):

        self.tools = {
            "vector_search": VectorSearchTool(),
            "graph_search": GraphSearchTool()
        }

    def get(self, name):
        return self.tools[name]

    def list(self):
        return list(self.tools.values())