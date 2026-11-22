from app.agent.retrieval_agent import RetrievalAgent

agent = RetrievalAgent()

results = agent.retrieve(
    "How do I submit Spark through Airflow?"
)

print(f"Retrieved {len(results)} documents")

for r in results:
    print(r["technology"])
    print(r["document"])
    print(r["score"])