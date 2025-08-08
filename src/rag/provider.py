# provider.py

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

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", None)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", None)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", None)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", None)
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", None)
HUGGINGFACE_EMBEDDING_MODEL = os.getenv("HUGGINGFACE_EMBEDDING_MODEL", None)


@lru_cache(maxsize=1)
def ollama_llm() -> ChatOllama:
    """Initialize the Ollama LLM."""
    try:
        llm = ChatOllama(model=OLLAMA_MODEL, reasoning=True)
        logger.info("Initialized Ollama LLM with model: %s", OLLAMA_MODEL)
        return llm
    except Exception as e:  
        logger.error("Failed to initialize Ollama LLM: %s", str(e))

@lru_cache(maxsize=1)
def ollama_embedding() -> OllamaEmbeddings:
    try:
        embedding = OllamaEmbeddings(model=OLLAMA_MODEL)
        logger.info(
            "Initialized Ollama Embeddings with model: %s", 
            OLLAMA_MODEL
        )
        return embedding
    except Exception as e:
        logger.error("Failed to initialize Ollama Embeddings: %s", str(e))

@lru_cache(maxsize=1)
def google_llm() -> ChatGoogleGenerativeAI:
    """Initialize the Google LLM."""
    try:
        llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL, 
            api_key=GEMINI_API_KEY,
        )
        logger.info(
            "Initialized Google LLM with model: %s", 
            GEMINI_MODEL
        )
        return llm
    except Exception as e:
        logger.error("Failed to initialize Google LLM: %s", str(e))

@lru_cache(maxsize=1)
def google_embedding() -> GoogleGenerativeAIEmbeddings:
    """Initialize the Google Generative AI Embeddings."""
    try:
        embedding = GoogleGenerativeAIEmbeddings(
            model=GEMINI_EMBEDDING_MODEL, 
            google_api_key=GEMINI_API_KEY,
        )
        logger.info(
            "Initialized Google Generative AI Embeddings with model: %s", 
            GEMINI_EMBEDDING_MODEL
        )
        return embedding
    except Exception as e:
        logger.error("Failed to initialize Google Generative AI Embeddings: %s", str(e))

@lru_cache(maxsize=1)
def huggingface_embedding() -> HuggingFaceEmbeddings:
    try:
        embedding = HuggingFaceEmbeddings(model_name=HUGGINGFACE_EMBEDDING_MODEL)
        logger.info(
            "Initialized HuggingFace Embeddings with model: %s", 
            HUGGINGFACE_EMBEDDING_MODEL
        )
        return embedding
    except Exception as e:
        logger.error("Failed to initialize HuggingFace Embeddings: %s", str(e))


llm, embedding = None, None
if OLLAMA_MODEL and HUGGINGFACE_EMBEDDING_MODEL:
    llm = ollama_llm()
    embedding = huggingface_embedding()
elif OLLAMA_MODEL:
    llm = ollama_llm()
    embedding = ollama_embedding()
elif GEMINI_API_KEY and GEMINI_MODEL and GEMINI_EMBEDDING_MODEL:
    llm = google_llm()
    embedding = google_embedding()
elif GEMINI_API_KEY and GEMINI_MODEL and HUGGINGFACE_EMBEDDING_MODEL:
    llm = google_llm()
    embedding = huggingface_embedding()
else:
    logger.warning(
        "No valid LLM or embedding model configuration found. "
        "Please check your environment variables."
    )

if not llm or not embedding:
    raise ValueError(
        "Failed to initialize LLM or embedding. "
        "Ensure that the required environment variables are set correctly."
    )


__all__ = ["llm", "embedding"]