from __future__ import annotations

import re


class RAGSanitizer:
    """
    Sanitizes user queries before they reach the RAG pipeline.
    """

    def sanitize_query(self, query: str) -> str:
        """
        Clean and normalize a user query.
        """

        if not query:
            return ""

        # Remove leading/trailing whitespace
        query = query.strip()

        # Normalize repeated whitespace
        query = re.sub(r"\s+", " ", query)

        # Remove null bytes
        query = query.replace("\x00", "")

        return query

    def is_empty(self, query: str) -> bool:
        """
        Check whether a query is empty after sanitization.
        """

        return not query.strip()