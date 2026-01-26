from typing import Any, Dict
from dotenv import load_dotenv
from graph.state import AgentState

from graph.retrieve.retriver_graph import retriever_graph
import json
load_dotenv()


def retrieve_node(state: AgentState) -> Dict[str, Any]:
    print("---RETRIEVE NODE---")
    
    messages = state["messages"]
    last_message = messages[-1].content if messages else ""
    print("Last Message:", last_message)
    if isinstance(last_message, list) and last_message:
        last_text = last_message[-1].get("text", "") if isinstance(last_message[-1], dict) else str(last_message[-1])
    elif isinstance(last_message, dict):
        last_text = last_message.get("text", "")
    else:
        last_text = str(last_message) if last_message else ""
    print("Last Text:", last_text)
    result = retriever_graph.invoke({
        "raw_text": last_text,
    })
    return {"save_retrieve_response": json.dumps(result)}