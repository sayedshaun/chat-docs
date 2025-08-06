![alt text](docs/cover.jpg)

# ChatDocs: A private knowledge base chatbot to chat with your documents

This is a RAG chatbot that uses LangChain and LangGraph to build a chatbot that can answer questions based on a given document.

## Project Structure

The project is structured as follows:

```bash
chat-docs/
    ├── README.md
    ├── dockerfiles/
    │   ├── backend.Dockerfile
    │   └── frontend.Dockerfile
    ├── docs/
    │   ├── cover.jpg
    │   └── image.png
    ├── src/
    │    ├── __init__.py
    │    ├── backend/
    │    │   ├── __init__.py
    │    │   ├── ...
    │    │   └── ...
    │    ├── rag/
    │    │   ├── __init__.py
    │    │   ├── ...
    │    │   └── ...
    │    ├── ui/
    │    │   ├── __init__.py
    │    │   ├── ...
    │    │   └── ...
    │    └── __init__.py
    ├── .env
    ├── .gitignore
    ├── .dockerignore
    ├── docker-compose.yml
    ├── requirements.txt
    └── LICENSE
```

## Setup

```bash
git clone https://github.com/sayedshaun/chat-docs.git
cd chat-docs
```
### Setup Environment Variables

Create `.env` file and add the following environment variables:
You can customize the environment variables as per your requirements.
```bash
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
HUGGINGFACE_EMBEDDING_MODEL=all-MiniLM-L6-v2
# .env
POSTGRES_DB=chatdocs
CHROMADB_INDEX=chatdocs
# Auth
POSTGRES_USER=user
POSTGRES_PASSWORD=password
CHROMADB_PRESET=./vectorstore
# Ports
BACKEND_PORT=9010
FRONTEND_PORT=9011
CHROMADB_PORT=9012
POSTGRES_PORT=9013
# Confgis
CHUNK_SIZE=500
CHUNK_OVERLAP=50
# If you use ollama model
OLLAMA_MODEL=llama3.2
```

If you use ollama model, you need to set up [ollama](https://ollama.com/download) first.

# Usage

### Start Server
```bash
docker compose up --build
```

### API

ChatDocs built with FastAPI, so you can view the API documentation with Swagger UI. Here is the reference of the available endpoints:

#### API Reference
- Ask Question: `http://{HOST}:{BACKEND_PORT}/ask`
- Get stream response: `http://{HOST}:{BACKEND_PORT}/ask_stream`
- Upload Files: `http://{HOST}:{BACKEND_PORT}/upload_files`
- Update Database: `http://{HOST}:{BACKEND_PORT}/update_database`


## Prebuilt UI
`ChatDocs` provides a prebuilt UI, you can access it at `http://{HOST}:{FRONTEND_PORT}`, e.g. `http://localhost:9011`.

![alt text](docs/image.png)

## Supported Document
| File Type      | Extensions         | Description                |
|----------------|-------------------|----------------------------|
| PDF            | `.pdf`            | Portable Document Format   |
| Word           | `.doc`, `.docx`   | Microsoft Word Documents   |
| Text           | `.txt`            | Plain Text Files           |
| Markdown       | `.md`             | Markdown Files             |
| HTML           | `.html`, `.htm`   | HyperText Markup Language  |
| PowerPoint     | `.ppt`, `.pptx`   | Microsoft PowerPoint Files |
| Excel          | `.xls`, `.xlsx`   | Microsoft Excel Files      |
| XML            | `.xml`            | XML Data Files             |
| Email          | `.eml`            | Email Message Files        |
| JSON           | `.json`           | JavaScript Object Notation |
| CSV            | `.csv`            | Comma-Separated Values     |


## Supported Language
Based on embedding model and document type. text pictures does not support yet but will be available soon.



