from typing import Any, Dict
from graph.retrieve.retrive_state import GraphState
from dotenv import load_dotenv
load_dotenv()
from graph.retrieve.graph.graph import app

def agentic_rag_retriever(state: GraphState) -> Dict[str, Any]:
    response = app.invoke({"question": state.raw_text})
    return {"generation": response["generation"]}