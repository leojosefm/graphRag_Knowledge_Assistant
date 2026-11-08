from app.retrieval.hybrid_retriever import HybridRetriever


def main():

    retriever = HybridRetriever()

    try:

        results = retriever.search(
            question="How does Spark work with Iceberg?",
            top_k=3
        )

        print("\nResults")
        print("=" * 80)

        for i, result in enumerate(results, start=1):

            print(f"\nResult #{i}")
            print("-" * 80)

            print(f"Technology : {result['technology']}")
            print(f"Document   : {result['document']}")
            print(f"Chunk      : {result['chunk_number']}")
            print(f"Score      : {result['score']:.4f}")
            print(f"URL        : {result['url']}")

            print("\nRelated Technologies:")

            if result["related_technologies"]:
                for related in result["related_technologies"]:
                    print(
                        f"  - {related['technology']} "
                        f"({related['relationship']})"
                    )
            else:
                print("  None")

            print("\nChunk Text")
            print(result["text"][:300])
            print("...")

    finally:
        retriever.close()


if __name__ == "__main__":
    main()