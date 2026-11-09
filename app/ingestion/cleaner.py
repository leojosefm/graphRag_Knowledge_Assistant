from bs4 import BeautifulSoup


class HTMLCleaner:

    def clean(self, document: dict) -> dict:
        """
        Extracts clean text from an HTML document while preserving
        headings and paragraph structure.
        """

        soup = BeautifulSoup(document["html"], "html.parser")

        # Remove unwanted elements
        for tag in soup([
            "script",
            "style",
            "nav",
            "header",
            "footer",
            "aside",
            "noscript"
        ]):
            tag.decompose()

        # Preserve paragraph spacing
        content = soup.get_text(
            separator="\n",
            strip=True
        )

        # Remove excessive blank lines
        lines = [
            line.strip()
            for line in content.splitlines()
            if line.strip()
        ]

        content = "\n\n".join(lines)

        return {
            "technology": document["technology"],
            "url": document["url"],
            "title": soup.title.string if soup.title else document["url"],
            "content": content,
        }