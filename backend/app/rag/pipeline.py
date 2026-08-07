from __future__ import annotations

from typing import Any, Dict, List

from app.rag.guard import RAGGuard
from app.rag.sanitizer import RAGSanitizer
from app.rag.retriever import Retriever
from app.rag.generator import RAGGenerator
from app.rag.citation import CitationManager


class RAGPipeline:
    """
    Main entry point for the SentinelForge RAG pipeline.

    Flow:

        User Query
            ↓
        Sanitizer
            ↓
        Security Guard
            ↓
        Retriever
            ↓
        Context Validation
            ↓
        Generator
            ↓
        Answer Validation
            ↓
        Citation Manager
            ↓
        Final Response
    """

    def __init__(
        self,
        retriever: Retriever | None = None,
        sanitizer: RAGSanitizer | None = None,
        guard: RAGGuard | None = None,
        generator: RAGGenerator | None = None,
        citation_manager: CitationManager | None = None,
    ):
        """
        Initialize the RAG pipeline.

        Components can be injected for testing.
        """

        self.sanitizer = sanitizer or RAGSanitizer()
        self.guard = guard or RAGGuard()
        self.retriever = retriever or Retriever()
        self.generator = generator or RAGGenerator()
        self.citation_manager = (
            citation_manager or CitationManager()
        )

    def query(
        self,
        query: str,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """
        Execute the complete RAG pipeline.
        """

        # --------------------------------------------------
        # 1. Sanitize query
        # --------------------------------------------------

        sanitized_query = self.sanitizer.sanitize_query(
            query
        )

        if self.sanitizer.is_empty(
            sanitized_query
        ):
            return {
                "success": False,
                "query": sanitized_query,
                "answer": "",
                "results": [],
                "citations": [],
                "grounded": False,
                "reason": "Query cannot be empty.",
            }

        # --------------------------------------------------
        # 2. Security validation
        # --------------------------------------------------

        validation = self.guard.validate_query(
            sanitized_query
        )

        if not validation["allowed"]:
            return {
                "success": False,
                "query": sanitized_query,
                "answer": "",
                "results": [],
                "citations": [],
                "grounded": False,
                "reason": validation["reason"],
            }

        # --------------------------------------------------
        # 3. Retrieve documents
        # --------------------------------------------------

        results = self.retriever.retrieve(
            sanitized_query,
            top_k=top_k,
        )

        # --------------------------------------------------
        # 4. Validate context
        # --------------------------------------------------

        context_validation = self.guard.validate_context(
            results
        )

        if not context_validation["allowed"]:
            return {
                "success": False,
                "query": sanitized_query,
                "answer": "I could not find relevant information.",
                "results": [],
                "citations": [],
                "grounded": False,
                "reason": context_validation["reason"],
            }

        # --------------------------------------------------
        # 5. Generate answer
        # --------------------------------------------------

        generated = self.generator.generate(
            query=sanitized_query,
            documents=results,
        )

        # Support the generator returning a dictionary.
        if isinstance(generated, dict):

            answer = generated.get(
                "answer",
                "",
            )

            grounded = generated.get(
                "grounded",
                True,
            )

            generation_reason = generated.get(
                "reason"
            )

        else:
            # Defensive fallback if generator returns
            # a plain string.
            answer = str(generated)
            grounded = True
            generation_reason = None

        # --------------------------------------------------
        # 6. Validate answer
        # --------------------------------------------------

        answer_validation = self.guard.validate_answer(
            answer
        )

        if not answer_validation["allowed"]:
            return {
                "success": False,
                "query": sanitized_query,
                "answer": "",
                "results": results,
                "citations": [],
                "grounded": False,
                "reason": answer_validation["reason"],
            }

        # --------------------------------------------------
        # 7. Extract citations
        # --------------------------------------------------

        citations = self.citation_manager.extract_citations(
            results
        )

        formatted_citations = (
            self.citation_manager.format_citations(
                citations
            )
        )

        # --------------------------------------------------
        # 8. Final response
        # --------------------------------------------------

        return {
            "success": True,
            "query": sanitized_query,
            "answer": answer,
            "results": results,
            "citations": citations,
            "formatted_citations": formatted_citations,
            "grounded": grounded,
            "reason": generation_reason,
        }

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Convenience method returning only retrieved documents.
        """

        response = self.query(
            query=query,
            top_k=top_k,
        )

        return response["results"]