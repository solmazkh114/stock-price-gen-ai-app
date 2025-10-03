from .graph_state import AppState
from .nodes import router_node
from langgraph.graph import StateGraph


# create a graph with state
graph = StateGraph(AppState)

graph.add_node("router", router_node)
# Set the router as the entry point
graph.set_entry_point("router")

# Compile the graph
compiled_graph = graph.compile()
