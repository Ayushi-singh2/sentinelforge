from __future__ import annotations

from fastapi import APIRouter, HTTPException

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
    "/query",
    response_model=QueryResponse,
)
def query(
    request: QueryRequest,
):

    # Empty string should return HTTP 422
    if request.query == "":
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "type": "value_error",
                    "loc": ["body", "query"],
                    "msg": "Query cannot be empty",
                    "input": request.query,
                }
            ],
        )

    # Whitespace query is handled by RAG pipeline
    # It should return HTTP 200 with failure response
    if not request.query.strip():
        return pipeline.query(
            query=request.query,
            top_k=request.top_k,
        )

    result = pipeline.query(
        query=request.query,
        top_k=request.top_k,
    )

    return result