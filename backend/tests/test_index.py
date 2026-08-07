from app.rag.loader import DocumentLoader
from app.rag.chunker import DocumentChunker
from app.rag.embedder import LocalEmbedder
from app.rag.index import VectorIndex

loader = DocumentLoader()

documents = loader.load("sample.md")

chunker = DocumentChunker()

chunks = chunker.chunk_documents(documents)

embedder = LocalEmbedder()

embedded = embedder.embed_documents(chunks)

index = VectorIndex()

index.add_documents(embedded)

print()

print("Indexed Chunks:")

print(index.total_chunks())