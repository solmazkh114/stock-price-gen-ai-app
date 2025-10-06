# Stock Price Gen-AI Application

This project contains a conversational AI application that assists users with stock price analysis using intelligent agent orchestration and memory-based chat continuity. It aims to build a generative AI application (with Python) that helps users analyze stock market data through natural language conversations. The AI agent can fetch historical stock data, perform technical analysis, and maintain context across multiple interactions within a conversation thread.

## Key Features

### AI Agent Orchestration with LangGraph
- Built using **LangGraph** for sophisticated AI workflow orchestration
- Implements a state-based graph architecture for managing conversation flow
- Conditional routing based on user queries and tool requirements
- Memory persistence using **MemorySaver** for thread-based conversation history

### Tools

1. **Get Stock Data Tool** (`get_stock_data_tool_function`)
   - Fetches historical stock price data from Yahoo Finance
   - Supports multiple data types (open, close, high, low, volume)
   - Configurable time periods (number of days)
   - Returns structured data with dates and corresponding values

2. **Moving Average Tool** (`moving_average_tool_function`)
   - Calculates moving averages for stock price trends
   - Helps identify ascending or descending price patterns
   - Provides technical analysis capabilities

### Conversation Memory
- **Thread-based conversation management** maintains context across multiple user queries
- Each conversation is identified by a unique `thread_id`
- Previous messages are automatically loaded and maintained
- Enables follow-up questions without losing context (e.g., "What about yesterday?" after asking about today's price)

## Technology Stack

- **LangChain** and **LangGraph**: Foundation for building LLM-powered applications and AI agent orchestration and workflow management
- **OpenAI GPT-4.1-nano**: Language model for understanding and responding to queries
- **Pydantic**: Schema definition and type validation for tool inputs and outputs
- **yfinance**: Yahoo Finance API for fetching real-time stock market data
- **FastAPI**: High-performance web framework for the REST API
- **Uvicorn**: ASGI server for running the FastAPI application

## Getting Started

### Installation

1. Clone the repository and create and activate a python virtual environment:

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

4. Running the Application (start the FastAPI server):
```bash
python -m src.main
```

The API will be available at `http://localhost:8000`

##  API Usage

### Chat Endpoint

**POST** `/chat`

Request body:

For the first chat define `thread_id = null` and for continuing the chat and using graph memory, copy & paste the `thread_id` from previous chat.
```json
{
  "message": "What is the Apple stock price for the last 7 days?",
  "thread_id": null 
}
```

### Conversation Flow Example

1. **First message** (creates new thread):
```json
{
  "message": "Get me close stock data for Apple for the last 5 days"
}
```

2. **Follow-up message** (uses same thread_id):
```json
{
  "message": "Is it ascending or descending?",
  "thread_id": "abc123-def456-..."
}
```

### Visualizing the Graph

To visualize the LangGraph structure:
```bash
python visualize_graph.py
```

This generates a PNG diagram showing the agent workflow and tool connections.