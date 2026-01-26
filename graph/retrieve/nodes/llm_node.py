from typing import Any, Dict
from graph.retrieve.retrive_state import GraphState
from dotenv import load_dotenv
load_dotenv()
from configuration import get_llm

def llm_response_node(state: GraphState) -> Dict[str, Any]:
    print("---LLM RESPONSE NODE---")
    llm = get_llm()
    response = llm.invoke(state.raw_text)
    print("LLM Response:", response.content)
    return {"llm_result": response.content}