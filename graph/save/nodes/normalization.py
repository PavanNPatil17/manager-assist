from typing import Any, Dict
from graph.save.save_graph_state import GraphState
from graph.save.chains.normalize import normalize_chain
import os
from dotenv import load_dotenv
from datetime import datetime
from graph.save.constants import ALLOWED_CATEGORIES, ALLOWED_SUBCATEGORIES
load_dotenv()

def normalize_input_node(state: GraphState) -> Dict[str, Any]:
    print("---NORMALIZE NODE---")
    with open("schema.sql", "r") as f:
        db_schema_content = f.read()
    sample_input = {
        "raw_text": state.raw_text,
        "user_id": os.environ.get("USER_ID", "testuser"),
        "org_id": os.environ.get("ORG_ID", "testorg"),
        "source": "manager_chat",
        "db_schema": db_schema_content,
        "allowed_categories": list(ALLOWED_CATEGORIES),
        "allowed_subcategories": {k: list(v) for k, v in ALLOWED_SUBCATEGORIES.items()},
        "now_iso": datetime.now().isoformat()
    }
    result = normalize_chain.invoke(sample_input)
    return {"normalized_memory": result}