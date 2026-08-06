from __future__ import annotations

from typing import List, Dict

from app.rag.embedder import LocalEmbedder
from app.rag.index import VectorIndex


class Retriever:
    """
    Semantic retriever for SentinelForge RAG pipeline.

    Features:
    - Local query embeddings
    - ChromaDB semantic search
    - Similarity scoring
    - Citation metadata
    """


    def __init__(
        self,
        index: VectorIndex | None = None,
        embedder: LocalEmbedder | None = None,
    ):

        self.index = index or VectorIndex()
        self.embedder = embedder or LocalEmbedder()



    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict]:
        """
        Retrieve relevant document chunks.

        Returns:

        [
            {
                "content": "...",
                "score": 0.85,
                "citation": {
                    "filename": "...",
                    "page": "...",
                    "language": "...",
                    "chunk_id": "..."
                }
            }
        ]
        """


        # --------------------------------
        # Step 1:
        # Convert query into embedding
        # --------------------------------

        query_embedding = self.embedder.embed_text(
            query
        )


        # --------------------------------
        # Step 2:
        # Search vector database
        # --------------------------------

        results = self.index.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )


        documents = results.get(
            "documents",
            [[]]
        )[0]


        distances = results.get(
            "distances",
            [[]]
        )[0]


        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]



        retrieved_chunks = []


        # --------------------------------
        # Step 3:
        # Format results with citations
        # --------------------------------

        for document, distance, metadata in zip(
            documents,
            distances,
            metadatas,
        ):


            # Convert Chroma distance
            # into readable similarity score

            score = max(
                0,
                1 - distance
            )


            retrieved_chunks.append(
                {
                    "content": document,

                    "score": round(
                        score,
                        4
                    ),


                    "citation": {

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
                }
            )


        return retrieved_chunks



    def retrieve_context(
        self,
        query: str,
        top_k: int = 5,
    ) -> str:
        """
        Returns only combined text context.

        Useful before sending retrieved
        context to an LLM.
        """


        results = self.retrieve(
            query=query,
            top_k=top_k,
        )


        context = []


        for item in results:

            context.append(
                item["content"]
            )


        return "\n\n".join(context)