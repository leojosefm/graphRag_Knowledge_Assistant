from app.agent.tools.retrieval import RetrievalTool
from app.agent.tools.web_search import WebSearchTool
from app.agent.tools.neo4j_query import Neo4jQueryTool


class ToolRegistry:

    def __init__(self):

        self.tools = {
            "retrieval": RetrievalTool(),
            "web_search": WebSearchTool(),
            "neo4j_query": Neo4jQueryTool()
        }

    def get(self, name):
        return self.tools[name]

    def list(self):
        return list(self.tools.values())

    def close(self):

        for tool in self.tools.values():
            tool.close()