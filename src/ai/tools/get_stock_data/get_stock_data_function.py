import yfinance as yf
from datetime import datetime, timedelta
from input_output_types import StockRequest, StockResponse, AverageRequest, AverageResponse


def get_stock_data(input: StockRequest) -> StockResponse:
    stock = yf.Ticker(input.ticker)
    # Convert number of days to yfinance period format
    period = f"{input.number_of_days}d"
    hist = stock.history(period=period)

    print("hist:\n",hist)

    if hist.empty:
        raise ValueError("No data found")

    last_row = hist.iloc[-1]
    print("last_row:\n",last_row)

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
    return StockResponse(
        ticker=input.ticker,
        values=values
    )

print(get_stock_data(StockRequest(ticker="AAPL",  data_type="close", number_of_days=5)))


def average_last_7_days(input: AverageRequest) -> AverageResponse:
    end_date = datetime.today()
    start_date = end_date - timedelta(days=7)

    stock = yf.Ticker(input.ticker)
    hist = stock.history(start=start_date, end=end_date)

    if hist.empty:
        raise ValueError("No data found")

    avg_close = hist["Close"].mean()

    return AverageResponse(
        ticker=input.ticker,
        average_close_last_7_days=round(float(avg_close), 2)
    )