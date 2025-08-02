import os
from functools import lru_cache
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from .provider import embedding
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"

load_dotenv()

@lru_cache(maxsize=1)
def start_vectorstore_session() -> Chroma:
    return Chroma(
        collection_name="rag_collection",
        embedding_function=embedding,
        persist_directory=os.getenv("VECTOR_DATABASE_URL")
    )

@lru_cache(maxsize=1)
def start_sql_database_session() -> SQLDatabase:
    engine = create_engine(os.getenv("SQL_DATABASE_URL"))
    return SQLDatabase(engine=engine)


vectorstore = start_vectorstore_session()
sqldatabase = start_sql_database_session()

__all__ = ["vectorstore", "sqldatabase"]