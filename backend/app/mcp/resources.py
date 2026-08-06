from pathlib import Path
from typing import Dict, List


class DocumentResource:
    """
    Stores metadata about indexed documents.

    Later this will be connected to the RAG index.
    """

    def __init__(self):
        self.documents: List[Dict] = []

    def add_document(
        self,
        filename: str,
        filepath: str,
        filetype: str,
        chunks: int = 0,
    ) -> None:

        self.documents.append(
            {
                "filename": filename,
                "filepath": filepath,
                "filetype": filetype,
                "chunks": chunks,
            }
        )

    def remove_document(self, filename: str):

        self.documents = [
            doc for doc in self.documents
            if doc["filename"] != filename
        ]

    def clear(self):

        self.documents.clear()

    def get_documents(self):

        return {
            "documents": self.documents,
            "count": len(self.documents)
        }


document_resource = DocumentResource()