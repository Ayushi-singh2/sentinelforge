from __future__ import annotations

import time

from collections import defaultdict


class RateLimiter:
    """
    Simple in-memory rate limiter.
    """

    def __init__(
        self,
        limit: int = 60,
        window: int = 60,
    ):
        self.limit = limit
        self.window = window

        self.requests = defaultdict(list)


    def check(
        self,
        client_id: str,
    ):

        now = time.time()

        history = self.requests[
            client_id
        ]

        history[:] = [
            timestamp
            for timestamp in history
            if now - timestamp < self.window
        ]


        if len(history) >= self.limit:
            return False


        history.append(now)

        return True