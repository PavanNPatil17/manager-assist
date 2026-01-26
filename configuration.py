from langchain_milvus import Milvus
import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

load_dotenv()

# This is for parallel node execution where each node can import this configuration get_llm() and get_embeddings() to get the configured instances.
def get_llm():
    """Get the configured LLM instance."""
    return AzureChatOpenAI(
        deployment_name="gpt-5/chat/completions",
        model=None,
        temperature=1,
        api_version="2024-10-21",
        azure_endpoint="https://genai-nexus.api.corpinter.net/apikey/",
        api_key=os.environ.get("OPENAI_API_KEY")
    )

def get_embeddings():
    """Get the configured embeddings instance."""
    return AzureOpenAIEmbeddings(
        azure_endpoint="https://genai-nexus.api.corpinter.net/apikey/",
        api_key=os.environ.get("OPENAI_API_KEY"),
        show_progress_bar=True,
        retry_min_seconds=10
    )

# Singleton instances (lazy initialization)
_llm = None
_embeddings = None

def get_shared_llm():
    """Get a shared LLM instance (singleton)."""
    global _llm
    if _llm is None:
        _llm = get_llm()
    return _llm

def get_shared_embeddings():
    """Get a shared embeddings instance (singleton)."""
    global _embeddings
    if _embeddings is None:
        _embeddings = get_embeddings()
    return _embeddings

def get_vector_store():
    """Create and return a Milvus vector store instance using shared embeddings."""
    embeddings = get_shared_embeddings()
    milvus_host = os.environ.get("MILVUS_HOST", "localhost")
    milvus_port = os.environ.get("MILVUS_PORT", "19530")
    milvus_uri = f"http://{milvus_host}:{milvus_port}"
    
    return Milvus(
        embedding_function=embeddings,
        collection_name=os.environ.get("INDEX_NAME"),
        connection_args={
            "uri": milvus_uri
        },
        primary_field="id",
        vector_field="embedding",
        text_field="source",
        auto_id=True
    )