from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from app.core.config import settings


def validate_api_key(request: Request):
    """
    Validate API key from request header.
    Raises HTTPException if invalid.
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


async def auth_middleware(request: Request, call_next):

    # Protect only API routes
    if request.url.path.startswith("/api"):

        api_key = request.headers.get("X-API-Key")

        if not api_key or api_key != settings.api_key:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Invalid or missing API key"
                },
            )

    return await call_next(request)