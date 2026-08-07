from __future__ import annotations

from typing import List, Dict


class RAGGuard:
    """
    Security checks for the RAG pipeline.
    """

    BLOCKED_PATTERNS = [
        "ignore previous instructions",
        "ignore all instructions",
        "system prompt",
        "developer message",
        "reveal your prompt",
        "jailbreak",
        "bypass safety",
        "disable safety",
    ]

    def validate_query(self, query: str) -> Dict:
        """
        Validate the user's query before retrieval.
        """

        if not query or not query.strip():
            return {
                "allowed": False,
                "reason": "Query cannot be empty.",
            }

        query_lower = query.lower()

        for pattern in self.BLOCKED_PATTERNS:
            if pattern in query_lower:
                return {
                    "allowed": False,
                    "reason": "Potential prompt injection detected.",
                }

        return {
            "allowed": True,
            "reason": None,
        }

    def validate_context(self, documents: List[Dict]) -> Dict:
        """
        Ensure the retriever returned usable documents.
        """

        if not documents:
            return {
                "allowed": False,
                "reason": "No relevant documents found.",
            }

        return {
            "allowed": True,
            "reason": None,
        }

    def validate_answer(self, answer: str) -> Dict:
        """
        Validate generated answer.
        """

        if not answer or not answer.strip():
            return {
                "allowed": False,
                "reason": "Generated answer is empty.",
            }

        return {
            "allowed": True,
            "reason": None,
        }