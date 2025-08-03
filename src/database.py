import os
from functools import lru_cache
from dotenv import load_dotenv
from chromadb import Client, PersistentClient, HttpClient
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_elasticsearch import ElasticsearchStore
from elasticsearch import Elasticsearch
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from .provider import embedding
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"

load_dotenv()

@lru_cache(maxsize=1)
def _start_vectorstore_session() -> ElasticsearchStore:
    """Initialize the vectorstore session with Elasticsearch."""
    ES_INDEX_NAME = os.getenv("ES_INDEX_NAME", "chatdocs")
    ES_PORT = os.getenv("ES_PORT")
    conn_url = f"http://localhost:{ES_PORT}"
    es = Elasticsearch(hosts=[conn_url])
    vectorstore = ElasticsearchStore(
        index_name=ES_INDEX_NAME,
        embedding=embedding,
        es_client=es,
        filter_complex_metadata=True,
    )
    return vectorstore


@lru_cache(maxsize=1)
def start_vectorstore_session() -> Chroma:
    index = os.getenv("CHROMADB_INDEX", "chatdocs")
    port = os.getenv("CHROMADB_PORT", "9012")       
    host = os.getenv("CHROMADB_HOST", "localhost") 
    preset = os.getenv("CHROMADB_PRESET", ".vectorstore")

    settings = Settings(
        chroma_server_host=host,
        chroma_server_http_port=port,
    )
    client = HttpClient(host=host, port=port, settings=settings)

    vectorstore = Chroma(
        collection_name=index,
        embedding_function=embedding,
        client=client,
        persist_directory=preset,  
    )
    return vectorstore

@lru_cache(maxsize=1)
def start_postgresql_session() -> SQLDatabase:
    """Initialize the SQL database session with PostgreSQL."""
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    
    POSTGRES_URL = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@localhost:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    engine = create_engine(POSTGRES_URL)
    return SQLDatabase(engine=engine)


vectorstore = start_vectorstore_session()
sqldatabase = start_postgresql_session()

__all__ = ["vectorstore", "sqldatabase"]