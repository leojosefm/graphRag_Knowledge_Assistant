from app.agent.tools.vector_search import VectorSearchTool
from app.agent.tools.graph_search import GraphSearchTool

vector = VectorSearchTool()
graph = GraphSearchTool()

chunks = vector.execute(
    question="How do I submit Spark through Airflow?",
    top_k=1
)

print(chunks[0]["chunk_id"])   # <-- this is a real chunk id

result = graph.execute(
    chunk_id=chunks[0]["chunk_id"]
)

print(result["technology"])
print(result["document"])
print(result["related_technologies"])