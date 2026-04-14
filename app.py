import streamlit as st
from database import init_db, save_message, get_history
from engine import process_document, get_llm, retrieve_context
from langchain.agents import create_agent

# Initialize Database
init_db()

# --- LOGIN ---
if "user_id" not in st.session_state:
    st.title("🔐 Agent Login")
    uid = st.text_input("Enter your Unique ID:")
    if st.button("Login"):
        if uid:
            st.session_state.user_id = uid
            st.rerun()
    st.stop()

# --- SIDEBAR ---
st.sidebar.title(f"User: {st.session_state.user_id}")
if st.sidebar.button("Logout"):
    del st.session_state.user_id
    st.rerun()

doc_url = st.sidebar.text_input("🔗 Document URL:", placeholder="https://...")

# --- DOCUMENT PROCESSING ---
if doc_url:
    if st.session_state.get("last_url") != doc_url:
        with st.spinner("Indexing document..."):
            process_document(doc_url)
            st.session_state.last_url = doc_url
            st.session_state.indexed = True

# --- AGENT INITIALIZATION ---
llm = get_llm()
agent = create_agent(llm, tools=[retrieve_context])

# --- CHAT UI ---
st.subheader("Chat Assistant")

# Display History
for role, content in get_history(st.session_state.user_id):
    with st.chat_message(role):
        st.markdown(content)

# Input
if query := st.chat_input("Ask about the document..."):
    if not doc_url:
        st.error("Please provide a URL in the sidebar first!")
    else:
        st.chat_message("user").markdown(query)
        save_message(st.session_state.user_id, "user", query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = agent.invoke({"messages": [("user", query)]})
                ans = response["messages"][-1].content
                st.markdown(ans)
                save_message(st.session_state.user_id, "assistant", ans)