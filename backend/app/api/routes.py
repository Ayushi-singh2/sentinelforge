from __future__ import annotations

from fastapi import APIRouter

from app.api.schemas import QueryRequest, QueryResponse
from app.rag.pipeline import RAGPipeline


router = APIRouter()


pipeline = RAGPipeline()


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "sentinelforge",
    }


@router.get("/")
def root():
    return {
        "name": "SentinelForge",
        "status": "running",
        "service": "RAG API",
    }


@router.post(
    "/api/query",
    response_model=QueryResponse,
)
def query(
    request: QueryRequest,
):

    result = pipeline.query(
        query=request.query,
        top_k=request.top_k,
    )

    return result