from typing import Any, Dict
from graph.retrieve.retrive_state import GraphState
from graph.retrieve.chains.retrieval_precheck_gate import retrieval_precheck_gate
from dotenv import load_dotenv
load_dotenv()
from utilities import _get

CONFIDENCE_THRESHOLD = 0.65
def retrieval_decision_node(state: GraphState) -> Dict[str, Any]:
    print("---RETREIVE DECISION NODE---")
    retrieval_precheck_gate_input = {
        "user_input": state.raw_text,
    }
    result = retrieval_precheck_gate.invoke(retrieval_precheck_gate_input)

    retrieve = _get(result, "retrieve", False)
    confidence = _get(result, "confidence", 0.0)

    retrieve_from_memory = bool(retrieve and confidence >= CONFIDENCE_THRESHOLD)
    return {"retrieve": retrieve_from_memory}