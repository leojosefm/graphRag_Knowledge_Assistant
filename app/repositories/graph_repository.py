
import re

from app.neo4j_connection import Neo4jConnection
from app.models.labels import Label
from app.models.relationship import Relationship


class GraphRepository:

    def __init__(self):
        self.db = Neo4jConnection()

    def close(self):
        self.db.close()

    # =========================================================
    # Generic Node Operations
    # =========================================================

    def create_node(
        self,
        label: Label,
        properties: dict,
        identity_key: str = "name"
    ):

        if not isinstance(label, Label):
            raise ValueError("Invalid node label")

        if not isinstance(properties, dict):
            raise ValueError("Properties must be a dictionary")

        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", identity_key):
            raise ValueError("Invalid identity key")

        if identity_key not in properties:
            raise ValueError(f"'{identity_key}' is required")

        identity_value = properties[identity_key]

        if identity_value is None or identity_value == "":
            raise ValueError(f"'{identity_key}' cannot be empty")

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
        RETURN properties(n) AS node
        """

        params = {
            "identity_value": identity_value,
            "properties": other_properties
        }

        return self.db.execute_query(query, params)

    def get_node(self, label: Label, name: str):

        query = f"""
        MATCH (n:{label.value} {{name: $name}})
        RETURN properties(n) AS node
        """

        return self.db.execute_query(
            query,
            {"name": name}
        )

    def get_all_nodes(self, label: Label):

        query = f"""
        MATCH (n:{label.value})
        RETURN properties(n) AS node
        ORDER BY n.name
        """

        return self.db.execute_query(query)

    def update_node(
        self,
        label: Label,
        name: str,
        properties: dict
    ):

        for key in properties:
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
                raise ValueError(f"Invalid property name: {key}")

        set_clause = ", ".join(
            [f"n.{key} = ${key}" for key in properties.keys()]
        )

        query = f"""
        MATCH (n:{label.value} {{name: $name}})
        SET {set_clause}
        RETURN properties(n) AS node
        """

        params = {"name": name}
        params.update(properties)

        return self.db.execute_query(query, params)

    def delete_node(self, label: Label, name: str):

        query = f"""
        MATCH (n:{label.value} {{name: $name}})
        DETACH DELETE n
        """

        return self.db.execute_query(
            query,
            {"name": name}
        )

    # =========================================================
    # Relationship Operations
    # =========================================================

    def create_relationship(
        self,
        source_label: Label,
        source_key: str,
        source_value: str,
        relationship: Relationship,
        target_label: Label,
        target_key: str,
        target_value: str
    ):

        if not isinstance(source_label, Label):
            raise ValueError("Invalid source label")

        if not isinstance(target_label, Label):
            raise ValueError("Invalid target label")

        if not isinstance(relationship, Relationship):
            raise ValueError("Invalid relationship type")

        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", source_key):
            raise ValueError("Invalid source key")

        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", target_key):
            raise ValueError("Invalid target key")

        query = f"""
        MATCH (s:{source_label.value} {{{source_key}: $source}})
        MATCH (t:{target_label.value} {{{target_key}: $target}})

        MERGE (s)-[r:{relationship.value}]->(t)

        RETURN
            properties(s) AS source,
            type(r) AS relationship,
            properties(t) AS target
        """

        return self.db.execute_query(
            query,
            {
                "source": source_value,
                "target": target_value
            }
        )

    def get_neighbors(self, label: Label, name: str):

        query = f"""
        MATCH (n:{label.value} {{name: $name}})-[r]-(neighbor)

        RETURN
            properties(n) AS node,
            type(r) AS relationship,
            properties(neighbor) AS neighbor

        ORDER BY neighbor.name
        """

        return self.db.execute_query(
            query,
            {"name": name}
        )

    def get_all_relationships(
        self,
        source_label: Label,
        target_label: Label
    ):

        query = f"""
        MATCH (s:{source_label.value})-[r]->(t:{target_label.value})

        RETURN
            s.name AS source,
            type(r) AS relationship,
            t.name AS target

        ORDER BY source, relationship, target
        """

        return self.db.execute_query(query)

    def update_relationship(
        self,
        source_label: Label,
        old_source: str,
        old_relationship: Relationship,
        old_target: str,
        new_source: str,
        new_relationship: Relationship,
        new_target: str,
        target_label: Label
    ):

        if not isinstance(old_relationship, Relationship):
            raise ValueError("Invalid old relationship type")

        if not isinstance(new_relationship, Relationship):
            raise ValueError("Invalid new relationship type")

        query = f"""
        MATCH (s:{source_label.value} {{name: $old_source}})
              -[r:{old_relationship.value}]->
              (t:{target_label.value} {{name: $old_target}})

        MATCH (new_s:{source_label.value} {{name: $new_source}})
        MATCH (new_t:{target_label.value} {{name: $new_target}})

        WITH r, new_s, new_t

        DELETE r

        MERGE (new_s)-[new_r:{new_relationship.value}]->(new_t)

        RETURN
            new_s.name AS source,
            type(new_r) AS relationship,
            new_t.name AS target
        """

        params = {
            "old_source": old_source,
            "old_target": old_target,
            "new_source": new_source,
            "new_target": new_target
        }

        return self.db.execute_query(query, params)

    def delete_relationship(
        self,
        source_label: Label,
        source_name: str,
        relationship: Relationship,
        target_label: Label,
        target_name: str
    ):

        query = f"""
        MATCH (s:{source_label.value} {{name: $source}})
              -[r:{relationship.value}]->
              (t:{target_label.value} {{name: $target}})

        DELETE r
        """

        return self.db.execute_query(
            query,
            {
                "source": source_name,
                "target": target_name
            }
        )
