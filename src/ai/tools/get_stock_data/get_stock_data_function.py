import yfinance as yf
from langchain.tools import tool
from langgraph.prebuilt import ToolNode
from .input_output_types import GetStockDataInput, GetStockDataOutput
from loguru import logger

@tool
def get_stock_data_tool_function(input: GetStockDataInput) -> GetStockDataOutput:
    """Fetch historical stock data from Yahoo Finance."""
    logger.info("get stock data tool is called")
    stock = yf.Ticker(input.ticker)
    # Convert number of days to yfinance period format
    period = f"{input.number_of_days}d"
    hist = stock.history(period=period)

    if hist.empty:
        raise ValueError("No data found")
    
    logger.info("data fetched for {ticker} for period {period}", ticker=input.ticker, period=period)

    if type(input.data_type)== str:
        input.data_type = [input.data_type]

    values = []

    for day in range(1, input.number_of_days + 1):
        daily_dict = {}
        daily_dict["date"] = str(hist.index[-day].date())
        for dtype in input.data_type:
            daily_dict[dtype] = round(float(hist.iloc[-day][dtype.capitalize()]), 2)
        values.append(daily_dict)

    logger.info(f"values:\n{values}")
    return GetStockDataOutput(
        ticker=input.ticker,
        values=values
    )

get_stock_data_tool_node = ToolNode([get_stock_data_tool_function])