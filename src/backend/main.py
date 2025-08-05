
from fastapi import FastAPI
from src.backend.router import router as backend_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(backend_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)