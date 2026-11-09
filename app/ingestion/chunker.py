from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ],
        )

    def chunk(self, document: dict) -> list[dict]:
        """
        Splits a cleaned document into overlapping chunks.
        """

        texts = self.splitter.split_text(
            document["content"]
        )

        chunks = []

        for i, text in enumerate(texts, start=1):

            chunks.append(
                {
                    "technology": document["technology"],
                    "url": document["url"],
                    "title": document["title"],
                    "chunk_number": i,
                    "text": text,
                }
            )

        return chunks