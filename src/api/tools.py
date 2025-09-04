from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Dict, Tuple
import time

from src import config


router = APIRouter(prefix="/tools", tags=["tools"])

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
        return ConfirmIdentityResponse(verified=True, locked=False)

    if req.session_id:
        retries = _bump_retry(req.session_id)
        if retries > config.max_retries:
            return ConfirmIdentityResponse(verified=False, locked=True)
        return ConfirmIdentityResponse(verified=False, locked=False)

    return ConfirmIdentityResponse(verified=False, locked=False)

