import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):

        request_id = str(uuid.uuid4())

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        response.headers["X-Request-ID"] = request_id

        response.headers["X-Process-Time"] = str(
            process_time
        )

        return response



async def request_middleware(
    request: Request,
    call_next,
):
    """
    Function based middleware compatibility.
    """

    middleware = RequestMiddleware(
        app=None
    )

    return await middleware.dispatch(
        request,
        call_next,
    )