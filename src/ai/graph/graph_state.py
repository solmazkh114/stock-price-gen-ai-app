from typing import Literal
from pydantic import BaseModel
from langgraph.graph import StateGraph
from ..tools.get_stock_data import GetStockDataInput, GetStockDataOutput
from ..tools.stock_data_analysis import MovingAverageInput, MovingAverageOutput
# Define LangGraph state

class AppState(BaseModel):
    request_type: Literal["get_stock_data", "stock_data_ma", None] = None
    get_stock_data_input: GetStockDataInput | None = None
    stock_data_ma_input: MovingAverageInput | None = None
    result: GetStockDataOutput | MovingAverageOutput | None = None

graph = StateGraph(AppState)
