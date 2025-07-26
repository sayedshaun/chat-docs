import asyncio
import json
from typing import AsyncGenerator, List
from src.ingest import update_database
from src.graph import build_graph
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import shutil
import os
import tempfile
from src.schema import LLMResponse, Question
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
config={"configurable":{"thread_id":1}}

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/ask", response_model=LLMResponse)
async def ask_question(question: Question) -> LLMResponse:
    graph = build_graph()
    response = graph.invoke({"question": question.question}, config=config)
    return LLMResponse(answer=response["answer"])

@app.post("/ask_stream")
async def ask_question_stream(question: Question) -> StreamingResponse:
    graph = build_graph()
    async def token_stream() -> AsyncGenerator[str, None]:
        for msg, metadata in graph.stream(
            {"question": question.question}, 
            stream_mode="messages", 
            config=config
            ):
            if msg.content:
                yield f"data: {msg.content}\n\n"
                await asyncio.sleep(0)
    return StreamingResponse(token_stream(), media_type="text/event-stream")

@app.post("/upload_files/")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        system_temp_dir = tempfile.gettempdir()
        temp_dir = os.path.join(system_temp_dir, ".temp")
        os.makedirs(temp_dir, exist_ok=True)
        for uploaded_file in files:
            file_path = os.path.join(temp_dir, uploaded_file.filename)
            with open(file_path, "wb") as f:
                shutil.copyfileobj(uploaded_file.file, f)
        return {
            "status": "success",
            "message": f"{len(files)} files uploaded to {temp_dir}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/update_database/")
async def update_db():
    try:
        system_temp_dir = tempfile.gettempdir()
        temp_dir = os.path.join(system_temp_dir, ".temp")
        if not os.path.exists(temp_dir) or not os.listdir(temp_dir):
            return {
                "status": "error",
                "message": f"No files found in {temp_dir}. Please upload first."
            }
        update_database(temp_dir)
        shutil.rmtree(temp_dir)
        return {
            "status": "success",
            "message": f"Database updated from files in {temp_dir}"
        }
    except Exception as e:
        raise RuntimeError(f"Failed to update database: {str(e)}")
        

# if __name__ == "__main__":
#     backend_port = os.getenv("BACKEND_PORT", "9010")
#     subprocess.run(["uvicorn", "api:app", "--host", "0.0.0.0", "--port", str(backend_port), "--reload"])