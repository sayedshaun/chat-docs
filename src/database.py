import os
from functools import lru_cache
from dotenv import load_dotenv
from langchain_chroma import Chroma
from .provider import embedding
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"

load_dotenv()

@lru_cache(maxsize=1)
def start_session() -> Chroma:
    return Chroma(
        collection_name="rag_collection",
        embedding_function=embedding,
        persist_directory="./.chromadb"
    )

chroma = start_session()

__all__ = ["chroma"]