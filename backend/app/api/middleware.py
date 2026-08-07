from __future__ import annotations

import time
import uuid
import logging

from fastapi import Request


logger = logging.getLogger("sentinelforge.api")


async def request_middleware(
    request: Request,
    call_next,
):
    """
    Request logging middleware.

    Adds request id, logs start/end,
    and measures request processing time.
    """

    request_id = str(uuid.uuid4())

    start_time = time.time()


    logger.info(
        "Request started | id=%s | method=%s | path=%s",
        request_id,
        request.method,
        request.url.path,
    )


    response = await call_next(request)


    elapsed = time.time() - start_time


    logger.info(
        "Request completed | id=%s | status=%s | time=%.4fs",
        request_id,
        response.status_code,
        elapsed,
    )


    response.headers["X-Request-ID"] = request_id


    return response