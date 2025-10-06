
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, SystemMessage
from ..ai.graph.graph import compiled_graph
from ..ai.graph.system_prompt import SYSTEM_PROMPT
import uuid
from typing import Optional
from loguru import logger


class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None  # Optional thread ID for context


def chat_handler(request: ChatRequest) -> dict:
    """
    Handle chat requests with automatic thread management.
    LangGraph handles conversation history automatically when thread_id is provided.
    """
    
    # Generate thread_id if not provided (new conversation)
    if not request.thread_id:
        thread_id = str(uuid.uuid4())
        logger.info(f"Created new conversation thread: {thread_id}")

        inputs = {
            "messages": [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=request.message)
            ]
        }
    else:
        thread_id = request.thread_id
        logger.info(f"Continuing conversation thread: {thread_id}")

            # Input state - LangGraph will automatically load chat history for existing threads
        inputs = {
            "messages": [HumanMessage(content=request.message)]
        }

    # Configure LangGraph with thread_id for automatic memory persistence
    config = {
        "configurable": {"thread_id": thread_id}
    }
    

    
    try:
        # Invoke the graph instead of streaming
        logger.info("Starting graph invocation...")

        result = compiled_graph.invoke(inputs, config)

        return {
            "response": result["messages"][-1].content,
            "thread_id": thread_id
        }

    except Exception as e:
        logger.error(f"Error during chat processing: {e}")
        return {
            "error": str(e),
            "thread_id": thread_id
        }

