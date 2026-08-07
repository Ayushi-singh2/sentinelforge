from fastapi import FastAPI

from app.api.routes import router
from app.api.auth import auth_middleware
from app.api.middleware import RequestMiddleware


app = FastAPI(
    title="SentinelForge",
    version="1.0.0",
)


# Request logging middleware
app.add_middleware(RequestMiddleware)


# API Key Authentication
app.middleware("http")(auth_middleware)


# API routes
app.include_router(
    router,
    prefix="/api",
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