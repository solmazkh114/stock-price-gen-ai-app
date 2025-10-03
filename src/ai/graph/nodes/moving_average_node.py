from ..graph_state import AppState
from ...tools.moving_average import moving_average_function
from loguru import logger

def moving_average_node(state: AppState) -> AppState:
    """Node for processing moving average requests"""
    logger.info("moving_average_node is called")
    state.result = moving_average_function(state.moving_average_input)
    return state