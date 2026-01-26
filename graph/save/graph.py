from langgraph.graph import StateGraph, END
from graph.save.save_graph_state import GraphState
from graph.save.nodes.normalization import normalize_input_node
from graph.save.nodes.storage_decision import storage_decision_node
from graph.save.nodes.save_postgres import save_postgres_node
from graph.save.nodes.save_milvus import save_milvus_node


graph_builder = StateGraph(GraphState)

graph_builder.add_node("normalize_input", normalize_input_node)
graph_builder.add_node("storage_decision", storage_decision_node)

graph_builder.add_node("save_postgres", save_postgres_node)
graph_builder.add_node("save_milvus", save_milvus_node)

graph_builder.set_entry_point("storage_decision")

graph_builder.add_conditional_edges(
    "storage_decision",
    lambda state: state.storage_intent,
    {
        "STRUCTURED_AND_VECTOR": "normalize_input",
        "VECTOR_ONLY": "save_milvus",
    }
)

graph_builder.add_edge("normalize_input", "save_postgres")
graph_builder.add_edge("save_postgres", "save_milvus")

graph_builder.add_edge("save_milvus", END)

graph = graph_builder.compile()

try:
    graph.get_graph().draw_mermaid_png(output_file_path="save_graph.png")
    print("Graph visualization saved to save_graph.png")
except Exception as e:
    print(f"Could not generate graph PNG: {e}")
