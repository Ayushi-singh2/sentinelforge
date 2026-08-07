from __future__ import annotations

from fastapi import FastAPI

from app.api.routes import router
from app.api.middleware import RequestMiddleware


app = FastAPI(
    title="SentinelForge",
    description="Secure RAG API system",
    version="1.0.0",
)


app.add_middleware(
    RequestMiddleware
)


@app.get("/")
def root():
    return {
        "name": "SentinelForge",
        "status": "running",
        "service": "RAG API",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "sentinelforge",
    }


app.include_router(
    router,
    prefix="/api",
)