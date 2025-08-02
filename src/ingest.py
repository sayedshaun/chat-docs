# ingest.py
from typing import Union
from pathlib import Path
import pandas as pd
import os
import logging
from .utils import calculate_execution_time
from .loader import load_files_from_directory, load_csv_from_directory
from .database import vectorstore, sqldatabase
from langchain_community.vectorstores.utils import filter_complex_metadata

logging.basicConfig(
    filemode="a", filename='info.log', 
    level=logging.INFO, format='[%(levelname)s] %(message)s'
    )


@calculate_execution_time
def update_vectorstore(
    file_or_dir: Union[Path, str], collection_name: str = "rag_collection"
    ) -> None:
    """
    Update the Chroma database with new documents.
    """
    try:
        documents = load_files_from_directory(file_or_dir)
        if not documents:
            logging.warning(f"No documents found in {file_or_dir}. Skipping update for {collection_name}.")
            return
        vectorstore.add_documents(
            documents=documents,
            collection_name=collection_name
        )
        logging.info(f"Updated {collection_name} with {len(documents)} documents from {file_or_dir}")
    except Exception as e:
        logging.error(f"Failed to update vectorstore: {str(e)}")


@calculate_execution_time
def update_sqldatabase(file_or_dir: Union[Path, str]) -> None:
    """
    Update the SQL database with new documents.
    """
    def add_table(dataframe, table_data):
        if dataframe.empty:
            logging.warning(f"DataFrame for table '{table_data}' is empty. Skipping.")
            return
        dataframe.to_sql(table_data, con=sqldatabase._engine, index=False, if_exists="append")
    try:
        if not hasattr(sqldatabase, "_engine") or sqldatabase._engine is None:
            raise RuntimeError("SQL database engine is not initialized.")
        csv_files = load_csv_from_directory(file_or_dir)
        for csv in csv_files:
            try:
                df = pd.read_csv(csv)
            except Exception as read_err:
                logging.error(f"Failed to read CSV file {str(read_err)}")
                continue
            table_name = os.path.splitext(os.path.basename(csv))[0]
            add_table(df, table_name)
        logging.info(f"Updated SQL database with {len(csv_files)} CSV files from {file_or_dir}")
    except Exception as e:
        logging.error(f"Failed to update SQL database: {str(e)}")
    

def update_database(file_or_dir: Union[Path, str]) -> None:
    update_vectorstore(file_or_dir)
    update_sqldatabase(file_or_dir)