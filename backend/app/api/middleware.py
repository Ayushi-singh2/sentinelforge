from __future__ import annotations

import time
import uuid
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


logger = logging.getLogger("sentinelforge.api")


class RequestMiddleware(BaseHTTPMiddleware):
    """
    API request logging middleware.

    Adds:
    - Request ID
    - Processing time
    - Request lifecycle logs
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:

        request_id = str(uuid.uuid4())

        start_time = time.time()

        logger.info(
            f"Request started | "
            f"id={request_id} | "
            f"method={request.method} | "
            f"path={request.url.path}"
        )

        response = await call_next(request)

        process_time = round(
            time.time() - start_time,
            4,
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)

        logger.info(
            f"Request completed | "
            f"id={request_id} | "
            f"status={response.status_code} | "
            f"time={process_time}s"
        )

        return response