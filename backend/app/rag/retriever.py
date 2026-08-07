from __future__ import annotations

from typing import Any, Dict, List

from app.core.config import settings
from app.rag.embedder import LocalEmbedder
from app.rag.index import VectorIndex


class Retriever:
    """
    Semantic retriever for SentinelForge.

    Flow:

        Query
          ↓
        Embed query
          ↓
        ChromaDB search
          ↓
        Structured results
    """

    def __init__(
        self,
        embedder: LocalEmbedder | None = None,
        index: VectorIndex | None = None,
    ):
        self.embedder = embedder or LocalEmbedder(
            model_name=settings.embedding_model
        )

        self.index = index or VectorIndex()

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve the most relevant documents.

        Returns:

        [
            {
                "content": "...",
                "score": 0.123,
                "citation": {...}
            }
        ]
        """

        if not query or not query.strip():
            return []

        if top_k is None:
            top_k = settings.default_top_k

        if top_k < 1:
            raise ValueError(
                "top_k must be greater than zero."
            )

        if top_k > settings.max_top_k:
            raise ValueError(
                f"top_k cannot exceed "
                f"{settings.max_top_k}."
            )

        query = query.strip()

        # Generate query embedding using the SAME
        # embedding model used during indexing.
        query_embedding = self.embedder.embed_text(
            query
        )

        search_results = self.index.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        documents = search_results.get(
            "documents",
            [[]],
        )

        metadatas = search_results.get(
            "metadatas",
            [[]],
        )

        distances = search_results.get(
            "distances",
            [[]],
        )

        if not documents or not documents[0]:
            return []

        documents = documents[0]
        metadatas = (
            metadatas[0]
            if metadatas
            else []
        )
        distances = (
            distances[0]
            if distances
            else []
        )

        results: List[Dict[str, Any]] = []

        for index, content in enumerate(documents):

            metadata = (
                metadatas[index]
                if index < len(metadatas)
                else {}
            )

            distance = (
                distances[index]
                if index < len(distances)
                else None
            )

            citation = {
                "filename": metadata.get(
                    "filename"
                ),
                "page": metadata.get(
                    "page"
                ),
                "language": metadata.get(
                    "language"
                ),
                "chunk_id": metadata.get(
                    "chunk_id"
                ),
            }

            results.append(
                {
                    "content": content,
                    "score": distance,
                    "citation": citation,
                }
            )

        return results