from app.rag.loader import DocumentLoader
from app.rag.chunker import DocumentChunker

loader = DocumentLoader()

documents = loader.load("sample.md")

chunker = DocumentChunker(
    chunk_size=100,
    chunk_overlap=20,
)

chunks = chunker.chunk_documents(documents)

print("=" * 80)

print("Total Chunks:", len(chunks))

print("=" * 80)

for chunk in chunks:

    print(chunk["metadata"])

    print(chunk["content"])

    print("-" * 80)