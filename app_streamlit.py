import streamlit as st
import datetime
from rag_utils import answer_query

st.set_page_config(page_title="RAG — ReadyTensor Publications", layout="wide")

# --- session state ---
if "chat_history" not in st.session_state:
    # list of {"q": str, "a": str, "ts": str}
    st.session_state.chat_history = []
if "show_history" not in st.session_state:
    st.session_state.show_history = False
if "load_question" not in st.session_state:
    st.session_state.load_question = ""

# Header with title and a top-right Chat history toggle button
hdr_col, btn_col = st.columns([9, 1])
with hdr_col:
    st.title("📚 RAG Assistant — ReadyTensor Publications")
with btn_col:
    if st.button("Chat history"):
        st.session_state.show_history = not st.session_state.show_history

# Main layout: left = chat, right = history panel (hidden unless toggled)
col_main, col_side = st.columns([3, 1])

with col_side:
    if st.session_state.show_history:
        st.markdown("### Chat History")
        if not st.session_state.chat_history:
            st.info("No chat history yet.")
        else:
            # display items newest first
            for i, item in enumerate(reversed(st.session_state.chat_history), 1):
                st.markdown(f"**{i}. [{item['ts']}]**")
                st.write(f"**Q:** {item['q']}")
                st.write(f"**A:** {item['a']}")
                cols = st.columns([3,1])
                with cols[0]:
                    if st.button(f"Load Q #{i}", key=f"load_{i}"):
                        # map displayed index back to original index
                        orig_idx = len(st.session_state.chat_history) - i
                        st.session_state.load_question = st.session_state.chat_history[orig_idx]["q"]
                        # keep history visible after action
                with cols[1]:
                    if st.button(f"Re-run #{i}", key=f"rerun_{i}"):
                        orig_idx = len(st.session_state.chat_history) - i
                        q_re = st.session_state.chat_history[orig_idx]["q"]
                        with st.spinner("Re-running question..."):
                            ans = answer_query(q_re, top_k=5, concise=False)
                        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state.chat_history.append({"q": q_re, "a": ans, "ts": ts})
                        # no explicit rerun call; Streamlit will rerun on button click

with col_main:
    st.markdown("### Chat")

    # chat area
    chat_area = st.container()
    with chat_area:
        # BUBBLE STYLES
        st.markdown(
            """
            <style>
            .chat-wrap { max-width: 880px; margin: 0; }
            .bubble { padding:12px 16px; border-radius:16px; margin:6px 0; display:inline-block; max-width:75%; }
            .user { background:#e6f0ff; color:#000; border-top-left-radius:4px; float:left; clear:both; }
            .assistant { background:#2b2b2b; color:#fff; border-top-right-radius:4px; float:right; clear:both; }
            .ts { font-size:11px; color:#888; margin-top:4px; }
            .chat-row { overflow:auto; padding:4px 0; }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # RENDER MESSAGES AS BUBBLES
        st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
        for item in st.session_state.chat_history:
            q = item["q"]
            a = item["a"]
            ts = item.get("ts", "")

            # user (left)
            st.markdown(
                f'''
<div class="chat-row">
  <div class="bubble user">{q}</div>
  <div class="ts" style="clear:left;">{ts}</div>
</div>
                ''',
                unsafe_allow_html=True,
            )

            # assistant (right)
            st.markdown(
                f'''
<div class="chat-row">
  <div class="bubble assistant">{a}</div>
  <div class="ts" style="text-align:right; clear:right;">{ts}</div>
</div>
                ''',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # Input area: use load_question if user loaded one from history
    try:
        default_value = st.session_state.load_question or ""
        user_input = st.chat_input("Ask a question about the publications dataset:", key="chat_input")
        if st.session_state.load_question and not user_input:
            st.info("Loaded question ready — paste it into the input or use Re-run from history.")
        if user_input:
            q = user_input.strip()
            if q:
                with st.spinner("Retrieving and generating..."):
                    answer = answer_query(q, top_k=5, concise=False)
                ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.chat_history.append({"q": q, "a": answer, "ts": ts})
                st.session_state.load_question = ""
                # Force an immediate rerun so the chat display updates now
                st.experimental_rerun()
    except Exception:
        # fallback to text_input if chat_input not available
        default = st.session_state.load_question or ""
        txt = st.text_input("Ask a question about the publications dataset:", value=default, key="fallback_input")
        if st.button("Send", key="send_fallback"):
            q = txt.strip()
            if q:
                with st.spinner("Retrieving and generating..."):
                    answer = answer_query(q, top_k=5, concise=False)
                ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.chat_history.append({"q": q, "a": answer, "ts": ts})
                st.session_state.load_question = ""
                # Force rerun so chat bubbles appear immediately
                st.experimental_rerun()
