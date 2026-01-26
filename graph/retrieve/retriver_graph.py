from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, START, END

from graph.retrieve.retrive_state import GraphState
from graph.retrieve.nodes.agentic_rag_retriver import agentic_rag_retriever
from graph.retrieve.nodes.llm_node import llm_response_node
from graph.retrieve.nodes.retreive_graph_gate import retrieval_decision_node


# Node name constants
RETRIEVAL_DECISION_NODE = "retrieval_decision"
AGENTIC_RAG_RETRIEVER_NODE = "agentic_rag_retriever"
LLM_RESPONSE_NODE = "llm_response"


# Create the graph
graph = StateGraph(GraphState)

# Add nodes
graph.add_node(RETRIEVAL_DECISION_NODE, retrieval_decision_node)
graph.add_node(AGENTIC_RAG_RETRIEVER_NODE, agentic_rag_retriever)
graph.add_node(LLM_RESPONSE_NODE, llm_response_node)

# Entry point
graph.add_edge(START, RETRIEVAL_DECISION_NODE)

# Conditional routing
def retrieval_decision_edge(state: GraphState) -> str:
    return (
        AGENTIC_RAG_RETRIEVER_NODE
        if getattr(state, "retrieve", False)
        else LLM_RESPONSE_NODE
    )

graph.add_conditional_edges(
    RETRIEVAL_DECISION_NODE,
    retrieval_decision_edge,
    {
        AGENTIC_RAG_RETRIEVER_NODE: AGENTIC_RAG_RETRIEVER_NODE,
        LLM_RESPONSE_NODE: LLM_RESPONSE_NODE,
    },
)

# Terminal edges
graph.add_edge(AGENTIC_RAG_RETRIEVER_NODE, END)
graph.add_edge(LLM_RESPONSE_NODE, END)

# Compile
retriever_graph = graph.compile()

# Visualize
retriever_graph.get_graph().draw_mermaid_png(output_file_path="save_graph.png")
