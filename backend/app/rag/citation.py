from __future__ import annotations

from typing import Any, Dict, List


class CitationManager:
    """
    Handles citation extraction, formatting, and deduplication
    for SentinelForge RAG responses.
    """

    def extract_citations(
        self,
        documents: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Extract citation metadata from retrieved documents.
        """

        citations: List[Dict[str, Any]] = []
        seen = set()

        for document in documents:

            citation = document.get("citation")

            if not citation:
                metadata = document.get("metadata", {})
                citation = self._citation_from_metadata(metadata)

            if not citation:
                continue

            normalized = self._normalize_citation(citation)

            key = (
                normalized.get("filename"),
                normalized.get("page"),
                normalized.get("chunk_id"),
            )

            if key in seen:
                continue

            seen.add(key)
            citations.append(normalized)

        return citations

    def format_citation(
        self,
        citation: Dict[str, Any],
    ) -> str:
        """
        Convert citation metadata into a human-readable string.
        """

        filename = citation.get(
            "filename",
            "unknown",
        )

        page = citation.get("page")

        chunk_id = citation.get(
            "chunk_id"
        )

        parts = [f"Source: {filename}"]

        if page is not None:
            parts.append(f"Page: {page}")

        if chunk_id:
            parts.append(f"Chunk: {chunk_id}")

        return " | ".join(parts)

    def format_citations(
        self,
        citations: List[Dict[str, Any]],
    ) -> List[str]:
        """
        Format multiple citations.
        """

        return [
            self.format_citation(citation)
            for citation in citations
        ]

    def _citation_from_metadata(
        self,
        metadata: Dict[str, Any],
    ) -> Dict[str, Any] | None:
        """
        Build citation information from document metadata.
        """

        if not metadata:
            return None

        filename = metadata.get("filename")

        if not filename:
            return None

        return {
            "filename": filename,
            "page": metadata.get("page"),
            "language": metadata.get("language"),
            "chunk_id": metadata.get("chunk_id"),
        }

    @staticmethod
    def _normalize_citation(
        citation: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Normalize citation fields so all citations have
        a consistent structure.
        """

        return {
            "filename": citation.get("filename"),
            "page": citation.get("page"),
            "language": citation.get("language"),
            "chunk_id": citation.get("chunk_id"),
        }