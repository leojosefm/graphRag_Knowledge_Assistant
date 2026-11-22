from app.llm.llm_service import LLMService
import json


class Planner:

    def __init__(self):
        self.llm = LLMService()

    def plan(self, question: str):

        prompt = f"""
You are an AI planner.

Available tools:

1. retrieval
Description:
Searches the internal documentation using GraphRAG.

Use for:
- Answering questions about internal documentation
- Finding information from ingested documents

2. web_search
Description:
Searches the public internet.

Use for:
- Questions about recent events
- Information not contained in the internal knowledge base

3. neo4j_query
Description:
Executes Cypher queries against the knowledge graph.

Use for:
- Questions about relationships in the graph
- Finding connected technologies
- Graph exploration

Return ONLY valid JSON.

Example:

{{
    "tools": ["retrieval"]
}}

Question:
{question}
"""

        response = self.llm.generate(prompt)

        response = response.strip()

        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "").strip()

        return json.loads(response)