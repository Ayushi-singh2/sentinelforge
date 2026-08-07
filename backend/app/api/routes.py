from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.rag.pipeline import RAGPipeline


router = APIRouter(
    prefix="/api",
    tags=["RAG"],
)

pipeline = RAGPipeline()


class QueryRequest(BaseModel):
    """
    Request body for the RAG query endpoint.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="User question",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of documents to retrieve",
    )


class QueryResponse(BaseModel):
    """
    Response returned by the RAG API.
    """

    success: bool
    query: str
    answer: str
    grounded: bool
    reason: str | None = None
    citations: list[Dict[str, Any]] = []
    formatted_citations: list[str] = []


@router.post(
    "/query",
    response_model=QueryResponse,
)
def query_rag(request: QueryRequest) -> QueryResponse:
    """
    Execute the SentinelForge RAG pipeline.
    """

    result = pipeline.query(
        query=request.query,
        top_k=request.top_k,
    )

    return QueryResponse(
        success=result["success"],
        query=result["query"],
        answer=result.get("answer", ""),
        grounded=result.get("grounded", False),
        reason=result.get("reason"),
        citations=result.get("citations", []),
        formatted_citations=result.get(
            "formatted_citations",
            [],
        ),
    )