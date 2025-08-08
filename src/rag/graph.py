# graph.py
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AIMessage
from .state import AgentState
from typing import Dict, Any
from .tools import TOOLS
from .provider import llm
from .agent import create_rag_agent 
from .prompt import create_agent_prompt


async def rag_agent_node(state: AgentState) -> Dict[str, Any]:
    """Node that invokes the RAG agent to process the state."""
    message = state["messages"]
    agent = create_rag_agent(llm=llm, tools=TOOLS, verbose=False)
    response = await agent.ainvoke(message)
    message = AIMessage(content=response["output"])
    return {"messages": [message]}


async def react_agent_node(state: AgentState) -> Dict[str, Any]:
    """Node that invokes the React agent to process the state."""
    message = state["messages"]
    agent = await create_react_agent(model=llm, tools=TOOLS)
    response = await agent.ainvoke({"messages": message})
    message = response["messages"][-1]
    return {"messages": [message]}


async def create_graph() -> CompiledStateGraph[AgentState]:
    """ Create the workflow for the RAG agent."""
    checkpointer = InMemorySaver()
    graph = StateGraph(AgentState)
    graph.add_node("rag_agent_node", rag_agent_node)
    graph.add_edge(START, "rag_agent_node")
    graph.add_edge("rag_agent_node", END) 
    compiled_graph = graph.compile(checkpointer=checkpointer)
    return compiled_graph

