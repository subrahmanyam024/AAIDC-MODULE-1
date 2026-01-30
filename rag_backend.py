'''# app.py
import streamlit as st
from rag_utils import answer_query, retrieve

st.set_page_config(page_title="RAG — ReadyTensor Publications", layout="wide")
st.title("📚 RAG Assistant — ReadyTensor Publications")

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

col1, col2 = st.columns([2, 1])

with col1:
    q = st.text_input("Ask a question about the publications dataset:")
    if st.button("Ask"):
        if q.strip():
            with st.spinner("Retrieving and generating..."):
                answer = answer_query(q, top_k=5)  # ✅ fixed (no use_openai)
            st.session_state.chat_history.append((q, answer))

    st.markdown("### Chat History")
    for q_hist, a_hist in reversed(st.session_state.chat_history[-20:]):
        st.markdown(f"**Q:** {q_hist}")
        st.markdown(f"**A:** {a_hist}")
        st.markdown("---")

with col2:
    st.markdown("### Retrieved Docs (preview)")
    preview_q = st.text_area("Test retrieval query:", value="What is memory in RAG?")
    if st.button("Retrieve"):
        docs = retrieve(preview_q, top_k=5)
        for d in docs:
            st.markdown(f"**Title:** {d['meta'].get('title')}")
            st.markdown(f"_{d['text'][:400]}..._")
            st.write(f"Distance: {d['distance']:.4f}")
            st.markdown("---")

# Sidebar
st.sidebar.button("Clear chat", on_click=lambda: st.session_state.update(chat_history=[]))
st.sidebar.markdown("### Notes")
st.sidebar.write("""
- Uses OpenRouter API for LLM responses.
- Ensure you set `OPENROUTER_API_KEY` in your `.env`.
- Dataset: ReadyTensor publications (JSON ingested into Chroma).
""")
'''


'''

from embeddings.generate_embeddings import generate_jina_embeddings_batch, main as embed_main # type: ignore
from retrieval.retriever import retrieve_relevant_chunks # type: ignore
from llm.llm_handler import modify_question_with_memory, generate_answer, CHAT_LLM
from memory.memory_manager import get_last_questions, insert_interaction

# Assume API_KEY and other secrets loaded here

if __name__ == "__main__":
    # Step 1: Run embedding if needed
    API_KEY = 'jina_6209620aeb344cfbbb9a8b72bf00602aCd7ZK49F2Ra3lKMSu7tQbfj9y6GO'
    QDRANT_URL = 'https://2e1b44d6-19f8-4bd4-92f6-ae782f1dd015.us-west-1-0.aws.cloud.qdrant.io'
    QDRANT_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.R8GZpGgYx-o-Lw5kbjTNobZJaGziiA1ghDDUySZFVH0'
    embed_main(API_KEY, QDRANT_URL, QDRANT_API_KEY)

    # Step 2: Sample question cycle
    user_email = "user@test.com"
    chat_id = "chat001"
    user_question = "How do I add memory to a chatbot?"

    past_questions = get_last_questions(user_email, chat_id, 3)
    refined_question = modify_question_with_memory(user_question, past_questions)
    # Generate query embedding
    query_embedding = generate_jina_embeddings_batch(API_KEY, [refined_question])[0]
    # Search Qdrant
    relevant_chunks = retrieve_relevant_chunks(qdrant, query_embedding)
    # LLM answer
    answer = generate_answer(CHAT_LLM, relevant_chunks, refined_question)
    print("AI:", answer)
    insert_interaction(user_email, chat_id, user_question, answer)

'''


import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient # type: ignore
from embeddings.generate_embeddings import generate_nomic_embeddings_batch # type: ignore
from retrieval.retrieval import retrieve_relevant_chunks # type: ignore
from llm.llm_handler import modify_question_with_memory, generate_answer, CHAT_LLM
from memory.memory_manager import get_last_questions, insert_interaction

# Load environment variables
load_dotenv()

# Get credentials from environment variables
API_KEY = os.getenv('NOMIC_API_KEY')
QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')

'''API_KEY = 'jina_6209620aeb344cfbbb9a8b72bf00602aCd7ZK49F2Ra3lKMSu7tQbfj9y6GO'
QDRANT_URL = 'https://2e1b44d6-19f8-4bd4-92f6-ae782f1dd015.us-west-1-0.aws.cloud.qdrant.io'
QDRANT_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.R8GZpGgYx-o-Lw5kbjTNobZJaGziiA1ghDDUySZFVH0'
'''

qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def rag_pipeline(user_question, user_email, chat_id):
    past_questions = get_last_questions(user_email, chat_id, limit=3)
    refined_question = modify_question_with_memory(user_question, past_questions)
    print("Refined question:", refined_question)
    query_embedding = generate_nomic_embeddings_batch(API_KEY, [refined_question], model_name="nomic-embed-text-v1")[0]
    relevant_chunks = retrieve_relevant_chunks(qdrant, query_embedding)
    print("Retrieved context:", relevant_chunks)
    answer = generate_answer(CHAT_LLM, relevant_chunks, refined_question)
    insert_interaction(user_email, chat_id, user_question, answer)
    return answer


if __name__ == "__main__":
    # Example run
    user_question = "How do I add memory to my chatbot?"
    user_email = "user@test.com"
    chat_id = "chat001"
    response = rag_pipeline(user_question, user_email, chat_id)
    print("AI:", response)
