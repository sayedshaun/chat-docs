# tools.py
from langchain.tools import tool
from .database import vectorstore, sqldatabase

@tool
def context_retriever_tool(query: str) -> str:
    """Retrieve relevant context from the database based on the query.
    Args:
        query (str): The query string to search for.
    Returns:
        str: The context retrieved from the database.
    """
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)
    context = "\n".join(doc.page_content for doc in docs)
    return context


@tool
def sql_query_tool(query: str) -> str:
    """Execute a SQL query and return the results.
    Args:
        query (str): The SQL query to execute.
    Returns:
        str: The results of the SQL query.
    """
    try:
        result = sqldatabase.run(query)
        return result if isinstance(result, str) else str(result)
    except Exception as e:
        return f"SQL execution error: {str(e)}"



TOOLS = [context_retriever_tool, sql_query_tool]

__all__ = ["TOOLS"]


