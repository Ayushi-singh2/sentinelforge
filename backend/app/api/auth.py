from fastapi import Request, HTTPException

from app.core.config import settings


def validate_api_key(request: Request):
    """
    Validate API key from request header.

    Raises:
        HTTPException 401 if invalid.
    """

    api_key = request.headers.get("X-API-Key")

    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API key",
        )

    if api_key != settings.api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
        )

    return True