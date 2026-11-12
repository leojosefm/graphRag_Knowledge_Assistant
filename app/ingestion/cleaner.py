from bs4 import BeautifulSoup


class HTMLCleaner:
    """
    Cleans raw HTML and extracts readable documentation text.
    """

    # Common documentation UI elements that add noise to embeddings
    IGNORED_LINES = {
        "Search",
        "Search docs",
        "Previous",
        "Next",
        "Edit this page",
        "View source",
        "Contents",
        "Navigation",
        "Table of contents",
    }

    def clean(self, document: dict) -> dict:
        """
        Converts an HTML document into clean text while preserving
        headings and paragraph boundaries.
        """

        soup = BeautifulSoup(document["html"], "html.parser")

        # Capture the page title before modifying the HTML
        title = (
            soup.title.get_text(strip=True)
            if soup.title
            else document["url"]
        )

        # Remove non-content elements
        for tag in soup([
            "script",
            "style",
            "nav",
            "header",
            "footer",
            "aside",
            "noscript",
            "svg",
        ]):
            tag.decompose()

        # Extract readable text while preserving structure
        content = soup.get_text(
            separator="\n",
            strip=True,
        )

        cleaned_lines = []

        for line in content.splitlines():

            line = line.strip()

            if not line:
                continue

            if line in self.IGNORED_LINES:
                continue

            cleaned_lines.append(line)

        # Preserve paragraph separation for the recursive splitter
        content = "\n\n".join(cleaned_lines)

        return {
            "technology": document["technology"],
            "url": document["url"],
            "title": title,
            "content": content,
        }