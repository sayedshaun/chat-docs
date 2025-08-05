#llm.py
import logging
import os
from dotenv import load_dotenv
from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

@lru_cache(maxsize=1)
def ollama_llm() -> ChatOllama:
    """Initialize the Ollama LLM."""
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
    try:
        return ChatOllama(model=OLLAMA_MODEL, reasoning=True)
    except Exception as e:  
        logger.error("Failed to initialize Ollama LLM: %s", str(e))


@lru_cache(maxsize=1)
def ollama_embedding() -> OllamaEmbeddings:
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
    try:
        return OllamaEmbeddings(model=OLLAMA_MODEL)
    except Exception as e:
        logger.error("Failed to initialize Ollama Embeddings: %s", str(e))

@lru_cache(maxsize=1)
def google_llm() -> ChatGoogleGenerativeAI:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in environment variables")
    return ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"), 
        api_key=GEMINI_API_KEY
    )

@lru_cache(maxsize=1)
def google_embedding() -> GoogleGenerativeAIEmbeddings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in environment variables")
    return GoogleGenerativeAIEmbeddings(
        model=os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001"), 
        google_api_key=GEMINI_API_KEY
    )

@lru_cache(maxsize=1)
def huggingface_embedding() -> HuggingFaceEmbeddings:
    HUGGINGFACE_EMBEDDING_MODEL = os.getenv("HUGGINGFACE_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    try:
        return HuggingFaceEmbeddings(model_name=HUGGINGFACE_EMBEDDING_MODEL)
    except Exception as e:
        logger.error("Failed to initialize HuggingFace Embeddings: %s", str(e))


llm = google_llm()
embedding = huggingface_embedding()

__all__ = ["llm", "embedding"]