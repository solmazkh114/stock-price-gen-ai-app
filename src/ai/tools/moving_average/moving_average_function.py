import yfinance as yf
from .input_output_types import MovingAverageInput, MovingAverageOutput
from langchain.tools import tool
from langgraph.prebuilt import ToolNode
from loguru import logger
from typing import Union, List


@tool(args_schema=MovingAverageInput)
def moving_average_tool_function(ticker: str, window_size: int = 7, years_back: int = 1, data_type: Union[str, List[str]] = "close") -> MovingAverageOutput:
    """Calculate moving averages for stock data from Yahoo Finance."""
    logger.info("moving average tool is called")
    stock = yf.Ticker(ticker)
    # Convert number of days to yfinance period format
    period = f"{years_back}y"
    hist = stock.history(period=period)

    logger.info("data fetched for {ticker} for period {period}", ticker=ticker, period=period)

    logger.info("hist:\n {hist}", hist=hist)

    if hist.empty:
        raise ValueError("No data found")
    
    if type(data_type) == str:
        data_type = [data_type]

    for dtype in data_type:
        hist['moving_avg_' + dtype] = hist[dtype.capitalize()].rolling(window=window_size).mean()
        hist = hist.dropna(subset=['moving_avg_' + dtype])

    logger.info("hist after moving avg\n: {hist}", hist=hist)

    values = {}

    for dtype in data_type:
        key = str(dtype.capitalize())
        values[key] = {}
        for day in range(len(hist)):
            values[key][str(hist.index[-day].date())] = round(float(hist.iloc[-day]['moving_avg_' + dtype]), 2)

    logger.info(f"values:\n{values}")

    return MovingAverageOutput(
        ticker=ticker,
        values=values
    )

moving_average_tool_node = ToolNode([moving_average_tool_function])
