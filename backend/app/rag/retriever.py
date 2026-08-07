from __future__ import annotations

from typing import Any, Dict, List

from app.rag.embedder import LocalEmbedder
from app.rag.guard import RAGGuard
from app.rag.index import VectorIndex
from app.rag.sanitizer import RAGSanitizer


class Retriever:
    """
    RAG retrieval pipeline.

    Flow:

        User Query
            ↓
        Sanitizer
            ↓
        Security Guard
            ↓
        Embedding
            ↓
        ChromaDB
            ↓
        Normalized Results
    """

    def __init__(
        self,
        db_path: str = "./chroma_db",
        collection_name: str = "sentinelforge",
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.embedder = LocalEmbedder(
            model_name=model_name
        )

        self.index = VectorIndex(
            db_path=db_path,
            collection_name=collection_name,
        )

        self.guard = RAGGuard()
        self.sanitizer = RAGSanitizer()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve the most relevant documents for a query.

        Returns:

        [
            {
                "content": "...",
                "score": 0.87,
                "citation": {
                    "filename": "...",
                    "page": ...,
                    "language": "...",
                    "chunk_id": "..."
                }
            }
        ]
        """

        # -------------------------------------------------
        # 1. Sanitize query
        # -------------------------------------------------

        clean_query = self.sanitizer.sanitize_query(query)

        if self.sanitizer.is_empty(clean_query):
            return []

        # -------------------------------------------------
        # 2. Security validation
        # -------------------------------------------------

        validation = self.guard.validate_query(
            clean_query
        )

        if not validation["allowed"]:
            return []

        # -------------------------------------------------
        # 3. Validate top_k
        # -------------------------------------------------

        if top_k <= 0:
            return []

        # -------------------------------------------------
        # 4. Create query embedding
        # -------------------------------------------------

        query_embedding = self.embedder.embed_text(
            clean_query
        )

        # -------------------------------------------------
        # 5. Search ChromaDB
        # -------------------------------------------------

        results = self.index.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        # -------------------------------------------------
        # 6. Convert ChromaDB response
        #    into application-level results
        # -------------------------------------------------

        return self._format_results(results)

    def _format_results(
        self,
        results: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Convert the raw ChromaDB result into a clean
        list of retrieval results.
        """

        if not results:
            return []

        documents = results.get("documents") or []
        metadatas = results.get("metadatas") or []
        distances = results.get("distances") or []

        # Chroma returns nested lists because query_embeddings
        # contains one query.
        if documents and isinstance(documents[0], list):
            documents = documents[0]

        if metadatas and isinstance(metadatas[0], list):
            metadatas = metadatas[0]

        if distances and isinstance(distances[0], list):
            distances = distances[0]

        formatted: List[Dict[str, Any]] = []

        for index, content in enumerate(documents):

            metadata = {}

            if index < len(metadatas):
                metadata = metadatas[index] or {}

            distance = 0.0

            if index < len(distances):
                distance = distances[index]

            # Chroma's default distance for normalized
            # embeddings is commonly cosine distance:
            #
            #   similarity = 1 - distance
            #
            # Clamp the result so floating point noise does
            # not produce values outside [-1, 1].
            score = 1.0 - float(distance)

            score = max(
                -1.0,
                min(1.0, score),
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

            formatted.append(
                {
                    "content": content,
                    "score": score,
                    "citation": citation,
                }
            )

        return formatted

    def retrieve_with_threshold(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.0,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve documents and remove results below
        the requested similarity score.
        """

        results = self.retrieve(
            query=query,
            top_k=top_k,
        )

        return [
            result
            for result in results
            if result["score"] >= min_score
        ]

    def validate_results(
        self,
        results: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Validate retrieval results through the security guard.
        """

        validation = self.guard.validate_context(
            results
        )

        return validation