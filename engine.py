import bs4
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools import tool
# from langchain.agents import create_agent

class GlobalStore:
    v_store = None

@tool
def retrieve_context(query: str) -> str:
    """Search the document for information to answer queries."""
    if GlobalStore.v_store is None:
        return "No document has been indexed yet."
    retrieved_docs = GlobalStore.v_store.similarity_search(query, k=5)
    return "\n\n".join(doc.page_content for doc in retrieved_docs)

def get_llm():
    return ChatOllama(model="llama3.1", temperature=0)

def get_embeddings():
    model_name = "BAAI/bge-small-en-v1.5"
    encode_kwargs = {'normalize_embeddings': True} # Recommended for BGE models
    return HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs=encode_kwargs
    )

def process_document(url):
    embeddings = get_embeddings()
    vector_store = InMemoryVectorStore(embeddings)
    
    # bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))
    # loader = WebBaseLoader(web_paths=(url,), bs_kwargs={"parse_only": bs4_strainer})
    loader = WebBaseLoader(
        web_paths=(url,),
        # Some sites block basic crawlers; adding a header helps
        header_template={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    )
    docs = loader.load()
    
    if not docs or len(docs[0].page_content.strip()) < 100:
        return "Error: Could not extract meaningful text from this URL."

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)
    vector_store.add_documents(documents=all_splits)
    GlobalStore.v_store = vector_store
    return vector_store