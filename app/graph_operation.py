from app.database import Neo4jConnection
from app.models.relationship import Relationship

def create_technology(name, category):
    db = Neo4jConnection()

    try:
        query = """
        CREATE (t:Technology {
            name: $name,
            category: $category
        })
        RETURN t
        """

        # This creates Technology node with name and category properties

        result = db.execute_query(
            query,
            {
                "name": name,
                "category": category
            }
        )

        return result

    finally:
        db.close()


def get_technology(name):
    # Read all technology nodes with a given name
    db = Neo4jConnection()

    try:
        query = """
        MATCH (t:Technology {name: $name})
        RETURN properties(t) AS technology
        """

        return db.execute_query(
            query,
            {"name": name}
        )

    finally:
        db.close()


def create_relationship(source: str, target: str, relation: Relationship):
    db = Neo4jConnection()

    try:
        query = f"""
        MATCH (k:Technology {{name:$source}})
        MATCH (s:Technology {{name:$target}})
        MERGE (k)-[r:{relation.value}]->(s)

        RETURN
            properties(k) AS source,
            type(r) AS relationship,
            properties(s) AS target
        """

        result = db.execute_query(
            query,
            {
                "source": source,
                "target": target
            }
        )

        if not result:
            raise ValueError("Source or target technology was not found")

        return result

    finally:
        db.close()