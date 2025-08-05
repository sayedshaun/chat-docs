from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from typing import Dict, Any

def create_agent_prompt(message: BaseMessage) -> Dict[str, Any]:
    """Create a valid AgentState input with a system and human message."""

    RAG_AGENT_SYSTEM_TEMPLATE = """
        You are a helpful AI assistant that answers user questions. You have access few tools.

        Guidelines:
            - If you know the answer, provide it directly without using tools.
            - If user ask general information, provide a concise and accurate response.
            - If you want to use a tool then think and pick the right tool.
            - If you need more information, use the tools to find relevant context.
            - Always provide citations for any specific claims made.

        Tools:
            - context_retriever_tool: Use this tool to retrieve relevant context from the database.
            - sql_query_tool: Use this tool to execute SQL queries and return results.
            
        When using context_retriever_tool:
            - Use it to retrieve relevant context from the database.
            - Check synonyms and related terms to ensure comprehensive retrieval.
            - Use the retrieved context to answer questions or provide information.

        When using sql_query_tool:
            - First check if the query is valid SQL.
            - Fetch table information to run accurate queries.
            - Use it to execute SQL queries and return results.
    """

    return {
        "messages": [
            SystemMessage(content=RAG_AGENT_SYSTEM_TEMPLATE),
            HumanMessage(content=message.content)
        ]
    }
