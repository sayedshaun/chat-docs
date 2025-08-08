
from fastapi import FastAPI
from src.backend.router import router as backend_router
from src.backend.router import lifespan
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="ChatDocs API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(backend_router)
