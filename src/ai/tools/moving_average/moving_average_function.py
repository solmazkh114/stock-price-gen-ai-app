import yfinance as yf
from .input_output_types import MovingAverageInput, MovingAverageOutput
from langchain.tools import tool
from langgraph.prebuilt import ToolNode
from loguru import logger


@tool
def moving_average_tool_function(input: MovingAverageInput) -> MovingAverageOutput:
    """Calculate moving averages for stock data from Yahoo Finance."""
    logger.info("moving average tool is called")
    stock = yf.Ticker(input.ticker)
    # Convert number of days to yfinance period format
    period = f"{input.years_back}y"
    hist = stock.history(period=period)

    logger.info("data fetched for {ticker} for period {period}", ticker=input.ticker, period=period)

    logger.info("hist:\n {hist}", hist=hist)

    if hist.empty:
        raise ValueError("No data found")
    
    if type(input.data_type)== str:
        input.data_type = [input.data_type]

    for dtype in input.data_type:
        hist['moving_avg_' + dtype] = hist[dtype.capitalize()].rolling(window=input.window_size).mean()
        hist = hist.dropna(subset=['moving_avg_' + dtype])

    logger.info("hist after moving avg\n: {hist}", hist=hist)

    values = {}

    for dtype in input.data_type:
        key = str(dtype.capitalize())
        values[key] = {}
        for day in range(len(hist)):
            values[key][str(hist.index[-day].date())] = round(float(hist.iloc[-day]['moving_avg_' + dtype]), 2)

    return MovingAverageOutput(
        ticker=input.ticker,
        values=values
    )

moving_average_tool_node = ToolNode([moving_average_tool_function])

#print(moving_average_function(MovingAverageInput(ticker="AAPL", window_size=5, data_type=["close", "open"], years_back=2)))