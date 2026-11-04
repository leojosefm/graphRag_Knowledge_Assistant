from app.models.labels import Label
from app.repositories.graph_repository import GraphRepository
from app.seed.relationships import RELATIONSHIPS
from app.seed.technologies import TECHNOLOGIES
from app.database.schema_manager import SchemaManager


schema = SchemaManager()
schema.create_constraints()
schema.close()

repo = GraphRepository()

# Create all technology nodes
for technology in TECHNOLOGIES:
    repo.create_node(
        Label.TECHNOLOGY,
        {
            "name": technology["name"],
            "category": technology["category"].value,
            "description": technology["description"]
        }
    )



# Create all relationships
for relationship in RELATIONSHIPS:
    repo.create_relationship(
        Label.TECHNOLOGY,
        relationship["source"],
        relationship["relationship"],
        Label.TECHNOLOGY,
        relationship["target"]
    )


repo.close()

