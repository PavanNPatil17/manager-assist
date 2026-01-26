from typing import Any, Dict
from dotenv import load_dotenv

from graph.state import AgentState
from chains.general.response_shaper import response_shaper

load_dotenv()


def response_shaper_node(state: AgentState) -> Dict[str, Any]:
    print("→ RESPONSE_SHAPER_NODE")

    intent = state.get("intent")
    save_retrieve_response = state.get("save_retrieve_response")
    messages = state.get("messages", [])

    result = response_shaper.invoke(
        {
            "intent": intent,
            "save_retrieve_response": save_retrieve_response,
        }
    )

    final_message = result.final_ai_message

    return {
        "final_ai_message": final_message,
        "messages": [
            *messages,
            {"type": "ai", "content": final_message},
        ],
    }
