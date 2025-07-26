# executor.py
import re
from typing import Awaitable, Callable, List
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit  
from langchain.agents import AgentExecutor
from langchain_core.runnables.base import Runnable
from .prompt import (
    DOCUMENT_EXECUTOR_PROMPT, 
)
from .provider import llm
from .database import chroma
from .utils import calculate_execution_time
from .state import Message

@calculate_execution_time
def document_executor() -> Callable[[str], Awaitable[str]]:
    retriever = chroma.as_retriever(search_kwargs={"k": 3})
    prompt = DOCUMENT_EXECUTOR_PROMPT

    def retrieval_chain(query: str) -> str:
        docs = retriever.invoke(query)
        context = "\n".join(doc.page_content for doc in docs)
        formatted_prompt = prompt.format(context=context, question=query)
        response = llm.invoke(formatted_prompt)
        return response.content
    return retrieval_chain


def router_executor(question: str) -> dict:
    response = llm.invoke(question)
    return response.content

