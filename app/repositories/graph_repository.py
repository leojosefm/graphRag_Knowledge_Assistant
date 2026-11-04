from platform import node

from app.neo4j_connection import Neo4jConnection
from app.models.labels import Label
from app.models.relationship import Relationship
import re

class GraphRepository:

    def __init__(self):
        self.db = Neo4jConnection()

    def close(self):
        self.db.close()

    # ------------------------------------------------------------------
    # Generic Node Operations
    # ------------------------------------------------------------------

    def create_node(self, label: Label, properties: dict, identity_key: str = "name"):


        if not isinstance(label, Label):
            raise ValueError("Invalid node label")


        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", identity_key):
            raise ValueError("Invalid identity key")

        if identity_key not in properties:
            raise ValueError(f"'{identity_key}' is required")

        identity_value = properties[identity_key]

        other_properties = {
            key: value
            for key, value in properties.items()
            if key != identity_key
        }

        for key in other_properties:
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
                raise ValueError(f"Invalid property name: {key}")
        
        query = f"""
        MERGE (n:{label.value} {{{identity_key}: $identity_value}})
        SET n += $properties
        RETURN
            properties(n) AS node
        """
            # MERGE (n:Technology {name: "Spark"})
            # SET n += {
            #     category: "PROCESSING",
            #     description: "Distributed data processing engine"
            # }
            # RETURN properties(n) AS node
        

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