from collections import deque
from importlib.resources import path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from datetime import datetime

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

            # to avoid infinite loops, keep track of visited URLS
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
                    "html": html,
                    "crawl_date": datetime.utcnow().isoformat(),
                    "crawl_depth": depth,
                    "domain": urlparse(current_url).netloc,
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
                    absolute_url,
                    source.scope_path
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
        candidate_url: str,
        scope_path: str = "",
    ) -> bool:

        root = urlparse(root_url)
        candidate = urlparse(candidate_url)

        # Same website only
        if root.netloc != candidate.netloc:
            return False

        # Stay within the documentation subtree
        root_path = root.path.rstrip("/")

        if scope_path and not candidate.path.startswith(root_path):
            return False

        # Ignore page anchors
        if candidate.fragment:
            return False

        # Ignore non-web links
        if candidate.scheme not in ("http", "https"):
            return False

        path = candidate.path.lower()

        # Ignore documentation sections that aren't useful
        ignored_paths = (
            "/api/",
            "/javadoc/",
            "/scala/",
            "/java/",
            "/python/",
            "/r/",
            "/search",
            "/downloads",
            "/release",
        )

        if any(ignore in path for ignore in ignored_paths):
            return False

        # Ignore static assets
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
            ".gz",
        )

        if path.endswith(ignored_extensions):
            return False

        return True