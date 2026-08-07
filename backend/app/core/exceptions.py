from __future__ import annotations

from typing import Optional


class SentinelForgeException(Exception):
    """
    Base exception for SentinelForge.
    """

    def __init__(
        self,
        message: str,
        code: str = "internal_error",
    ):
        self.message = message
        self.code = code

        super().__init__(message)


class ValidationError(SentinelForgeException):
    """
    Raised when user input validation fails.
    """

    def __init__(
        self,
        message: str,
    ):
        super().__init__(
            message=message,
            code="validation_error",
        )


class RetrievalError(SentinelForgeException):
    """
    Raised when retrieval fails.
    """

    def __init__(
        self,
        message: str,
    ):
        super().__init__(
            message=message,
            code="retrieval_error",
        )


class GenerationError(SentinelForgeException):
    """
    Raised when answer generation fails.
    """

    def __init__(
        self,
        message: str,
    ):
        super().__init__(
            message=message,
            code="generation_error",
        )


def exception_response(
    exc: SentinelForgeException,
) -> dict:
    """
    Convert exception into API-safe response.
    """

    return {
        "success": False,
        "error": {
            "code": exc.code,
            "message": exc.message,
        },
    }