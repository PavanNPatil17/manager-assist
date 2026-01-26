from typing import Any, Dict
from dotenv import load_dotenv
from graph.state import AgentState
from chains.general.intent_classifier import intent_classifier

load_dotenv()


def intent_classifier_node(state: AgentState) -> Dict[str, Any]:
    print("---INTENT CLASSIFIER NODE---")
    print("intent classifier input state:", state)
    messages = state["messages"]
    last_message = messages[-1].content if messages else ""
    
    result = intent_classifier.invoke({"user_input": last_message})
    intent = result.intent  # Extract the string value from the Pydantic model
    print("Classified Intent:", intent)
    print("state before intent assignment:", state)
    response = {**state, "intent": intent}
    print("state after intent assignment:", response)
    return {"intent": intent}