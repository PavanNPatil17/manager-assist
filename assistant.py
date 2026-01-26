from langgraph.graph import StateGraph, START, END
from typing import Literal, TypedDict

from nodes.save_node import save_node
from nodes.retrieve_node import retrieve_node
from nodes.intent_classifier_node import intent_classifier_node
from nodes.response_shaper import response_shaper_node
from graph.state import AgentState


INTENT_CLASSIFIER = "intent_classifier"
SAVE_NODE = "save"
RETRIEVE_NODE = "retrieve"
RESPONSE_SHAPER = "response_shaper"


graph = StateGraph(AgentState)

graph.add_node(INTENT_CLASSIFIER, intent_classifier_node)
graph.add_node(SAVE_NODE, save_node)
graph.add_node(RETRIEVE_NODE, retrieve_node)
graph.add_node(RESPONSE_SHAPER, response_shaper_node)

# Entry
graph.add_edge(START, INTENT_CLASSIFIER)

# Intent-based routing
def intent_router(state: AgentState) -> str:
    return SAVE_NODE if state["intent"] == "save" else RETRIEVE_NODE

graph.add_conditional_edges(
    INTENT_CLASSIFIER,
    intent_router,
    {
        SAVE_NODE: SAVE_NODE,
        RETRIEVE_NODE: RETRIEVE_NODE,
    },
)

# Both paths converge
graph.add_edge(SAVE_NODE, RESPONSE_SHAPER)
graph.add_edge(RETRIEVE_NODE, RESPONSE_SHAPER)

graph.add_edge(RESPONSE_SHAPER, END)

# Compile
app = graph.compile()