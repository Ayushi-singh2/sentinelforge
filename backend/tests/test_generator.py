import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from app.rag.generator import RAGGenerator


generator = RAGGenerator()


# --------------------------------------------------
# Test 1: Normal grounded answer
# --------------------------------------------------

print("-" * 50)
print("TEST: Grounded answer")

documents = [
    {
        "content": (
            "# SentinelForge\n\n"
            "SentinelForge is a secure RAG system.\n\n"
            "It processes documents and retrieves relevant "
            "information using vector search."
        ),
        "score": 0.91,
        "citation": {
            "filename": "sample.md",
            "page": None,
            "language": "markdown",
            "chunk_id": "test-chunk-1",
        },
    }
]

result = generator.generate(
    query="What is SentinelForge?",
    documents=documents,
)

print("ANSWER:")
print(result["answer"])

print("\nGROUNDED:")
print(result["grounded"])

print("\nCITATIONS:")
print(result["citations"])

assert result["answer"]
assert result["grounded"] is True
assert len(result["citations"]) == 1


# --------------------------------------------------
# Test 2: Empty query
# --------------------------------------------------

print("-" * 50)
print("TEST: Empty query")

result = generator.generate(
    query="",
    documents=documents,
)

print("ANSWER:")
print(result["answer"])

print("GROUNDED:")
print(result["grounded"])

print("REASON:")
print(result["reason"])

assert result["grounded"] is False
assert result["reason"] == "Query cannot be empty."


# --------------------------------------------------
# Test 3: No documents
# --------------------------------------------------

print("-" * 50)
print("TEST: No documents")

result = generator.generate(
    query="What is SentinelForge?",
    documents=[],
)

print("ANSWER:")
print(result["answer"])

print("GROUNDED:")
print(result["grounded"])

print("REASON:")
print(result["reason"])

assert result["grounded"] is False
assert result["reason"] == "No relevant documents found."


# --------------------------------------------------
# Test 4: Unrelated context
# --------------------------------------------------

print("-" * 50)
print("TEST: Unrelated context")

documents = [
    {
        "content": (
            "The weather is sunny today. "
            "The temperature is twenty five degrees."
        ),
        "score": 0.10,
        "citation": {
            "filename": "weather.md",
            "page": None,
            "language": "markdown",
            "chunk_id": "weather-1",
        },
    }
]

result = generator.generate(
    query="What is SentinelForge?",
    documents=documents,
)

print("ANSWER:")
print(result["answer"])

print("GROUNDED:")
print(result["grounded"])

print("REASON:")
print(result["reason"])

assert result["grounded"] is False
assert result["citations"] == []


print("-" * 50)
print("All generator tests passed.")