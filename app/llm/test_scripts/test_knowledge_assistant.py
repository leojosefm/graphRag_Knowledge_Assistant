from app.llm.knowledge_assistant import KnowledgeAssistant


def main():

    assistant = KnowledgeAssistant()

    try:

        result = assistant.ask(
            "How do I submit a Spark application using Airflow?",
            debug=True
        )


        print("\nAnswer")
        print("=" * 80)
        print(result["answer"])

        print("\nSources")
        print("=" * 80)

        for source in result["sources"]:

            print(f"- {source['document']} ({source['technology']})")

    finally:
        assistant.close()


if __name__ == "__main__":
    main()