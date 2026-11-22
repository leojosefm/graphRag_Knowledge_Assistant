from app.agent.tools.base_tool import BaseTool


class Neo4jQueryTool(BaseTool):

    name = "neo4j_query"

    description = "Executes Cypher queries against Neo4j."

    def execute(self, question: str, **kwargs):
        print("Neo4jQueryTool.execute()")
        return []

    def close(self):
        pass