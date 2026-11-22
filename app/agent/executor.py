from app.agent.tools.tool_registry import ToolRegistry


class Executor:

    def __init__(self):
        self.registry = ToolRegistry()

    def execute(
        self,
        plan,
        question,
        top_k=20
    ):

        context = []

        for tool_name in plan["tools"]:

            tool = self.registry.get(tool_name)

            result = tool.execute(
                question=question,
                top_k=top_k
            )

            context.extend(result)

        return context

    def close(self):
        self.registry.close()