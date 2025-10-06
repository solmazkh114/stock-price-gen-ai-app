from .agent_state import AgentState
from .agent_function import agent_function
from ..tools.get_stock_data import get_stock_data_tool_node
from ..tools.moving_average import moving_average_tool_node
from .graph_condition import graph_condition
from .node_names import NodeNames
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


graph = StateGraph(AgentState)
graph.add_node(NodeNames.AGENT, agent_function)
graph.add_node(NodeNames.GET_STOCK_DATA, get_stock_data_tool_node)
graph.add_node(NodeNames.MOVING_AVERAGE, moving_average_tool_node)

graph.set_entry_point(NodeNames.AGENT)

graph.add_conditional_edges(
    NodeNames.AGENT,
    graph_condition,
    {NodeNames.GET_STOCK_DATA: NodeNames.GET_STOCK_DATA, NodeNames.MOVING_AVERAGE: NodeNames.MOVING_AVERAGE, NodeNames.END: END}
)
graph.add_edge(NodeNames.GET_STOCK_DATA, NodeNames.AGENT)
graph.add_edge(NodeNames.MOVING_AVERAGE, NodeNames.AGENT)

# Add memory for conversation persistence
memory = MemorySaver()
compiled_graph = graph.compile(checkpointer=memory)

