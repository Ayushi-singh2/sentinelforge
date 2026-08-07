from __future__ import annotations

import logging

from app.core.logging import (
    setup_logging,
    get_logger,
)


print("-" * 50)
print("TEST: Logging")


setup_logging()

logger = get_logger(
    "sentinelforge.test"
)


assert isinstance(
    logger,
    logging.Logger,
)


logger.info(
    "SentinelForge logging test successful."
)


print(
    "Logging test passed."
)

print("-" * 50)