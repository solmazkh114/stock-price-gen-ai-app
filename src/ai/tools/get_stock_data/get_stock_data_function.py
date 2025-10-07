import yfinance as yf
from langchain.tools import tool
from langgraph.prebuilt import ToolNode
from .input_output_types import GetStockDataInput, GetStockDataOutput
from loguru import logger
from typing import Union, List

@tool(args_schema=GetStockDataInput)
def get_stock_data_tool_function(ticker: str, data_type: Union[str, List[str]], number_of_days: int) -> GetStockDataOutput:
    """Fetch historical stock data from Yahoo Finance."""
    logger.info("get stock data tool is called")
    stock = yf.Ticker(ticker)
    # Convert number of days to yfinance period format
    period = f"{number_of_days}d"
    hist = stock.history(period=period)

    if hist.empty:
        raise ValueError("No data found")
    
    logger.info("data fetched for {ticker} for period {period}", ticker=ticker, period=period)

    if type(data_type) == str:
        data_type = [data_type]

    values = []

    for day in range(1, number_of_days + 1):
        daily_dict = {}
        daily_dict["date"] = str(hist.index[-day].date())
        for dtype in data_type:
            daily_dict[dtype] = round(float(hist.iloc[-day][dtype.capitalize()]), 2)
        values.append(daily_dict)

    logger.info(f"values:\n{values}")
    return GetStockDataOutput(
        ticker=ticker,
        values=values
    )

get_stock_data_tool_node = ToolNode([get_stock_data_tool_function])