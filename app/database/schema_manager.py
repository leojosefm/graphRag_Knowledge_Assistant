from app.neo4j_connection import Neo4jConnection


class SchemaManager:

    def __init__(self):
        self.db = Neo4jConnection()

    def create_constraints(self):

        query = """
        CREATE CONSTRAINT technology_name_unique
        IF NOT EXISTS
        FOR (t:Technology)
        REQUIRE t.name IS UNIQUE
        """

        self.db.execute_query(query)

    def close(self):
        self.db.close()