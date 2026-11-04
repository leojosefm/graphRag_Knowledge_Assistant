import os
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD")

        if not self.password:
            raise ValueError("NEO4J_PASSWORD password is missing")

        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))


    def verify_connection(self):
        self.driver.verify_connectivity()
        return True

    def execute_query(self, query, parameters=None):
        with self.driver.session(database = "neo4j") as session:
            result = session.run(query, parameters)
            return result.data()
        

    def close(self):
        self.driver.close()