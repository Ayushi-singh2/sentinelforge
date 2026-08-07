from app.rag.citation import CitationManager


citation_manager = CitationManager()


documents = [
    {
        "content": "SentinelForge is a RAG security system.",
        "citation": {
            "filename": "sample.md",
            "page": None,
            "language": "markdown",
            "chunk_id": "chunk-1",
        },
    },
    {
        "content": "SentinelForge protects RAG pipelines.",
        "citation": {
            "filename": "security.md",
            "page": 3,
            "language": "markdown",
            "chunk_id": "chunk-2",
        },
    },
    {
        "content": "Duplicate source.",
        "citation": {
            "filename": "sample.md",
            "page": None,
            "language": "markdown",
            "chunk_id": "chunk-1",
        },
    },
]


print("-" * 50)
print("TEST: Extract citations")

citations = citation_manager.extract_citations(
    documents
)

for citation in citations:
    print(citation)

assert len(citations) == 2


print("-" * 50)
print("TEST: Format citation")

formatted = citation_manager.format_citation(
    citations[0]
)

print(formatted)

assert "sample.md" in formatted
assert "chunk-1" in formatted


print("-" * 50)
print("TEST: Format citations")

formatted_list = citation_manager.format_citations(
    citations
)

for citation in formatted_list:
    print(citation)

assert len(formatted_list) == 2


print("-" * 50)
print("TEST: Extract from metadata")

metadata_documents = [
    {
        "content": "Test document.",
        "metadata": {
            "filename": "metadata.md",
            "page": 5,
            "language": "markdown",
            "chunk_id": "metadata-chunk-1",
        },
    }
]

metadata_citations = citation_manager.extract_citations(
    metadata_documents
)

print(metadata_citations)

assert len(metadata_citations) == 1
assert metadata_citations[0]["filename"] == "metadata.md"
assert metadata_citations[0]["page"] == 5


print("-" * 50)
print("ALL CITATION TESTS PASSED")