from app.ingestion.sources import DOCUMENTATION_SOURCES
from app.ingestion.crawler import DocumentationCrawler
from app.ingestion.parser import DocumentationParser
from app.ingestion.loader import DocumentationLoader


def main():

    crawler = DocumentationCrawler()
    parser = DocumentationParser()
    loader = DocumentationLoader()

    try:

        for source in DOCUMENTATION_SOURCES:

            print(f"\n{'=' * 60}")
            print(f"Ingesting: {source.technology}")
            print(f"Source: {source.url}")
            print(f"{'=' * 60}")

            # Crawl documentation
            pages = crawler.crawl(source)

            print(f"Downloaded {len(pages)} pages")

            documents = []

            # Parse pages
            for page in pages:

                document = parser.parse(page)

                if document:
                    documents.append(document)

            print(f"Parsed {len(documents)} documents")

            # Load into Neo4j
            loader.load(documents)

            print(f"Loaded {len(documents)} documents")

    finally:

        loader.close()


if __name__ == "__main__":
    main()