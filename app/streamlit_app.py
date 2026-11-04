
import streamlit as st

st.set_page_config(
    page_title="DataStack AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 DataStack AI")

st.subheader("Knowledge Assistant")

st.write(
    "Welcome to DataStack AI. "
    "Your AI-powered data engineering knowledge assistant."
)

question = st.text_input(
    "Ask a data engineering question",
    placeholder="How do Kafka consumer groups work?"
)

if st.button("Submit"):
    if question:
        st.info(f"Your question: {question}")
        st.warning("Knowledge retrieval is coming soon!")
