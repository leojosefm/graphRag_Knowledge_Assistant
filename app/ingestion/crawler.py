from collections import deque
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class DocumentationCrawler:

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def crawl(self, source):
        """
        Crawls a documentation website.

        Returns:
            [
                {
                    "technology": "...",
                    "url": "...",
                    "html": "..."
                }
            ]
        """

        visited = set()
        queue = deque()

        queue.append((source.url, 0))

        documents = []

        while queue:

            current_url, depth = queue.popleft()

            if current_url in visited:
                continue

            visited.add(current_url)

            print(f"Crawling: {current_url}")

            try:
                response = requests.get(
                    current_url,
                    timeout=self.timeout,
                    headers={
                        "User-Agent": "DataStack-AI Documentation Crawler"
                    }
                )

                response.raise_for_status()

            except Exception as ex:

                print(f"Failed: {current_url}")
                print(ex)
                continue

            html = response.text

            documents.append(
                {
                    "technology": source.technology,
                    "url": current_url,
                    "html": html
                }
            )

            if depth >= source.crawl_depth:
                continue

            soup = BeautifulSoup(html, "html.parser")

            for link in soup.find_all("a", href=True):

                href = link["href"]
                #<a href="sql-programming-guide.html">SQL Guide</a>
                # to  ->  https://spark.apache.org/docs/latest/sql-programming-guide.html 
                absolute_url = urljoin(current_url, href)

                if self._should_visit(
                    source.url,
                    absolute_url
                ):

                    queue.append(
                        (
                            absolute_url,
                            depth + 1
                        )
                    )

        return documents

    def _should_visit(
        self,
        root_url: str,
        candidate_url: str
    ) -> bool:

        root = urlparse(root_url)
        candidate = urlparse(candidate_url)

        # Same website only
        if root.netloc != candidate.netloc:
            return False

        # Ignore anchors
        if "#" in candidate_url:
            return False

        # Ignore mailto/javascript
        if candidate.scheme not in ("http", "https"):
            return False

        # Ignore assets
        ignored_extensions = (
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".svg",
            ".css",
            ".js",
            ".ico",
            ".pdf",
            ".zip",
            ".tar",
            ".gz"
        )

        if candidate.path.lower().endswith(ignored_extensions):
            return False

        return True