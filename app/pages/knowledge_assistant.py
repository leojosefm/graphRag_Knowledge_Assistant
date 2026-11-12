import streamlit as st

from app.llm.knowledge_assistant import KnowledgeAssistant



@st.cache_resource
def get_assistant():
    return KnowledgeAssistant()


@st.cache_data(ttl=3600)
def ask_question(question):
    assistant = get_assistant()
    return assistant.ask(question)

st.title("Knowledge Assistant")

question = st.text_input(
    "Ask a question",
    placeholder="How do I submit a Spark application using Airflow?"
)

if st.button("Ask"):

    with st.spinner("Searching documentation..."):

        result = ask_question(question)

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Sources")

    for source in result["sources"]:
        st.write(f"- {source['document']} ({source['technology']})")

    # assistant.close()