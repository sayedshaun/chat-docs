# graph.py
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import InMemorySaver
from .state import AgentState
from typing import Dict, Any
from .tools import TOOLS
from .provider import llm
from .agent import create_rag_agent 


def rag_agent_node(state: AgentState) -> Dict[str, Any]:
    """Node that invokes the RAG agent to process the state."""
    message = state["messages"]
    agent = create_rag_agent(llm=llm, tools=TOOLS, verbose=True)
    response = agent.invoke(message)
    return {"messages": [response["output"]]}


def create_graph() -> CompiledStateGraph:
    """ Create the workflow for the RAG agent."""
    checkpointer = InMemorySaver()
    graph = StateGraph(AgentState)
    graph.add_node("rag_agent", rag_agent_node)
    graph.add_edge(START, "rag_agent")
    graph.add_edge("rag_agent", END) 
    compiled_graph = graph.compile(checkpointer=checkpointer)
    return compiled_graph

