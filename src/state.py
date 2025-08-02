# state.py
from typing import TypedDict, List, Annotated
from langgraph.graph.message import BaseMessage, add_messages


class AgentState(TypedDict, total=False):
    messages: Annotated[List[BaseMessage], add_messages]
