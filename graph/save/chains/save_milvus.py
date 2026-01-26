from dotenv import load_dotenv
load_dotenv()
from configuration import get_embeddings
import os
import time
from graph.save.save_graph_state import NormalizedMemory, GraphState
from pymilvus import CollectionSchema, FieldSchema, DataType, Collection, connections, utility

embeddings = get_embeddings()

# Lazy initialization globals
_milvus_connected = False
_collection = None

def ensure_milvus_connection():
    """Ensure Milvus connection is established (lazy initialization)"""
    global _milvus_connected, _collection
    
    if _milvus_connected:
        return _collection
    
    # Connect to Milvus
    connections.connect(
        alias="default",
        host=os.getenv("MILVUS_HOST", "172.17.0.4"),
        port=os.getenv("MILVUS_PORT", "19530")
    )
    
    # Milvus collection schema
    def get_milvus_schema():
        """Define the Milvus collection schema"""
        return CollectionSchema(
            fields=[
                FieldSchema("id", DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema("embedding", DataType.FLOAT_VECTOR, dim=1536),
                # Foreign key to PostgreSQL
                FieldSchema("postgres_id", DataType.VARCHAR, max_length=64),
                # Routing / filtering
                FieldSchema("category", DataType.VARCHAR, max_length=64),
                FieldSchema("source", DataType.VARCHAR, max_length=4096),
                # Recency
                FieldSchema("created_at", DataType.INT64),
            ],
            description="Manager memory embeddings with metadata"
        )
    
    collection_name = os.getenv("INDEX_NAME", "cortex_memory")
    if collection_name not in utility.list_collections():
        schema = get_milvus_schema()
        _collection = Collection(name=collection_name, schema=schema)
    else:
        _collection = Collection(name=collection_name)
    
    _milvus_connected = True
    return _collection

def build_embedding_text(mem: NormalizedMemory) -> str:
    parts = []

    if mem.title:
        parts.append(f"Title: {mem.title}")

    if mem.summary:
        parts.append(f"Summary: {mem.summary}")

    if mem.entities:
        for entity_type, values in mem.entities.items():
            parts.append(f"{entity_type.capitalize()}: {', '.join(values)}")

    if mem.facts:
        for key, value in mem.facts.items():
            if isinstance(value, list):
                parts.append(f"{key}: {', '.join(map(str, value))}")
            else:
                parts.append(f"{key}: {value}")

    if mem.memory_date:
        parts.append(f"Date: {mem.memory_date.isoformat()}")

    parts.append(f"Source: {mem.source}")

    return "\n".join(parts)


def save_to_milvus(normalized_memory: NormalizedMemory, postgres_id: str) -> str:
    """
    Save NormalizedMemory to Milvus vector store with metadata.
    
    Args:
        normalized_memory: The normalized memory object to save
        postgres_id: The UUID from PostgreSQL to link records
        
    Returns:
        str: The Milvus document ID
    """
    print("---SAVE TO MILVUS---")
    
    collection = ensure_milvus_connection()
    
    mem = normalized_memory
    
    if not mem or not postgres_id:
        raise ValueError("Normalized memory or postgres_id missing")
    
    embedding_text = build_embedding_text(mem)
    vector = embeddings.embed_query(embedding_text)
    
    collection.insert([
        {
            "embedding": vector,
            "postgres_id": postgres_id,
            "category": mem.category[0] if mem.category else "",
            "source": embedding_text,
            "created_at": int(time.time()),
        }
    ])
    
    collection.flush()
    
    print(f"Successfully saved to Milvus with postgres_id: {postgres_id}")
    
    return postgres_id


def save_raw_text_to_milvus(raw_text: str, category: str = "") -> str:
    """
    Save raw text directly to Milvus without structured normalization.
    Used for VECTOR_ONLY storage intent.
    
    Args:
        raw_text: The raw text to embed and save
        category: Optional category for filtering
        source: Source of the text (default: "manager_chat")
        
    Returns:
        str: Empty string (no postgres_id for raw text)
    """
    print("---SAVE RAW TEXT TO MILVUS---")
    
    collection = ensure_milvus_connection()
    
    if not raw_text:
        raise ValueError("Raw text is required")
    
    # Embed the raw text directly
    vector = embeddings.embed_query(raw_text)
    
    result = collection.insert([
        {
            "embedding": vector,
            "postgres_id": "",  # No postgres record for raw text
            "category": category,
            "source": raw_text,
            "created_at": int(time.time()),
        }
    ])
    
    collection.flush()
    
    milvus_id = str(result.primary_keys[0])
    print(f"Successfully saved raw text to Milvus with ID: {milvus_id}")
    
    return milvus_id
