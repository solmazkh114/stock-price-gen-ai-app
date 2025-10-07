from pydantic import BaseModel, Field
from typing import Literal, Union, List, Dict, Any


class GetStockDataInput(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol, e.g., AAPL")
    data_type: Union[
        Literal["open", "high", "low", "close"], 
        List[Literal["open", "high", "low", "close"]]
    ] = Field(..., description="Type of price to fetch - can be a single value or list of values")
    number_of_days: int = Field(..., description="Number of days to look back (1-30)")


class GetStockDataOutput(BaseModel):
    ticker: str
    values: List[Dict[str, Any]] = Field(..., description="List of daily data with date and requested price types")
