from __future__ import annotations

import hashlib
from typing import Dict, List

from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:
    """
    Splits documents into overlapping chunks while preserving metadata.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def chunk_documents(
        self,
        documents: List[Dict],
    ) -> List[Dict]:

        chunks = []

        for document in documents:

            text = document["content"]
            metadata = document["metadata"]

            pieces = self.splitter.split_text(text)

            current_position = 0

            for index, piece in enumerate(pieces):

                start = text.find(piece, current_position)

                if start == -1:
                    start = current_position

                end = start + len(piece)

                current_position = end

                start_line = text[:start].count("\n") + 1
                end_line = text[:end].count("\n") + 1

                chunk_metadata = metadata.copy()

                chunk_metadata.update(
                    {
                        "chunk_index": index,
                        "chunk_id": hashlib.sha256(
                            (
                                metadata["filename"]
                                + str(index)
                                + piece
                            ).encode()
                        ).hexdigest(),
                        "line_start": start_line,
                        "line_end": end_line,
                    }
                )

                chunks.append(
                    {
                        "content": piece,
                        "metadata": chunk_metadata,
                    }
                )

        return chunks