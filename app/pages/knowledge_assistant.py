import streamlit as st

from app.llm.knowledge_assistant import KnowledgeAssistant

st.title("💬 Knowledge Assistant")

question = st.text_input(
    "Ask a question",
    placeholder="How do I submit a Spark application using Airflow?"
)

if st.button("Ask"):

    assistant = KnowledgeAssistant()

    with st.spinner("Searching documentation..."):

        result = assistant.ask(question)

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Sources")

    for source in result["sources"]:
        st.write(f"- {source['document']} ({source['technology']})")

    assistant.close()