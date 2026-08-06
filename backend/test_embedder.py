from app.rag.loader import DocumentLoader
from app.rag.chunker import DocumentChunker
from app.rag.embedder import LocalEmbedder

loader = DocumentLoader()

documents = loader.load("sample.md")

chunker = DocumentChunker()

chunks = chunker.chunk_documents(documents)

embedder = LocalEmbedder()

embedded = embedder.embed_documents(chunks)

print("=" * 80)

print("Total embedded chunks:", len(embedded))

print("=" * 80)

print(embedded[0]["metadata"])

print()

print("Embedding dimension:")

print(len(embedded[0]["embedding"]))