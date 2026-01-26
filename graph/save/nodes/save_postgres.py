from graph.save.save_graph_state import GraphState
from graph.save.chains.save_postgres import save_to_postgres
from typing import Any, Dict
import os
from dotenv import load_dotenv

load_dotenv()


def save_postgres_node(state: GraphState) -> Dict[str, Any]:
    print("---SAVE TO POSTGRES NODE---")
    
    if not state.normalized_memory:
        print("No normalized memory to save")
        return {}
    
    user_id = os.getenv("USER_ID", "testuser")
    org_id = os.getenv("ORG_ID", "testorg")
    
    memory_id = save_to_postgres(state.normalized_memory, user_id, org_id)
    
    return {"postgres_id": memory_id, "storage_status": {"postgres": "success"}}