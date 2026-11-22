from app.agent.tools.vector_search import VectorSearchTool

tool = VectorSearchTool()

results = tool.execute(
    question="How do I submit Spark through Airflow?"
)

for result in results[:3]:
    print(result["technology"])
    print(result["document"])
    print(result["score"])
    print(result["text"][:200])
    print("-" * 80)