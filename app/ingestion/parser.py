from bs4 import BeautifulSoup


class DocumentationParser:

    def parse(self, raw_document: dict) -> dict:
        """
        Converts raw HTML into a clean document.

        Input:
        {
            "technology": "...",
            "url": "...",
            "html": "..."
        }

        Output:
        {
            "technology": "...",
            "url": "...",
            "title": "...",
            "content": "..."
        }
        """

        html = raw_document["html"]

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        # ---------------------------------------------------------
        # Remove unwanted HTML
        # ---------------------------------------------------------

        for tag in soup(
            [
                "script",
                "style",
                "noscript",
                "svg",
                "img",
                "header",
                "footer",
                "nav",
                "aside"
            ]
        ):
            tag.decompose()

        # ---------------------------------------------------------
        # Title
        # ---------------------------------------------------------

        if soup.title:
            title = soup.title.get_text(strip=True)
        else:
            title = ""

        # ---------------------------------------------------------
        # Main content
        # ---------------------------------------------------------

        content = soup.get_text(
            separator="\n",
            strip=True
        )

        # Remove blank lines
        lines = [
            line.strip()
            for line in content.splitlines()
            if line.strip()
        ]

        content = "\n".join(lines)

        return {
            "technology": raw_document["technology"],
            "url": raw_document["url"],
            "title": title,
            "content": content
        }