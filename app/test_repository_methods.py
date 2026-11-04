from app.models.labels import Label
from app.repositories.graph_repository import GraphRepository


repo = GraphRepository()

print(repo.get_all_nodes(Label.TECHNOLOGY))

repo.close()