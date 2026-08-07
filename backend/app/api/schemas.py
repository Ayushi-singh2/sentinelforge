from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="User query",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of documents to retrieve",
    )

    @field_validator("query")
    @classmethod
    def validate_query(cls, value: str):
        if value == "":
            raise ValueError("Query cannot be empty")

        return value


class QueryResponse(BaseModel):
    success: bool
    query: str
    answer: str
    grounded: bool
    reason: str | None = None
    citations: list[dict] = []
    formatted_citations: list[str] = []