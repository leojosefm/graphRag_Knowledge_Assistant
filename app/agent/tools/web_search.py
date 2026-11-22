from app.agent.tools.base_tool import BaseTool


class WebSearchTool(BaseTool):

    name = "web_search"

    description = "Searches the web."

    def execute(self, question: str, **kwargs):
        print("WebSearchTool.execute()")
        return []

    def close(self):
        pass