'''from langchain_openai import OpenAI # type: ignore

CHAT_LLM = OpenAI()

new_question_modifier = """Your primary task is ..."""  # As previously provided

def modify_question_with_memory(new_question, past_questions):
    if past_questions:
        past_questions_text = " ".join(past_questions)
        system_prompt = f"{new_question_modifier}\nChat history: {past_questions_text}\nLatest question: {new_question}"
        standalone_question = CHAT_LLM.invoke(system_prompt)
    else:
        standalone_question = new_question
    return standalone_question

def generate_answer(llm, relevant_chunks, question):
    context = "\n\n".join(relevant_chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    return llm.invoke(prompt)
'''
'''
from langchain_cohere import Cohere # type: ignore
import os

os.environ["COHERE_API_KEY"] = "TjFX0RisXJk0WvoQ4wfuJYGvyBrHaMTEPMYzpOT5"  # Paste your key here or use dotenv

CHAT_LLM = Cohere()

new_question_modifier = """
Your primary task is to determine if the latest question requires context from the chat history to be understood.

IMPORTANT: If the latest question is standalone and can be fully understood without any context from the chat history or is not related to the chat history, you MUST return it completely unchanged. Do not modify standalone questions in any way.

Only if the latest question clearly references or depends on the chat history should you reformulate it as a complete, standalone legal question. When reformulating:
"""

def modify_question_with_memory(new_question, past_questions):
    if past_questions:
        past_questions_text = " ".join(past_questions)
        system_prompt = f"{new_question_modifier}\nChat history: {past_questions_text}\nLatest question: {new_question}"
        standalone_question = CHAT_LLM.invoke(system_prompt)
    else:
        standalone_question = new_question
    return standalone_question

def generate_answer(llm, relevant_chunks, question):
    context = "\n\n".join(relevant_chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    return llm.invoke(prompt)
'''

from dotenv import load_dotenv
import os
from langchain_cohere import ChatCohere # type: ignore
from langchain_core.messages import HumanMessage # type: ignore

load_dotenv()  # Load environment variables from .env

# The ChatCohere model automatically uses the COHERE_API_KEY from env variables
CHAT_LLM = ChatCohere()

new_question_modifier = """
Your primary task is to determine if the latest question requires context from the chat history to be understood.

IMPORTANT: If the latest question is standalone and can be fully understood without any context from the chat history or is not related to the chat history, you MUST return it completely unchanged. Do not modify standalone questions in any way.

Only if the latest question clearly references or depends on the chat history should you reformulate it as a complete, standalone legal question. When reformulating:
"""

def modify_question_with_memory(new_question, past_questions):
    if past_questions:
        past_questions_text = " ".join(past_questions)
        messages = [
            HumanMessage(content=f"{new_question_modifier}\nChat history: {past_questions_text}\nLatest question: {new_question}")
        ]
        response = CHAT_LLM.invoke(messages)
        standalone_question = response.content
    else:
        standalone_question = new_question
    return standalone_question

def generate_answer(llm, relevant_chunks, question):
    context = "\n\n".join(relevant_chunks)
    prompt = (
        "You are a Q&A assistant for ReadyTensor publications. "
        "Answer ONLY with information directly from the context below. "
        "If the answer is not explicitly in the context, reply: 'I cannot answer from this dataset.'\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
        f"Extracted Answer (quote or paraphrase, not general summary):"
    )
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    return response.content

def generate_answer(model, context_chunks, prompt, max_tokens: int = 1024, stream: bool = False, **kwargs):
    """
    Unified generate function:
      - If `model` exposes `invoke(messages)`, use that (e.g., ChatCohere/ChatCohere-like).
      - Otherwise try OpenAI-compatible ChatCompletion with `openai.ChatCompletion.create`.
    Parameters:
      - model: model object or model name/string for OpenAI clients
      - context_chunks: list of context pieces (not used directly here; prompt already contains context)
      - prompt: final prompt string
      - max_tokens: request token budget (increase to avoid API-side truncation)
      - stream: whether to use streaming (stream=False recommended for full responses)
    Returns:
      - response text (str). On error returns a short error message.
    """
    # Build a single HumanMessage for consistency with langchain-style clients
    messages = [HumanMessage(content=prompt)]

    # If model object supports invoke(), prefer that (langchain/cohere)
    if hasattr(model, "invoke"):
        try:
            resp = model.invoke(messages)
            # resp may be an object with .content or a string
            if hasattr(resp, "content"):
                return resp.content.strip()
            if isinstance(resp, str):
                return resp.strip()
            return str(resp).strip()
        except Exception as e:
            # Fall through to try OpenAI-style client; don't silently swallow error
            err = f"invoke-error: {e}"
            try:
                # continue to OpenAI branch
                pass
            except Exception:
                return err

    # Fallback: OpenAI-style ChatCompletion
    try:
        import openai  # type: ignore
        openai_messages = []
        for m in messages:
            content = getattr(m, "content", str(m))
            openai_messages.append({"role": "user", "content": content})

        resp = openai.ChatCompletion.create(
            model=model,
            messages=openai_messages,
            max_tokens=max_tokens,
            temperature=0.0,
            stream=stream,
            **kwargs
        )

        if stream:
            # Streaming is environment-specific; return empty string here and let caller handle streaming if needed.
            # Alternatively, implement streaming collector if required.
            return ""
        return resp["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"LLM generation error: {e}"

