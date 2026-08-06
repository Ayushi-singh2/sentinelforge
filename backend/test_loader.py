from app.rag.loader import DocumentLoader

loader = DocumentLoader()

documents = loader.load("sample.md")

print("=" * 60)

for doc in documents:

    print(doc["metadata"])

    print(doc["content"][:300])

    print("=" * 60)