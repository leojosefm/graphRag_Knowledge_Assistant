from app.agent.planner import Planner

planner = Planner()

question =  "How do I submit Spark jobs from Airflow?"
plan = planner.plan(question)   
print(plan)


question =  "What are the latest features in Spark 4.3?"
plan = planner.plan(question)   
print(plan)

question =  "What technologies are connected to Spark in the knowledge graph?"
plan = planner.plan(question)   
print(plan)
