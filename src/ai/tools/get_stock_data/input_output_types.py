from pydantic import BaseModel, Field
from typing import Literal, Union, List, Dict, Any


class StockRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol, e.g., AAPL")
    data_type: Union[
        Literal["open", "High", "Low", "close"], 
        List[Literal["open", "High", "Low", "close"]]
    ] = Field(..., description="Type of price to fetch - can be a single value or list of values")
    number_of_days: int = Field(..., description="Number of days to look back (1-30)")


# class DailyData(BaseModel):
#     date: str
#     # This will contain the requested data types dynamically
#     # e.g., {"open": 150.0, "close": 152.0} or {"High": 155.0, "Low": 148.0}
    
#     class Config:
#         extra = "allow"  # Allow additional fields beyond what's defined


class StockResponse(BaseModel):
    ticker: str
    values: List[Dict[str, Any]] = Field(..., description="List of daily data with date and requested price types")

