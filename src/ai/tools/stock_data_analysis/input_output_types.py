from pydantic import BaseModel, Field
from typing import Literal, Union, List, Dict


class MovingAverageInput(BaseModel):
    """
    Input model for moving average calculation requests.
    
    This class defines the required and optional parameters for calculating 
    moving averages of stock price data over a specified time period.
    
    Attributes:
        ticker (str): Stock ticker symbol (e.g., 'AAPL', 'GOOGL', 'TSLA').
                     This is a required field.
        window_size (int, optional): Number of periods to include in the moving average
                                   calculation. Common values are 5, 10, 20, 50, 200.
                                   Defaults to 7.
        years_back (int, optional): Number of years of historical data to fetch
                                  for the analysis. Defaults to 1 year.
        data_type (Union[str, List[str]]): Type(s) of price data to analyze.
                                         Can be a single value or list of values.
                                         Valid options: 'open', 'High', 'Low', 'close'.
                                         This is a required field.
    
    Examples:
        >>> # Basic usage with defaults
        >>> input_data = moving_average_input(
        ...     ticker="AAPL",
        ...     data_type="close"
        ... )
    """
    ticker: str = Field(..., description="Stock ticker symbol, e.g., AAPL")
    window_size: int = Field(default=7, description="Window size for moving average (e.g., 5, 10, 20)")
    years_back: int = Field(default=1, description="Number of years to look back for fetching data")
    data_type: Union[
        Literal["open", "High", "Low", "close"], 
        List[Literal["open", "High", "Low", "close"]]
    ] = Field(..., description="Type of price to fetch - can be a single value or list of values")




class MovingAverageOutput(BaseModel):
    """
    Output model for moving average calculation results.
    
    This class defines the structure of the response containing calculated
    moving averages for the requested stock and time period.
    
    Attributes:
        ticker (str): The stock ticker symbol that was analyzed.
        values (Dict[str, Dict[str, float]]): Nested dictionary structure containing
                                                   the moving average data organized by:
                                                   - key: price type (e.g., 'open', 'close')
                                                   - value: date-value pairs
    
    Data Structure:
        The values field contains data in the following format:
            {
                'open': {
                    '2024-10-03': 150.0,
                    '2024-10-04': 152.0,
                    '2024-10-05': 148.5
                },
                'close': {
                    '2024-10-03': 151.0,
                    '2024-10-04': 153.0,
                    '2024-10-05': 149.2
                }
            }
    """
    ticker: str
    values: Dict[str, Dict[str, float]] = Field(
        ..., 
        description="Dictionary with price types as keys and date-value pairs as nested dictionaries. Format: {'open': {'2024-10-03': 150.0, '2024-10-04': 152.0}, 'close': {'2024-10-03': 151.0, '2024-10-04': 153.0}}"
    ) 
    