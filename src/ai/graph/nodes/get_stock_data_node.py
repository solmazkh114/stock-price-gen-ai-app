from ..graph_state import AppState
from ...tools.get_stock_data import get_stock_data_function
from loguru import logger

def get_stock_data_node(state: AppState) -> AppState:
    """Node for processing stock data requests"""
    logger.info("get_stock_data_node is called")
    state.result = get_stock_data_function(state.get_stock_data_input)
    return state