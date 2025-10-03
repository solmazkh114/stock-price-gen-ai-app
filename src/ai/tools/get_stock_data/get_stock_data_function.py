import yfinance as yf
from datetime import datetime, timedelta
from input_output_types import GetStockDataInput, GetStockDataOutput
from loguru import logger


def get_stock_data(input: GetStockDataInput) -> GetStockDataOutput:
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

    print("values:\n",values)
    return GetStockDataOutput(
        ticker=input.ticker,
        values=values
    )

#print(get_stock_data(StockRequest(ticker="AAPL",  data_type=["close", "open"], number_of_days=5)))
