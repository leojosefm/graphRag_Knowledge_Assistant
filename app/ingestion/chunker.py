class DocumentChunker:

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, document: dict) -> list[dict]:
        """
        Splits a parsed document into fixed-size chunks.
        """

        content = document["content"]

        chunks = []

        step = self.chunk_size - self.chunk_overlap

        for i in range(0, len(content), step):

            chunk_text = content[i:i + self.chunk_size]

            chunks.append(
                {
                    "technology": document["technology"],
                    "url": document["url"],
                    "title": document["title"],
                    "chunk_number": len(chunks) + 1,
                    "text": chunk_text
                }
            )

        return chunks