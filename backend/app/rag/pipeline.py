from __future__ import annotations

from typing import Any, Dict, List

from app.rag.guard import RAGGuard
from app.rag.sanitizer import RAGSanitizer
from app.rag.retriever import Retriever


class RAGPipeline:
    """
    Main entry point for the SentinelForge RAG pipeline.

    Flow:

        User Query
            ↓
        Sanitizer
            ↓
        Security Guard
            ↓
        Retriever
            ↓
        Results
    """

    def __init__(
        self,
        retriever: Retriever | None = None,
        sanitizer: RAGSanitizer | None = None,
        guard: RAGGuard | None = None,
    ):
        """
        Initialize the RAG pipeline.

        Components can be injected for testing.
        """

        self.sanitizer = sanitizer or RAGSanitizer()
        self.guard = guard or RAGGuard()
        self.retriever = retriever or Retriever()

    def query(
        self,
        query: str,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """
        Execute the complete RAG retrieval pipeline.
        """

        # 1. Sanitize
        sanitized_query = self.sanitizer.sanitize_query(query)

        if self.sanitizer.is_empty(sanitized_query):
            return {
                "success": False,
                "query": sanitized_query,
                "results": [],
                "reason": "Query cannot be empty.",
            }

        # 2. Security validation
        validation = self.guard.validate_query(
            sanitized_query
        )

        if not validation["allowed"]:
            return {
                "success": False,
                "query": sanitized_query,
                "results": [],
                "reason": validation["reason"],
            }

        # 3. Retrieval
        results = self.retriever.retrieve(
            sanitized_query,
            top_k=top_k,
        )

        # 4. Validate retrieved context
        context_validation = self.guard.validate_context(
            results
        )

        if not context_validation["allowed"]:
            return {
                "success": False,
                "query": sanitized_query,
                "results": [],
                "reason": context_validation["reason"],
            }

        # 5. Return structured response
        return {
            "success": True,
            "query": sanitized_query,
            "results": results,
            "reason": None,
        }

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Convenience method returning only results.
        """

        response = self.query(
            query=query,
            top_k=top_k,
        )

        return response["results"]