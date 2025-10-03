from .graph_state import graph, AppState
from .nodes import get_stock_data_node, moving_average_node

# Create a routing node that decides which action to take
def router_node(state: AppState) -> AppState:
    """Router node that calls the appropriate function based on request type"""
    if state.request_type == "get_stock_data":
        return get_stock_data_node(state)
    elif state.request_type == "stock_data_ma":
        return moving_average_node(state)
    else:
        # Default to stock data if no request type specified
        return get_stock_data_node(state)

# Add only the router node
graph.add_node("router", router_node)

# Set the router as the entry point
graph.set_entry_point("router")

# Compile the graph
app = graph.compile()
