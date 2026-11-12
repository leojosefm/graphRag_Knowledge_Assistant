from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:
    """
    Splits cleaned documentation into overlapping chunks suitable
    for embedding and vector search.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",   # Prefer paragraphs
                "\n",     # Then lines
                ". ",     # Then sentences
                " ",      # Then words
                ""        # Finally characters
            ],
            keep_separator=True,
            strip_whitespace=True,
        )

    def chunk(self, document: dict) -> list[dict]:
        """
        Splits a cleaned document into overlapping chunks.
        """

        texts = self.splitter.split_text(document["content"])

        chunks = []

        for chunk_number, text in enumerate(texts, start=1):

            chunks.append(
                {
                    "technology": document["technology"],
                    "url": document["url"],
                    "title": document["title"],
                    "chunk_number": chunk_number,
                    "text": text,
                    "chunk_length": len(text),
                }
            )

        return chunks