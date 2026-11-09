from app.retrieval.hybrid_retriever import HybridRetriever
from app.llm.prompt_builder import PromptBuilder
from app.llm.llm_service import LLMService


class KnowledgeAssistant:

    def __init__(self):

        self.retriever = HybridRetriever()
        self.prompt_builder = PromptBuilder()
        self.llm = LLMService()

    def ask(self, question: str) -> str:
        """
        Retrieves relevant context and generates an answer.
        """

        # Step 1 - Retrieve context
        context = self.retriever.search(question)

        # Step 2 - Build prompt
        prompt = self.prompt_builder.build(
            question=question,
            context=context
        )

        # Step 3 - Ask the LLM
        answer = self.llm.generate(prompt)

        return {
            "question": question,
            "answer": answer,
            "sources": context
        }

    def _print_context(self, context):

        print("\nRetrieved Context")
        print("=" * 80)

        for i, item in enumerate(context, 1):

            print(f"\n[{i}]")
            print(f"Technology : {item['technology']}")
            print(f"Document   : {item['document']}")
            print(f"Chunk      : {item['chunk_number']}")
            print(f"Score      : {item['score']:.4f}")

            print("\nPreview:")
            print(item["text"][:250])

    def close(self):
        self.retriever.close()