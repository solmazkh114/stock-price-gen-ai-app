from langchain_openai import ChatOpenAI
from ..tools.get_stock_data import get_stock_data_tool_function
from ..tools.moving_average import moving_average_tool_function
from .agent_state import AgentState
import os
from loguru import logger
from dotenv import load_dotenv
load_dotenv()


llm = ChatOpenAI(api_key= os.environ.get("OPENAI_API_KEY"), model="gpt-4.1-nano", temperature=0)
tools = [get_stock_data_tool_function, moving_average_tool_function]
llm_with_tools = llm.bind_tools(tools)


def agent_function(state: AgentState):
    logger.info("Agent is called")
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    logger.info(f"Agent response: {response}")
    return {"messages": [response]}