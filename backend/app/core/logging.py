from __future__ import annotations

import logging
import sys

from app.core.config import settings


def setup_logging() -> None:
    """
    Configure application logging.
    """

    level = (
        logging.DEBUG
        if settings.debug
        else logging.INFO
    )

    logging.basicConfig(
        level=level,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
    )


def get_logger(
    name: str,
) -> logging.Logger:
    """
    Return a configured logger.
    """

    return logging.getLogger(name)