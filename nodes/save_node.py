from typing import Any, Dict
from dotenv import load_dotenv
from graph.state import AgentState
from graph.save.graph import graph
import json
import datetime
load_dotenv()


def save_node(state: AgentState) -> Dict[str, Any]:
    print("---SAVE NODE---")
    
    messages = state["messages"]
    last_message = messages[-1].content if messages else ""
    if isinstance(last_message, list) and last_message:
        last_text = last_message[-1].get("text", "")
    elif isinstance(last_message, dict):
        last_text = last_message.get("text", "")
    else:
        last_text = last_message if isinstance(last_message, str) else ""
    result = graph.invoke({
        "raw_text": last_text,
    })
    if "normalized_memory" in result:
        nm = result["normalized_memory"]
        if hasattr(nm, "dict"):
            nm_dict = nm.dict()
        elif hasattr(nm, "__dict__"):
            nm_dict = dict(nm.__dict__)
        else:
            nm_dict = nm

        if isinstance(nm_dict, dict) and "created_at" in nm_dict:
            if isinstance(nm_dict["created_at"], datetime.datetime):
                nm_dict["created_at"] = nm_dict["created_at"].isoformat()
        result["normalized_memory"] = nm_dict
    if "normalized_memory" in result:
        nm = result["normalized_memory"]
        if hasattr(nm, "dict"):
            result["normalized_memory"] = nm.dict()
        elif hasattr(nm, "__dict__"):
            result["normalized_memory"] = dict(nm.__dict__)

    return {"save_retrieve_response": json.dumps(result)}