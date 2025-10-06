from typing import TypedDict, Annotated, List
import operator


class AgentState(TypedDict):
    messages: Annotated[List, operator.add]
    thread_id: str