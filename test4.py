# create independent nodes for each tool and add thread_id to state to track conversations and history
from typing import TypedDict, Annotated, List, Optional
import operator
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from typing import List
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime

load_dotenv()
##################
from langchain_core.runnables.graph import MermaidDrawMethod

# In-memory conversation storage (in production, use a database)
conversation_store = {}

class AgentState(TypedDict):
    messages: Annotated[List, operator.add]
    thread_id: str

def save_conversation(thread_id: str, messages: List[BaseMessage]):
    """Save conversation to storage"""
    conversation_store[thread_id] = {
        'messages': messages,
        'last_updated': datetime.now()
    }

def load_conversation_history(thread_id: str) -> List[BaseMessage]:
    """Load conversation history for a thread"""
    if thread_id:
        return conversation_store[thread_id]['messages']
    return []

def create_new_thread() -> str:
    """Create a new conversation thread"""
    return str(uuid.uuid4())

@tool
def get_weather(city: str) -> str:
    """Get current weather information for a given city."""
    # Mock implementation – replace with real API call in production
    weather_data = {
        "New York": "Sunny, 72°F",
        "London": "Cloudy, 15°C",
        "Tokyo": "Rainy, 22°C"
    }
    return weather_data.get(city, "Weather data not available")

@tool
def calculate_sum(numbers: List[float]) -> float:
    """Calculate the sum of a list of numbers."""
    return sum(numbers)

@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information about a topic."""
    # Mock implementation – replace with a real search if needed
    return f"Wikipedia search results for '{query}': This is sample content about {query}."

# Register the tools
tools = [get_weather, calculate_sum, search_wikipedia]



llm = ChatOpenAI(api_key= os.environ.get("OPENAI_API_KEY"), model="gpt-4.1-nano", temperature=0)
llm_with_tools = llm.bind_tools(tools)

llm_with_tools = llm.bind_tools(tools)
tool_node_get_weather = ToolNode([get_weather])
tool_node_calculate_sum = ToolNode([calculate_sum])
tool_node_search_wikipedia = ToolNode([search_wikipedia])


def call_model(state: AgentState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        # Get the first tool call's name
        tool_name = last_message.tool_calls[0]["name"]
        if tool_name == "get_weather":
            return "get_weather"
        elif tool_name == "calculate_sum":
            return "calculate_sum"  
        elif tool_name == "search_wikipedia":
            return "search_wikipedia"
    return "end"




workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("get_weather", tool_node_get_weather)
workflow.add_node("calculate_sum", tool_node_calculate_sum)
workflow.add_node("search_wikipedia", tool_node_search_wikipedia)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {"get_weather": "get_weather", "calculate_sum": "calculate_sum", "search_wikipedia": "search_wikipedia", "end": END}
)
workflow.add_edge("get_weather", "agent")
workflow.add_edge("calculate_sum", "agent")
workflow.add_edge("search_wikipedia", "agent")

app = workflow.compile()


#####################################################################
# Save the graph as PNG file
try:
    graph_png = app.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.API,
    )
    
    # Save to file
    with open("langgraph_visualization2.png", "wb") as f:
        f.write(graph_png)
    
    print("✅ Graph saved as 'langgraph_visualization2.png'")
    print("You can open this file with any image viewer to see your LangGraph!")
    
except Exception as e:
    print(f"❌ Error saving graph: {e}")
    print("Make sure you have an internet connection for the Mermaid API")

######################################

def run_agent(query: str, thread_id: Optional[str] = None):
    """Run the agent with a given query and optional thread_id for conversation history."""
    if thread_id:
        print(f"💬 Continuing conversation thread: {thread_id}")
        # Load conversation history and add new message
        history = load_conversation_history(thread_id)
        #print("history:", history)
        initial_messages = history + [HumanMessage(content=query)]
    else:
        thread_id = create_new_thread()
        print(f"🆕 Created new conversation thread: {thread_id}")
        # Start with fresh conversation
        initial_messages = [HumanMessage(content=query)]
    
    initial_state = {
        "messages": initial_messages,
        "thread_id": thread_id
    }
    
    try:
        result = app.invoke(initial_state)
        
        # Save the complete conversation state after workflow completion
        save_conversation(thread_id, result["messages"])
        
        # Get the final response
        final_response = result["messages"][-1].content
        for i in range(len(result["messages"])):
            print("*"*50)
            print("type of message:", type(result["messages"][i]))
            print(f"Message {i}: {result['messages'][i]}")
        return final_response, thread_id
    except Exception as e:
        print(f"Error during agent run: {e}")
        return f"Error: {e}", thread_id


# # Example 1: Multiple separate conversations
# print("=== EXAMPLE 1: Separate Conversations ===")
# queries = [
#     "What's the weather like in New York?",
#     "Calculate the sum of 10, 25, and 37",
#     "Search Wikipedia for information about artificial intelligence"
# ]

# for query in queries:
#     print(f"Query: {query}")
#     response, thread_id = run_agent(query)
#     print(f"Response: {response}")
#     print("-" * 50)

print("\n" + "="*60)
print("=== EXAMPLE 2: Conversation with History ===")

# Example 2: Conversation with history
conversation_thread = None

# First message in conversation
print("👤 User: What's the weather like in New York?")
response, conversation_thread = run_agent("What's the weather like in New York?", conversation_thread)
print(f"🤖 Assistant: {response}")
print()

# Second message - should remember context
print("👤 User: What about London?")
response, conversation_thread = run_agent("What about London?", conversation_thread)
print(f"🤖 Assistant: {response}")
print()

# Third message - asking about the previous results
print("👤 User: Which city has better weather between those two?")
response, conversation_thread = run_agent("Which city has better weather between those two?", conversation_thread)
print(f"🤖 Assistant: {response}")



