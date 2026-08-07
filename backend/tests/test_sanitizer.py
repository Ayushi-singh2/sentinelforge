from app.rag.sanitizer import RAGSanitizer


sanitizer = RAGSanitizer()


tests = [
    "What is SentinelForge?",
    "   What is SentinelForge?   ",
    "What    is     SentinelForge?",
    "",
]


for query in tests:

    cleaned = sanitizer.sanitize_query(query)

    print("-" * 50)
    print("INPUT :", repr(query))
    print("OUTPUT:", repr(cleaned))
    print("EMPTY :", sanitizer.is_empty(cleaned))