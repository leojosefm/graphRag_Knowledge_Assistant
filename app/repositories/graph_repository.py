from neo4j_connection import Neo4jConnection
from models.labels import Label
from models.relationship import Relationship


class GraphRepository:

    def __init__(self):
        self.db = Neo4jConnection()

    def close(self):
        self.db.close()

    # ------------------------------------------------------------------
    # Generic Node Operations
    # ------------------------------------------------------------------

    def create_node(self, label: Label, properties: dict):

        property_string = ", ".join(
            [f"{key}: ${key}" for key in properties.keys()]
        )

        query = f"""
        MERGE (n:{label.value} {{{property_string}}})

        RETURN
            properties(n) AS node
        """

        return self.db.execute_query(query, properties)

    def get_node(self, label: Label, name: str):

        query = f"""
        MATCH (n:{label.value} {{name:$name}})

        RETURN
            properties(n) AS node
        """

        return self.db.execute_query(
            query,
            {
                "name": name
            }
        )

    def get_all_nodes(self, label: Label):

        query = f"""
        MATCH (n:{label.value})

        RETURN
            properties(n) AS node

        ORDER BY n.name
        """

        return self.db.execute_query(query)

    def update_node(self, label: Label, name: str, properties: dict):

        set_clause = ", ".join(
            [f"n.{key} = ${key}" for key in properties.keys()]
        )

        query = f"""
        MATCH (n:{label.value} {{name:$name}})

        SET
            {set_clause}

        RETURN
            properties(n) AS node
        """

        params = {"name": name}
        params.update(properties)

        return self.db.execute_query(query, params)

    def delete_node(self, label: Label, name: str):

        query = f"""
        MATCH (n:{label.value} {{name:$name}})

        DETACH DELETE n
        """

        return self.db.execute_query(
            query,
            {
                "name": name
            }
        )

    # ------------------------------------------------------------------
    # Relationship Operations
    # ------------------------------------------------------------------

    def create_relationship(
        self,
        source_label: Label,
        source_name: str,
        relationship: Relationship,
        target_label: Label,
        target_name: str
    ):

        query = f"""
        MATCH (s:{source_label.value} {{name:$source}})
        MATCH (t:{target_label.value} {{name:$target}})

        MERGE (s)-[r:{relationship.value}]->(t)

        RETURN
            properties(s) AS source,
            type(r) AS relationship,
            properties(t) AS target
        """

        return self.db.execute_query(
            query,
            {
                "source": source_name,
                "target": target_name
            }
        )
        # MATCH (n:Technology {{name:'{source_name}'}})  -- Cypher injection
        # Kafka'}) DETACH DELETE n //
        # MATCH (n:Technology {name:'Kafka'}) DETACH DELETE n //'})
        # use parameters  MATCH (n:Technology {name:$source})
#         {
#     "source": "Kafka'}) DETACH DELETE n //"
# }  MATCH (n:Technology {name:$source})
#  source = "Kafka'}) DETACH DELETE n //" returns nothing
 
    def get_neighbors(self, label: Label, name: str):

        query = f"""
        MATCH (n:{label.value} {{name:$name}})-[r]-(neighbor)

        RETURN
            properties(n) AS node,
            type(r) AS relationship,
            properties(neighbor) AS neighbor

        ORDER BY neighbor.name
        """

        return self.db.execute_query(
            query,
            {
                "name": name
            }
        )

    def delete_relationship(
        self,
        source_label: Label,
        source_name: str,
        relationship: Relationship,
        target_label: Label,
        target_name: str
    ):

        query = f"""
        MATCH (s:{source_label.value} {{name:$source}})
              -[r:{relationship.value}]->
              (t:{target_label.value} {{name:$target}})

        DELETE r
        """

        return self.db.execute_query(
            query,
            {
                "source": source_name,
                "target": target_name
            }
        )