from __future__ import annotations

from typing import Any, Dict, List

import chromadb
from chromadb.config import Settings


class VectorIndex:
    """
    Local ChromaDB vector index.

    Features:
    - Persistent storage
    - Duplicate detection
    - Incremental indexing
    - Semantic search
    - Document deletion
    - Collection reset
    """

    def __init__(
        self,
        db_path: str = "./chroma_db",
        collection_name: str = "sentinelforge",
    ):
        self.db_path = db_path
        self.collection_name = collection_name

        self.client = chromadb.PersistentClient(
            path=db_path,
            settings=Settings(
                anonymized_telemetry=False
            ),
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name
            )
        )

    def _clean_metadata(
        self,
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        ChromaDB metadata values must be primitive types.

        Supported:
        - str
        - int
        - float
        - bool

        None values are skipped.
        Lists, tuples and dictionaries are converted
        to strings.
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

            elif isinstance(
                value,
                (list, tuple),
            ):
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
        Add embedded chunks into ChromaDB.

        Duplicate chunk IDs are skipped.
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

            chunk_id = metadata.get(
                "chunk_id"
            )

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
                    f"Skipping duplicate chunk: "
                    f"{chunk_id}"
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
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """
        Perform semantic similarity search.

        Returns the raw ChromaDB result.
        The Retriever is responsible for formatting it.
        """

        if top_k <= 0:
            return {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]],
            }

        # Avoid requesting more results than exist.
        total = self.collection.count()

        if total == 0:
            return {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]],
            }

        n_results = min(
            top_k,
            total,
        )

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

    def delete_document(
        self,
        filename: str,
    ) -> None:
        """
        Delete every chunk belonging to a file.
        """

        results = self.collection.get()

        ids = results.get(
            "ids",
            [],
        )

        metadatas = results.get(
            "metadatas",
            [],
        )

        ids_to_delete: List[str] = []

        for chunk_id, metadata in zip(
            ids,
            metadatas,
        ):
            if not metadata:
                continue

            if metadata.get(
                "filename"
            ) == filename:
                ids_to_delete.append(
                    chunk_id
                )

        if ids_to_delete:
            self.collection.delete(
                ids=ids_to_delete
            )

            print(
                f"Deleted "
                f"{len(ids_to_delete)} "
                f"chunks."
            )

        else:
            print(
                "No matching document found."
            )

    def total_chunks(self) -> int:
        """
        Return total number of indexed chunks.
        """

        return self.collection.count()

    def reset(self) -> None:
        """
        Delete the current collection and
        recreate it.
        """

        try:
            self.client.delete_collection(
                name=self.collection_name
            )
        except Exception:
            pass

        self.collection = (
            self.client.get_or_create_collection(
                name=self.collection_name
            )
        )