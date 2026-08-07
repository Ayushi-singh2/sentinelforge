from __future__ import annotations

import re
from typing import Any, Dict, List


class RAGGenerator:
    """
    Generates answers from retrieved RAG documents.

    The generator performs two checks:

    1. Query/context relevance
    2. Answer/context grounding
    """

    STOP_WORDS = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "for",
        "from",
        "has",
        "have",
        "how",
        "i",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "that",
        "the",
        "this",
        "to",
        "was",
        "what",
        "when",
        "where",
        "which",
        "who",
        "with",
    }

    def __init__(
        self,
        min_grounding_score: float = 0.60,
        min_relevance_score: float = 0.20,
    ):
        self.min_grounding_score = min_grounding_score
        self.min_relevance_score = min_relevance_score

    def generate(
        self,
        query: str,
        documents: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generate an answer using retrieved documents.
        """

        if not query or not query.strip():
            return {
                "answer": "",
                "grounded": False,
                "reason": "Query cannot be empty.",
                "citations": [],
            }

        if not documents:
            return {
                "answer": "I could not find relevant information.",
                "grounded": False,
                "reason": "No relevant documents found.",
                "citations": [],
            }

        usable_documents = [
            document
            for document in documents
            if document.get("content")
            and document["content"].strip()
        ]

        if not usable_documents:
            return {
                "answer": "",
                "grounded": False,
                "reason": "Retrieved documents contain no usable content.",
                "citations": [],
            }

        relevance = self._calculate_relevance(
            query,
            usable_documents,
        )

        if relevance < self.min_relevance_score:
            return {
                "answer": "I could not find relevant information in the retrieved documents.",
                "grounded": False,
                "reason": "Retrieved context does not appear relevant to the query.",
                "citations": [],
            }

        answer = self._build_answer(
            usable_documents
        )

        grounding = self.validate_grounding(
            answer,
            usable_documents,
        )

        citations = []

        for document in usable_documents:
            citation = document.get("citation")

            if citation:
                citations.append(citation)

        return {
            "answer": answer,
            "grounded": grounding["grounded"],
            "reason": grounding["reason"],
            "citations": citations,
        }

    def _build_answer(
        self,
        documents: List[Dict[str, Any]],
    ) -> str:
        """
        Build a simple answer from retrieved context.

        Later this method can be replaced with an LLM call.
        """

        contents = []

        for document in documents:

            content = document.get(
                "content",
                "",
            ).strip()

            if content:
                contents.append(content)

        return "\n\n".join(contents)

    def _calculate_relevance(
        self,
        query: str,
        documents: List[Dict[str, Any]],
    ) -> float:
        """
        Calculate lexical overlap between the query
        and retrieved document content.
        """

        query_words = set(
            self._meaningful_words(query)
        )

        if not query_words:
            return 0.0

        context = " ".join(
            document.get("content", "")
            for document in documents
        )

        context_words = set(
            self._meaningful_words(context)
        )

        if not context_words:
            return 0.0

        overlap = query_words.intersection(
            context_words
        )

        return len(overlap) / len(query_words)

    def validate_grounding(
        self,
        answer: str,
        documents: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Validate whether the answer is supported by
        retrieved documents.
        """

        if not answer or not answer.strip():
            return {
                "grounded": False,
                "reason": "Answer is empty.",
                "score": 0.0,
            }

        if not documents:
            return {
                "grounded": False,
                "reason": "No context available for grounding.",
                "score": 0.0,
            }

        context = " ".join(
            document.get("content", "")
            for document in documents
        )

        context_normalized = self._normalize(
            context
        )

        if not context_normalized:
            return {
                "grounded": False,
                "reason": "Retrieved context is empty.",
                "score": 0.0,
            }

        sentences = self._split_sentences(
            answer
        )

        if not sentences:
            return {
                "grounded": False,
                "reason": "Unable to identify answer claims.",
                "score": 0.0,
            }

        supported = 0

        for sentence in sentences:

            normalized_sentence = self._normalize(
                sentence
            )

            if not normalized_sentence:
                continue

            if self._sentence_supported(
                normalized_sentence,
                context_normalized,
            ):
                supported += 1

        total = len(sentences)

        score = (
            supported / total
            if total
            else 0.0
        )

        if score >= self.min_grounding_score:
            return {
                "grounded": True,
                "reason": None,
                "score": score,
            }

        return {
            "grounded": False,
            "reason": "Answer contains claims not supported by retrieved context.",
            "score": score,
        }

    def _sentence_supported(
        self,
        sentence: str,
        context: str,
    ) -> bool:
        """
        Check whether a sentence is supported by context.
        """

        if sentence in context:
            return True

        sentence_words = self._meaningful_words(
            sentence
        )

        if not sentence_words:
            return False

        context_words = set(
            self._meaningful_words(context)
        )

        overlap = sum(
            1
            for word in sentence_words
            if word in context_words
        )

        score = (
            overlap / len(sentence_words)
        )

        return score >= self.min_grounding_score

    @classmethod
    def _meaningful_words(
        cls,
        text: str,
    ) -> List[str]:
        """
        Extract meaningful normalized words.
        """

        normalized = cls._normalize(text)

        return [
            word
            for word in normalized.split()
            if word not in cls.STOP_WORDS
        ]

    @staticmethod
    def _normalize(
        text: str,
    ) -> str:
        """
        Normalize text for comparisons.
        """

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    @staticmethod
    def _split_sentences(
        text: str,
    ) -> List[str]:
        """
        Split text into sentences.
        """

        sentences = re.split(
            r"(?<=[.!?])\s+|\n+",
            text.strip(),
        )

        return [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]