from typing import Any, TypedDict, Optional, List, Dict, Union
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage

class Message(TypedDict):
    role: str
    content: str

class GraphState(TypedDict, total=False):
    question: str
    metadata: Dict[str, Any]
    answer: Optional[str]
