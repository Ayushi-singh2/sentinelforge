from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="SentinelForge API",
    description="Secure Retrieval-Augmented Generation API",
    version="1.0.0",
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "name": "SentinelForge",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }