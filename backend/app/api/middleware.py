from __future__ import annotations

import time
import uuid
import logging

from fastapi import Request

from app.core.logging import get_logger


logger = get_logger(
    "sentinelforge.api"
)


async def request_middleware(
    request: Request,
    call_next,
):
    """
    Global API middleware.

    Features:
    - Request ID generation
    - Request timing
    - Basic request logging
    """

    request_id = str(uuid.uuid4())

    start_time = time.time()

    request.state.request_id = request_id

    logger.info(
        "Request started | id=%s | method=%s | path=%s",
        request_id,
        request.method,
        request.url.path,
    )

    response = await call_next(request)

    duration = (
        time.time() - start_time
    )

    response.headers[
        "X-Request-ID"
    ] = request_id

    response.headers[
        "X-Process-Time"
    ] = str(round(duration, 4))

    logger.info(
        "Request completed | id=%s | status=%s | time=%ss",
        request_id,
        response.status_code,
        round(duration, 4),
    )

    return response