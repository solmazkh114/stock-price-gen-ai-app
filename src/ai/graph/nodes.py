from .graph_state import AppState
from ..tools.get_stock_data import get_stock_data_function
from ..tools.stock_data_analysis import moving_average_function

def get_stock_data_node(state: AppState) -> AppState:
    """Node for processing stock data requests"""
    if state.request_type == "get_stock_data":
        state.result = get_stock_data_function(state.get_stock_data_input)
    return state

def moving_average_node(state: AppState) -> AppState:
    """Node for processing moving average requests"""
    if state.request_type == "stock_data_ma":
        state.result = moving_average_function(state.stock_data_ma_input)
    return state