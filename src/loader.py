#loader.py
import os
from .utils import calculate_execution_time
from typing import List
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import (
    UnstructuredPDFLoader,
    TextLoader, 
    UnstructuredWordDocumentLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

@calculate_execution_time
def load_files_from_directory(directory: str) -> List:
    """
    Load all documents from a specified directory.
    Supports PDF files and other text-based formats.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50
    )
    pdf_docs = splitter.split_documents(
        DirectoryLoader(
            path=directory,
            glob="**/*.pdf",
            loader_cls=UnstructuredPDFLoader,
            loader_kwargs={
                "mode": "elements",
                "language": "ben",
            }
        ).load()
    )
    text_docs = splitter.split_documents(
        DirectoryLoader(
            path=directory,
            glob="**/*.txt",
            loader_cls=TextLoader
        ).load()
    )
    word_docs = splitter.split_documents(
        DirectoryLoader(
            path=directory,
            glob="**/*.docx",
            loader_cls=UnstructuredWordDocumentLoader
        ).load()
    )
    splited_documents = pdf_docs + text_docs + word_docs
    return splited_documents


@calculate_execution_time
def load_file(file_path: str) -> List:
    """
    Load a single file based on its extension.
    Supports PDF, TXT, and DOCX formats.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50
    )
    if file_path.endswith(".pdf"):
        return splitter.split_documents(
            UnstructuredPDFLoader(file_path).load()
        )
    elif file_path.endswith(".txt"):
        return splitter.split_documents(
            TextLoader(file_path).load()
        )
    elif file_path.endswith(".docx"):
        return splitter.split_documents(
            UnstructuredWordDocumentLoader(file_path).load()
        )
    else:
        raise ValueError(
            "Unsupported file format. " \
            "Only PDF, TXT, and DOCX files are supported."
        )