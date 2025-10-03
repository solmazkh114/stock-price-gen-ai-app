# Create a routing node that decides which action to take
from .get_stock_data_node import get_stock_data_node
from .moving_average_node import moving_average_node
from ..graph_state import AppState
from loguru import logger

def router_node(state: AppState) -> AppState:
    """Router node that calls the appropriate function based on request type"""
    if state.request_type == "get_stock_data":
        logger.info("Routing to get_stock_data_node")
        return get_stock_data_node(state)
    elif state.request_type == "moving_average":
        logger.info("Routing to moving_average_node")
        return moving_average_node(state)
    else:
        # Default to stock data if no request type specified
        return get_stock_data_node(state)