# workflow.py
from functools import lru_cache
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import MemorySaver
from .state import GraphState
from .agent import document_executor, router_executor
from .utils import calculate_execution_time
import logging
from langchain_core.messages import AIMessage
from typing import Dict, Any, Union

logging.basicConfig(
    level=logging.INFO, filename='info.log', 
    filemode="a", format='[%(levelname)s] %(message)s'
)


def router_executor_node(state: GraphState) -> Dict[str, Union[str, AIMessage]]:
    question = state["question"]
    logging.info(f"question: {question}")
    response = router_executor(state)
    state["answer"] = response["answer"]
    return {"answer": response["answer"]}

def document_executor_node(state: GraphState) -> Dict[str, Union[str, AIMessage]]:        
    doc_chain = document_executor()
    question = state["question"]
    logging.info(f"question: {question}")
    answer = doc_chain(question)
    state["answer"] = answer    
    return {"answer": answer}


@calculate_execution_time
def build_graph() -> CompiledStateGraph[GraphState]:
    graph = StateGraph(GraphState)
    graph.add_node("document_executor_node", document_executor_node)
    graph.add_edge(START, "document_executor_node")
    graph.add_edge("document_executor_node", END)
    compiled_graph = graph.compile(checkpointer=MemorySaver())
    return compiled_graph




