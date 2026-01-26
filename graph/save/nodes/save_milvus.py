from graph.save.save_graph_state import GraphState
from graph.save.chains.save_milvus import save_to_milvus, save_raw_text_to_milvus
from typing import Any, Dict


def save_milvus_node(state: GraphState) -> Dict[str, Any]:
    print("---SAVE TO MILVUS NODE---")
    print(state)
    print("raw text:", state.raw_text)
    if state.storage_intent == "VECTOR_ONLY" and state.raw_text and len(state.raw_text.strip()) > 0:
        milvus_id = save_raw_text_to_milvus(
            raw_text=state.raw_text,
            category=state.normalized_memory.category[0] if state.normalized_memory and state.normalized_memory.category else "",
        )
        return {"storage_status": {"milvus": "success"}} if milvus_id else {"storage_status": {"milvus": "failure"}}

    if not state.normalized_memory:
        print("No normalized memory to save to Milvus")
        return {"storage_status": {"milvus": "no_normalized_memory"}}
    
    postgres_id = getattr(state, "postgres_id", "")
    
    if not postgres_id:
        print("Warning: No postgres_id found in state")
        return {"storage_status": {"milvus": "no_postgres_id"}}
    
    milvus_id = save_to_milvus(state.normalized_memory, postgres_id)
    
    return {"storage_status": {"milvus": "success"} if milvus_id else {"milvus": "failure"}}