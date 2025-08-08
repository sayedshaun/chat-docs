# agent.py

import re
from typing import Sequence
from langchain.agents import initialize_agent, AgentExecutor, AgentType, create_react_agent
from .provider import llm
from .utils import calculate_execution_time
from langchain_core.language_models import LanguageModelLike
from langchain_core.tools import BaseTool
import logging

logger = logging.getLogger(__name__)


@calculate_execution_time
def create_rag_agent(
    llm: LanguageModelLike, tools: Sequence[BaseTool], verbose: bool = False
    ) -> AgentExecutor:
    """Create a RAG agent for the RAG system."""
    agent =  initialize_agent(
        tools=tools, llm=llm, verbose=verbose,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True
    )
    return agent