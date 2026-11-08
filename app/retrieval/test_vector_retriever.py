from app.retrieval.vector_retriever import VectorRetriever


def main():

    retriever = VectorRetriever()

    try:
        query = "How does Spark Structured Streaming work?"

        results = retriever.search(
            question=query,
            top_k=5
        )

        print("\nResults")
        print("=" * 80)

        for i, result in enumerate(results, start=1):

            print(f"\nResult {i}")
            print("-" * 80)
            print(f"Score : {result['score']:.4f}")
            print(f"URL   : {result['url']}")
            print(f"Chunk : {result['chunk_number']}")
            print(f"\n{result['text'][:500]}")

    finally:
        retriever.close()


if __name__ == "__main__":
    main()