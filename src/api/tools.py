import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Tuple
import time
import openai

from src import config

client = openai.OpenAI()
router = APIRouter(prefix="/tools", tags=["tools"])
logger = logging.getLogger(__name__)

data = {
        "ten": "Nguyễn Thị Cam",
        "cccd": "528981176214",
        "dob": "18-09-1989",
        "phone": "0955423314"
    }

class ConfirmIdentityRequest(BaseModel):
    name: str = Field(..., description="Customer full name")
    cccd: str = Field(..., description="Citizen identification number")
    phone: str = Field(..., description="Phone number")
    dob: str = Field(..., description="Date of birth, DD-MM-YYYY")
    session_id: Optional[str] = Field(
        default=None,
        description="Session identifier for retry tracking",
    )


class ConfirmIdentityResponse(BaseModel):
    verified: bool
    locked: bool = False


# In-memory retry tracking with soft TTL per session
_sessions: Dict[str, Tuple[int, float]] = {}


def _now() -> float:
    return time.time()


def _cleanup_sessions() -> None:
    if not _sessions:
        return
    cutoff = _now() - config.session_ttl_seconds
    expired = [sid for sid, (_, ts) in _sessions.items() if ts < cutoff]
    for sid in expired:
        _sessions.pop(sid, None)


def _bump_retry(session_id: str) -> int:
    _cleanup_sessions()
    retries, _ = _sessions.get(session_id, (0, _now()))
    retries += 1
    _sessions[session_id] = (retries, _now())
    return retries


@router.post("/confirm-identity", response_model=ConfirmIdentityResponse)
def confirm_identity(req: ConfirmIdentityRequest):
    logger.info(
        "Confirm identity request received",
        extra={
            "request_id": getattr(req, "session_id", None),
        },
    )
    # Ensure expected values are configured
    ok = (
        req.name.strip() == data["ten"]
        and req.cccd.strip() == data["cccd"]
        and req.phone.strip() == data["phone"]
        and req.dob.strip() == data["dob"]
    )

    if ok:
        if req.session_id:
            _sessions.pop(req.session_id, None)
        logger.info("Identity verified", extra={"request_id": req.session_id})
        return ConfirmIdentityResponse(verified=True, locked=False)

    if req.session_id:
        retries = _bump_retry(req.session_id)
        if retries > config.max_retries:
            logger.warning(
                "Session locked after retries",
                extra={"request_id": req.session_id, "retries": retries},
            )
            return ConfirmIdentityResponse(verified=False, locked=True)
        logger.info(
            "Identity check failed",
            extra={"request_id": req.session_id, "retries": retries},
        )
        return ConfirmIdentityResponse(verified=False, locked=False)

    logger.info("Identity check failed without session")
    return ConfirmIdentityResponse(verified=False, locked=False)


class SearchVenueRequest(BaseModel):
    venue_name: str = Field(..., description="Name of the venue to search for")


class SearchVenueResponse(BaseModel):
    output_text: str


@router.post("/search-venue", response_model=SearchVenueResponse)
def search_venue(req: SearchVenueRequest):
    try:
        query = f"How How to book a table at {req.venue_name}, including hotline, exact name of the restaurant, required information to book a table, opening and closing hours, priority for a few branches near the waterfront building 1A Ton Duc Thang, Saigon, District 1."
        response = client.responses.create(
            model="gpt-4.1",
            tools=[{"type": "web_search"}],
            input=query,
        )
        return SearchVenueResponse(output_text=response.output_text)
    except Exception as e:
        logger.error(f"search_venue error: {e}")
        raise HTTPException(status_code=500, detail="Failed to search venue information.")
