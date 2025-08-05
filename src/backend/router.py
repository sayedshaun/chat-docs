# router.py
import asyncio
from typing import AsyncGenerator, List
from src.rag.ingest import update_database
from src.rag.graph import create_graph
from src.rag.prompt import create_agent_prompt
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from langchain_core.messages import BaseMessage, AIMessage
import shutil
import os
import tempfile
from src.backend.schema import Message
from dotenv import load_dotenv
import logging

logging.basicConfig(
    filemode="a", filename='info.log', 
    level=logging.INFO, format='[%(levelname)s] %(message)s'
    )


load_dotenv()

router = APIRouter()
config={"configurable":{"thread_id":1}}


@router.post("/ask", response_model=Message)
async def ask_question(message: Message) -> Message:
    graph = create_graph()
    input_prompt = create_agent_prompt(message)
    response = graph.invoke(input_prompt, config=config)
    messages: List[BaseMessage] = response.get("messages", [])
    last_ai_msg = next((m for m in reversed(messages) if isinstance(m, AIMessage)), None)
    if not last_ai_msg:
        return Message(content="Sorry, I couldn't generate a response.")
    return Message(content=last_ai_msg.content)


@router.post("/ask_stream", response_class=StreamingResponse)
async def ask_question_stream(question: Message) -> StreamingResponse:
    graph = create_graph()
    async def token_stream() -> AsyncGenerator[str, None]:
        for msg, metadata in graph.stream(
            {"messages": question.content}, 
            stream_mode="messages", 
            config=config
            ):
            if metadata["langgraph_node"]=="rag_agent_node":
                if msg.content:
                    yield f"data: {msg.content}\n\n"
                    await asyncio.sleep(0)
    return StreamingResponse(token_stream(), media_type="text/event-stream")


@router.post("/upload_files/")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        system_temp_dir = tempfile.gettempdir()
        temp_dir = os.path.join(system_temp_dir, ".temp")
        os.makedirs(temp_dir, exist_ok=True)
        for uploaded_file in files:
            file_path = os.path.join(temp_dir, uploaded_file.filename)
            with open(file_path, "wb") as f:
                shutil.copyfileobj(uploaded_file.file, f)
        return JSONResponse(content={"status": "Upload Success"})
    except Exception as e:
        raise RuntimeError(f"Failed to upload files: {str(e)}")


@router.post("/update_database/")
async def update_db():
    try:
        system_temp_dir = tempfile.gettempdir()
        temp_dir = os.path.join(system_temp_dir, ".temp")
        if not os.path.exists(temp_dir) or not os.listdir(temp_dir):
            return JSONResponse(content={"status": "No files found in temp directory"})
        update_database(temp_dir)
        shutil.rmtree(temp_dir)
        return JSONResponse(content={"status": "Database Updated"})
    except Exception as e:
        raise RuntimeError(f"Failed to update database: {str(e)}")