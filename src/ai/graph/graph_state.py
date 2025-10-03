from typing import Literal
from pydantic import BaseModel
from ..tools.get_stock_data import GetStockDataInput, GetStockDataOutput
from ..tools.moving_average import MovingAverageInput, MovingAverageOutput

class AppState(BaseModel):
    request_type: Literal["get_stock_data", "moving_average"] | None = None
    get_stock_data_input: GetStockDataInput | None = None
    moving_average_input: MovingAverageInput | None = None
    result: GetStockDataOutput | MovingAverageOutput | None = None
