from __future__ import annotations

from typing import Any, Dict, List

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings


class VectorIndex:
    """
    Local ChromaDB vector index.

    Configuration is loaded from app.core.config.
    """

    def __init__(
        self,
        db_path: str | None = None,
        collection_name: str | None = None,
    ):
        self.db_path = db_path or settings.chroma_db_path
        self.collection_name = (
            collection_name or settings.chroma_collection_name
        )

        self.client = chromadb.PersistentClient(
            path=self.db_path,
            settings=ChromaSettings(
                anonymized_telemetry=False
            ),
        )

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
        )

    def _clean_metadata(
        self,
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        ChromaDB metadata supports primitive values.

        Unsupported values are converted to strings.
        None values are skipped.
        """

        clean: Dict[str, Any] = {}

        for key, value in metadata.items():

            if value is None:
                continue

            if isinstance(
                value,
                (str, int, float, bool),
            ):
                clean[key] = value

            elif isinstance(value, (list, tuple)):
                clean[key] = ", ".join(
                    map(str, value)
                )

            elif isinstance(value, dict):
                clean[key] = str(value)

            else:
                clean[key] = str(value)

        return clean

    def add_documents(
        self,
        embedded_chunks: List[Dict[str, Any]],
    ) -> None:
        """
        Add embedded chunks to ChromaDB.

        Existing chunk IDs are skipped.
        """

        for chunk in embedded_chunks:

            if "content" not in chunk:
                raise ValueError(
                    "Chunk must contain 'content'."
                )

            if "embedding" not in chunk:
                raise ValueError(
                    "Chunk must contain 'embedding'."
                )

            if "metadata" not in chunk:
                raise ValueError(
                    "Chunk must contain 'metadata'."
                )

            metadata = self._clean_metadata(
                chunk["metadata"]
            )

            chunk_id = metadata.get("chunk_id")

            if not chunk_id:
                raise ValueError(
                    "Each chunk must contain "
                    "metadata['chunk_id']."
                )

            existing = self.collection.get(
                ids=[str(chunk_id)]
            )

            if existing.get("ids"):
                print(
                    f"Skipping duplicate chunk: {chunk_id}"
                )
                continue

            self.collection.add(
                ids=[str(chunk_id)],
                documents=[chunk["content"]],
                embeddings=[chunk["embedding"]],
                metadatas=[metadata],
            )

    def search(
        self,
        query_embedding: List[float],
        top_k: int | None = None,
    ) -> Dict[str, Any]:
        """
        Perform semantic search.
        """

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

        total = self.collection.count()

        if total == 0:
            return {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]],
            }

        top_k = min(top_k, total)

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

    def delete_document(
        self,
        filename: str,
    ) -> None:
        """
        Delete all chunks belonging to a filename.
        """

        results = self.collection.get()

        ids = results.get("ids", [])
        metadatas = results.get("metadatas", [])

        ids_to_delete: List[str] = []

        for chunk_id, metadata in zip(
            ids,
            metadatas,
        ):

            if not metadata:
                continue

            if metadata.get("filename") == filename:
                ids_to_delete.append(chunk_id)

        if ids_to_delete:
            self.collection.delete(
                ids=ids_to_delete
            )

            print(
                f"Deleted {len(ids_to_delete)} chunks "
                f"for '{filename}'."
            )
        else:
            print(
                f"No chunks found for '{filename}'."
            )

    def total_chunks(self) -> int:
        """
        Return the number of indexed chunks.
        """

        return self.collection.count()

    def reset(self) -> None:
        """
        Delete and recreate the configured collection.
        """

        self.client.delete_collection(
            name=self.collection_name
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=self.collection_name
            )
        )