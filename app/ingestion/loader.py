from app.ingestion.chunker import DocumentChunker
from app.models.labels import Label
from app.models.relationship import Relationship
from app.repositories.graph_repository import GraphRepository
from app.embedding.embedding_service import EmbeddingService


class DocumentationLoader:

    def __init__(self):
        self.repo = GraphRepository()
        self.chunker = DocumentChunker()
        self.embedding_service = EmbeddingService()

    def close(self):
        self.repo.close()

    def load(self, documents: list[dict]):

        if not documents:
            return

        for document in documents:

            # Create Document node
            self.repo.create_node(
                label=Label.DOCUMENT,
                properties={
                    "url": document["url"],
                    "title": document["title"]
                },
                identity_key="url"
            )

            # Link Technology -> Document
            self.repo.create_relationship(
                source_label=Label.TECHNOLOGY,
                source_key="name",
                source_value=document["technology"],
                relationship=Relationship.HAS_DOCUMENT,
                target_label=Label.DOCUMENT,
                target_key="url",
                target_value=document["url"]
            )

            # Split document into chunks
            chunks = self.chunker.chunk(document)
            texts = [chunk["text"] for chunk in chunks]
            embeddings = self.embedding_service.embed_batch(texts)

            for chunk, embedding in zip(chunks, embeddings):

                chunk_id = f"{chunk['url']}#{chunk['chunk_number']}"

                # Create Chunk node
                self.repo.create_node(
                    label=Label.CHUNK,
                    properties={
                        "id": chunk_id,
                        "chunk_number": chunk["chunk_number"],
                        "text": chunk["text"],
                        "embedding": embedding
                    },
                    identity_key="id"
                )

                # Link Document -> Chunk
                self.repo.create_relationship(
                    source_label=Label.DOCUMENT,
                    source_key="url",
                    source_value=document["url"],
                    relationship=Relationship.HAS_CHUNK,
                    target_label=Label.CHUNK,
                    target_key="id",
                    target_value=chunk_id
                )