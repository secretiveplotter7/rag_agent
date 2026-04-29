# Local RAG Agent with Ollama & Streamlit

A professional, local-first Retrieval-Augmented Generation (RAG) agent. This application allows users to log in with a unique ID, index web documents via URL, and chat with an AI assistant that has "memory" of both the document and the conversation history.

---

## 🛠️ Prerequisites

Before running the application, ensure you have the following installed:

1.  **Python 3.11 or 3.12** (Recommended for stability).
2.  **Ollama:** [Download Ollama here](https://ollama.com/).
3.  **Local Models:** Once Ollama is installed, run these commands in your terminal to download the necessary models:
    ```bash
    ollama pull llama3.1
    ollama pull nomic-embed-text
    ```

---

## 🚀 Getting Started

Follow these steps to set up the project on your local machine:

### 1. Project Setup
Create a project folder and navigate into it:
```bash
mkdir rag-agent-app
cd rag-agent-app
```
### 2. Virtual Environment
Create and activate a virtual environment to keep your dependencies isolated:
```bash
# Create the environment
python -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Activate it (Windows)
# venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install streamlit beautifulsoup4 langchain langchain-ollama langchain-community langchain-core langchain-text-splitters
```
### 4. Run the App
```bash
streamlit run app.py
```

## ⚙️ Configuration
The project is designed with Separation of Concerns:

- LLM Selection: To change the reasoning model, edit get_llm() in engine.py (e.g., change llama3.1 to gemma2).

- Embedding Selection: By default, it uses HuggingFace models, update get_embeddings() in engine.py to change it if required.

- Chunking: You can adjust the chunk_size and chunk_overlap in engine.py to optimize how the agent "reads" longer or shorter articles.

### 📝 Usage
1. Login: Enter any Unique ID. This ID acts as your "account" key.

2. Paste URL: In the sidebar, paste a link to a blog post, news article, or documentation.

3. Chat: Ask questions like "What are the main points of this article?" or "Explain the specific methodology used."

4. Persistent History: Even if you close the app, logging back in with the same ID will retrieve your previous chat history from the SQLite database.

5. Multi-Document: If you paste a new URL, the agent will re-index and begin answering based on the new context.

## 📂 Project Structure

```text
rag-agent-app/
├── app.py              # Main Entry point (Streamlit UI)
├── engine.py           # Core RAG & Agent Logic (LangChain/Ollama)
├── database.py         # SQLite Database handlers
├── requirements.txt    # Project dependencies
└── readme.md           # Project documentation