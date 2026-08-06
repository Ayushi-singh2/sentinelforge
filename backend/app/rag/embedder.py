from __future__ import annotations

from typing import List, Dict

from sentence_transformers import SentenceTransformer


class LocalEmbedder:
    """
    Local embedding model using Sentence Transformers.
    """

    _model = None

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):

        if LocalEmbedder._model is None:
            print(f"Loading embedding model: {model_name}")
            LocalEmbedder._model = SentenceTransformer(model_name)

        self.model = LocalEmbedder._model

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for one text.
        """

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_documents(
        self,
        chunks: List[Dict],
    ) -> List[Dict]:
        """
        Generate embeddings for all chunks.
        """

        texts = [chunk["content"] for chunk in chunks]

        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=16,
            show_progress_bar=True,
        )

        embedded_chunks = []

        for chunk, vector in zip(chunks, vectors):

            embedded_chunks.append(
                {
                    "content": chunk["content"],
                    "metadata": chunk["metadata"],
                    "embedding": vector.tolist(),
                }
            )

        return embedded_chunks