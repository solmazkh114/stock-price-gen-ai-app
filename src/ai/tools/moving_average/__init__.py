"""
Stock Data Analysis Tool

This module provides functionality to analyze stock data including moving averages
and other technical indicators. It includes input/output types and analysis functions.
"""

# Import types
from .input_output_types import (
    MovingAverageInput,
    MovingAverageOutput
)

# Import functions
from .moving_average_function import (
    moving_average_function
)

# Define what gets exported when using "from stock_data_analysis import *"
__all__ = [
    # Types
    "MovingAverageInput",
    "MovingAverageOutput",
    # Functions
    "moving_average_function"
]
