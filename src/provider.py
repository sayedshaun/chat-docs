#llm.py
import os
from dotenv import load_dotenv
from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()

@lru_cache(maxsize=1)
def ollama_llm() -> ChatOllama:
    try:
        OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
    except KeyError:
        raise ValueError("OLLAMA_MODEL is not set in environment variables")
    return ChatOllama(model=OLLAMA_MODEL, reasoning=True)

@lru_cache(maxsize=1)
def ollama_embedding() -> OllamaEmbeddings:
    try:
        OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
    except KeyError:
        raise ValueError("OLLAMA_MODEL is not set in environment variables")
    return OllamaEmbeddings(model=OLLAMA_MODEL)

@lru_cache(maxsize=1)
def google_llm() -> ChatGoogleGenerativeAI:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in environment variables")
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", 
        api_key=GEMINI_API_KEY
    )

@lru_cache(maxsize=1)
def google_embedding() -> GoogleGenerativeAIEmbeddings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in environment variables")
    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001", 
        google_api_key=GEMINI_API_KEY
    )

@lru_cache(maxsize=1)
def huggingface_embedding() -> HuggingFaceEmbeddings:
    try:
        HUGGINGFACE_EMBEDDING_MODEL = os.getenv("HUGGINGFACE_EMBEDDING_MODEL")
    except KeyError:
        raise ValueError("HUGGINGFACE_MODEL is not set in environment variables")
    return HuggingFaceEmbeddings(model_name=HUGGINGFACE_EMBEDDING_MODEL)


llm = ollama_llm()
embedding = ollama_embedding()

__all__ = ["llm", "embedding"]