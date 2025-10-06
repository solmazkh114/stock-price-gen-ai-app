from .agent_state import AgentState
from .node_names import NodeNames

def graph_condition(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        # Get the first tool call's name
        tool_name = last_message.tool_calls[0]["name"]
        if tool_name == "get_stock_data_tool_function":
            return NodeNames.GET_STOCK_DATA
        elif tool_name == "moving_average_tool_function":
            return NodeNames.MOVING_AVERAGE
    return NodeNames.END