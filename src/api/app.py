import logging
import time
import uuid
from fastapi import FastAPI, Request

from src.api.tools import router as tools_router
from src.api.chat import router as chat_router
from src.utils.logging_config import setup_logging


# Initialize logging before app creation
setup_logging()

app = FastAPI(title="ElevenLabs Server", version="0.1.0")
logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    start = time.perf_counter()
    status_code = None
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    except Exception:
        status_code = 500
        logger.exception("Unhandled error during request", extra={"request_id": request_id})
        raise
    finally:
        process_ms = (time.perf_counter() - start) * 1000
        extra = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": status_code,
            "client": request.client.host if request.client else None,
            "process_ms": round(process_ms, 2),
        }
        logger.info("📩 HTTP request", extra=extra)


@app.get("/health")
def health():
    return {"status": "ok"}


# Mount server tools under /tools prefix
app.include_router(tools_router)

# Mount LLM endpoint
app.include_router(chat_router)


@app.on_event("startup")
async def on_startup():
    logger.info("FastAPI application startup complete")
