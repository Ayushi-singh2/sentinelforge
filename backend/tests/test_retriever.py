import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)


from app.rag.retriever import Retriever


retriever = Retriever()


results = retriever.retrieve(
    "What is SentinelForge?",
    top_k=3
)


for result in results:

    print("\nCONTENT:")
    print(result["content"])

    print("\nSCORE:")
    print(result["score"])

    print("\nCITATION:")
    print(result["citation"])