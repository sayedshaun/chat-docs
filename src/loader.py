#loader.py
import glob
import os

from pyparsing import Optional
from .utils import calculate_execution_time
from typing import List
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import (
    TextLoader, 
    UnstructuredWordDocumentLoader,
    UnstructuredMarkdownLoader,
    UnstructuredHTMLLoader,
    UnstructuredCSVLoader,
    UnstructuredPowerPointLoader,
    UnstructuredExcelLoader,
    UnstructuredXMLLoader,
    UnstructuredEmailLoader,
    JSONLoader,
    PyPDFLoader,
    WebBaseLoader,
    WikipediaLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

@calculate_execution_time
def load_files_from_directory(directory: str) -> List:
    """Load all documents from the directory"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=int(os.getenv("CHUNK_SIZE")), 
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP"))
    )
    pdf_docs = splitter.split_documents(
        DirectoryLoader(
            path=directory,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
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
    markdown_docs = splitter.split_documents(
        DirectoryLoader(
            path=directory,
            glob="**/*.md",
            loader_cls=UnstructuredMarkdownLoader
        ).load()
    )
    html_docs = splitter.split_documents(
        DirectoryLoader(
            path=directory,
            glob="**/*.html",
            loader_cls=UnstructuredHTMLLoader
        ).load()
    )
    ppt_docs = splitter.split_documents(
        DirectoryLoader(
            path=directory,
            glob="**/*.pptx",
            loader_cls=UnstructuredPowerPointLoader
        ).load()
    )
    excel_docs = splitter.split_documents(
        DirectoryLoader(
            path=directory,
            glob="**/*.xlsx",
            loader_cls=UnstructuredExcelLoader
        ).load()
    )
    xml_docs = splitter.split_documents(
        DirectoryLoader(
            path=directory,
            glob="**/*.xml",
            loader_cls=UnstructuredXMLLoader
        ).load()
    )
    email_docs = splitter.split_documents(
        DirectoryLoader(
            path=directory,
            glob="**/*.eml",
            loader_cls=UnstructuredEmailLoader
        ).load()
    )
    json_docs = splitter.split_documents(
        DirectoryLoader(
            path=directory,
            glob="**/*.json",
            loader_cls=JSONLoader
        ).load()
    )
    splited_documents = (
        pdf_docs + 
        text_docs + 
        word_docs +
        markdown_docs +
        html_docs +
        ppt_docs +
        excel_docs +
        xml_docs +
        email_docs +
        json_docs
    )
    return splited_documents


@calculate_execution_time
def load_csv_from_directory(directory: str) -> List:
    """Load all documents from the directory"""
    return glob.glob(f"{directory}/*.csv")

