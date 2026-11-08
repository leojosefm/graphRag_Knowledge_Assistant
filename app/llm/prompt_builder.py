class PromptBuilder:

    def build(
        self,
        question: str,
        context: list[dict]
    ) -> str:
        """
        Builds a grounded prompt from the retrieved graph context.
        """

        prompt = []

        prompt.append(
            """
You are an expert Data Engineering assistant.

Answer the user's question ONLY using the supplied context.

If the answer cannot be determined from the context, reply:

"I don't have enough information in the retrieved documentation."

Do not make up information.

Always cite the document title when possible.
"""
        )

        prompt.append(f"\nQuestion:\n{question}\n")

        prompt.append("=" * 80)
        prompt.append("RETRIEVED CONTEXT")
        prompt.append("=" * 80)

        for item in context:

            prompt.append(f"\nTechnology: {item['technology']}")
            prompt.append(f"Document: {item['document']}")
            prompt.append(f"URL: {item['url']}")
            prompt.append(f"Similarity Score: {item['score']:.4f}")

            related = item.get("related_technologies", [])

            if related:

                prompt.append("\nRelated Technologies:")

                for relation in related:

                    if relation["technology"]:

                        prompt.append(
                            f"- {relation['technology']} ({relation['relationship']})"
                        )

            prompt.append("\nDocumentation Chunk:")

            prompt.append(item["text"])

            prompt.append("\n" + "-" * 80)

        prompt.append(
            """

Using ONLY the retrieved context above, answer the user's question.

Include the reasoning from the documentation.

If multiple documents agree, summarize them.

If the answer is not present, clearly say so.
"""
        )

        return "\n".join(prompt)