from pydantic import BaseModel, Field
from pathlib import Path

class Message(BaseModel):
    content: str = Field(..., description="Content of the message")

class DatabaseUpdate(BaseModel):
    file: Path = Field(..., description="Path to the file or directory to update the database")