from typing import Any, Dict
from graph.save.save_graph_state import GraphState
from graph.save.chains.storage_decision import storage_decision_chain
from dotenv import load_dotenv

load_dotenv()

def storage_decision_node(state: GraphState) -> Dict[str, Any]:
    print("---STORAGE DECISION NODE---")
    print("storage decision input state:", state)
    storage_decision_chain_input = {
        "raw_text": state.raw_text,
    }
    result = storage_decision_chain.invoke(storage_decision_chain_input)
    print("Storage Decision Result:", result)
    # Preserve raw_text in the returned state
    return {
        **result.model_dump(),
        "raw_text": state.raw_text
    }