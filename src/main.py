from .ai import compiled_graph

if __name__ == "__main__":
    # Example 1: Get today's closing price
    result1 = compiled_graph.invoke(
        {"request_type": "get_stock_data",
        "get_stock_data_input": {"ticker": "AAPL", "data_type": "close", "number_of_days": 5}}
    )
    print("result 1:", result1)

    # Example 2: Get last 2 years average close, open
    result2 = compiled_graph.invoke(
        {"request_type": "moving_average",
         "moving_average_input": {"ticker": "AAPL", "window_size": 5, "data_type": ["close", "open"], "years_back": 2}}
    )
    print("result 2: ", result2)

