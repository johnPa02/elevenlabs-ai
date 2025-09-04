import logging
import os
import sys
from typing import Any, Dict
import json


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        data: Dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "time": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"),
        }
        if record.exc_info:
            data["exc_info"] = self.formatException(record.exc_info)
        # Common extras if present
        for key in ("request_id", "method", "path", "status_code", "client", "process_ms"):
            if key in record.__dict__:
                data[key] = record.__dict__[key]
        return json.dumps(data, ensure_ascii=False)


def setup_logging() -> None:
    """Configure root and library loggers.

    Env vars:
    - LOG_LEVEL: DEBUG, INFO, WARNING, ERROR (default INFO)
    - LOG_FORMAT: "json" or "console" (default console)
    """
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    fmt = os.getenv("LOG_FORMAT", "console").lower()

    root = logging.getLogger()
    # Clear existing handlers to avoid duplicate logs in reloads
    for h in list(root.handlers):
        root.removeHandler(h)

    handler = logging.StreamHandler(stream=sys.stdout)
    if fmt == "json":
        formatter: logging.Formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    handler.setFormatter(formatter)

    root.addHandler(handler)
    root.setLevel(level)

    # Align common third-party loggers
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
