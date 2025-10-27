# rag_utils.py
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient # type: ignore
from embeddings.generate_embeddings import generate_jina_embeddings_batch
from retrieval.retrieval import retrieve_relevant_chunks
from llm.llm_handler import modify_question_with_memory, generate_answer, CHAT_LLM
from memory.memory_manager import get_last_questions, insert_interaction

# Load environment variables
load_dotenv()

# Get credentials from environment variables
API_KEY = os.getenv('JINA_API_KEY')
QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')

# Validate environment variables
if not API_KEY or not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("Missing required environment variables. Please check your .env file.")

# Set up your persistent client
qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def answer_query(user_question, top_k=5, user_email="user@test.com", chat_id="chat001",
                 concise=False, max_sentences=2, max_chars=400, return_full=False):
    """
    Retrieve context, generate a full answer using the LLM, store it, and return it.
    - This function now returns the full answer produced by the model (no summarization).
    - Keep 'concise' parameter for compatibility but it is ignored here.
    """
    # retrieval + refinement
    past_questions = get_last_questions(user_email, chat_id, limit=3)
    refined_question = modify_question_with_memory(user_question, past_questions)
    query_embedding = generate_jina_embeddings_batch(API_KEY, [refined_question])[0]
    relevant_chunks = retrieve_relevant_chunks(qdrant, query_embedding, top_k=top_k)

    # build combined context from retrieved chunks
    texts = []
    for c in relevant_chunks:
        if isinstance(c, dict):
            txt = c.get("text") or c.get("content") or (c.get("payload") or {}).get("content")
            if not txt:
                payload = c.get("payload") or {}
                txt = payload.get("content") or payload.get("text")
            if txt:
                texts.append(str(txt).strip())
        else:
            texts.append(str(c).strip())
    combined_context = "\n\n".join(t for t in texts if t)

    # FULL answer generation (ask the model to use ONLY the provided context)
    full_prompt = (
        "Using ONLY the provided context, answer the question below thoroughly.\n"
        "Be factual and do not add information not present in the context.\n\n"
        f"Context:\n{combined_context}\n\nQuestion: {refined_question}\nAnswer:"
    )

    # request a large token budget and non-streaming to reduce truncation risk
    full_answer = generate_answer(CHAT_LLM, relevant_chunks, full_prompt, max_tokens=2048, stream=False)

    # persist the full generated answer
    insert_interaction(user_email, chat_id, user_question, full_answer)

    if return_full:
        return full_answer
    return full_answer


def retrieve(query, top_k=5):
    """
    Convenience wrapper to call retrieval.retrieval.retrieve_relevant_chunks directly.
    """
    query_embedding = generate_jina_embeddings_batch(API_KEY, [query])[0]
    return retrieve_relevant_chunks(qdrant, query_embedding, top_k=top_k)
