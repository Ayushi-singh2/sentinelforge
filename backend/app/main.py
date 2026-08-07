from fastapi import FastAPI

from app.api.routes import router as api_router
from app.api.middleware import RequestMiddleware


app = FastAPI(
    title="SentinelForge",
    version="1.0.0",
)


# Middleware
app.add_middleware(
    RequestMiddleware
)


# Register API routes
app.include_router(
    api_router
)


@app.get("/")
def root():
    return {
        "name": "SentinelForge",
        "status": "running",
        "service": "RAG API",
    }