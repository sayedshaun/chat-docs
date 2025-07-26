# ingest.py
from typing import Callable, List, Sequence
from pathlib import Path
import pandas as pd
import time
import os
import logging
from tqdm import tqdm
from .database import start_session
from .utils import calculate_execution_time
from .loader import load_file, load_files_from_directory
from .provider import llm
from langchain_core.documents import Document
from langchain_community.vectorstores.utils import filter_complex_metadata

logging.basicConfig(
    filemode="a", filename='info.log', 
    level=logging.INFO, format='[%(levelname)s] %(message)s'
    )

chroma = start_session()

def update_database(
    file_or_dir: Path | str, 
    collection_name: str = "rag_collection"
    ) -> None:
    """
    Update the Chroma database with new documents.
    """
    if os.path.isdir(file_or_dir):
        documents = load_files_from_directory(file_or_dir)
        documents = filter_complex_metadata(documents)
    elif os.path.isfile(file_or_dir):
        documents = load_file(file_or_dir)
        documents = filter_complex_metadata(documents)
    chroma.add_documents(
        documents=documents,
        collection_name=collection_name
    )
    logging.info(f"Updated {collection_name} with {len(documents)} documents from {file_or_dir}")