from __future__ import annotations

from typing import List, Dict, Any

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
    """

    def __init__(
        self,
        db_path: str = "./chroma_db",
        collection_name: str = "sentinelforge",
    ):

        self.client = chromadb.PersistentClient(
            path=db_path,
            settings=Settings(anonymized_telemetry=False),
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def _clean_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        ChromaDB only supports:
        str, int, float, bool

        Convert unsupported values to strings and skip None.
        """

        clean = {}

        for key, value in metadata.items():

            if value is None:
                continue

            if isinstance(value, (str, int, float, bool)):
                clean[key] = value

            elif isinstance(value, (list, tuple)):
                clean[key] = ", ".join(map(str, value))

            elif isinstance(value, dict):
                clean[key] = str(value)

            else:
                clean[key] = str(value)

        return clean

    def add_documents(
        self,
        embedded_chunks: List[Dict],
    ):
        """
        Add embedded chunks into ChromaDB.

        Duplicate chunk_ids are skipped automatically.
        """

        for chunk in embedded_chunks:

            metadata = self._clean_metadata(chunk["metadata"])

            chunk_id = metadata.get("chunk_id")

            if not chunk_id:
                raise ValueError("Each chunk must contain metadata['chunk_id'].")

            existing = self.collection.get(ids=[chunk_id])

            if existing["ids"]:
                print(f"Skipping duplicate chunk: {chunk_id}")
                continue

            self.collection.add(
                ids=[chunk_id],
                documents=[chunk["content"]],
                embeddings=[chunk["embedding"]],
                metadatas=[metadata],
            )

    def search(
        self,
        query_embedding,
        top_k: int = 5,
    ):
        """
        Semantic search.
        """

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

    def delete_document(
        self,
        filename: str,
    ):
        """
        Delete every chunk belonging to a file.
        """

        results = self.collection.get()

        ids_to_delete = []

        ids = results.get("ids", [])
        metadatas = results.get("metadatas", [])

        for chunk_id, metadata in zip(ids, metadatas):

            if metadata is None:
                continue

            if metadata.get("filename") == filename:
                ids_to_delete.append(chunk_id)

        if ids_to_delete:
            self.collection.delete(ids=ids_to_delete)
            print(f"Deleted {len(ids_to_delete)} chunks.")

        else:
            print("No matching document found.")

    def total_chunks(self):
        """
        Return total indexed chunks.
        """
        return self.collection.count()

    def reset(self):
        """
        Delete all vectors.
        """

        self.client.delete_collection("sentinelforge")

        self.collection = self.client.get_or_create_collection(
            name="sentinelforge"
        )