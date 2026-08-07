from __future__ import annotations

from fastapi import Request, HTTPException

from app.core.config import settings


def validate_api_key(
    request: Request,
):
    """
    Validate API key.

    Header:
        X-API-Key

    If no API key is configured,
    authentication is disabled.
    """

    configured_key = settings.api_key

    # Development mode
    if not configured_key:
        return True


    request_key = request.headers.get(
        "X-API-Key"
    )


    if request_key != configured_key:

        raise HTTPException(
            status_code=401,
            detail={
                "error": "Invalid API key"
            },
        )


    return True