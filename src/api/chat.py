import json
import os
import random
import time

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
import logging
from pydantic import BaseModel
from typing import List, Optional
from src import config

# Configure logger for this module
logger = logging.getLogger(__name__)

router = APIRouter()
oai_client = AsyncOpenAI(api_key=config.openai_api_key)

# Schema
class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    messages: List[Message]
    model: str
    temperature: Optional[float] = 0.3
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False
    user_id: Optional[str] = None
    tools: Optional[List[dict]] = None  # Add this
    tool_choice: Optional[str] = None   # Add this

# List of fillers to randomize
FILLERS = [
    "Ờ...",
    "Ah...",
    "Dạ...",
    "Vâng...",
]

@router.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest) -> StreamingResponse:
    oai_request = request.model_dump(exclude_none=True)
    logger.info(oai_request)
    if "user_id" in oai_request:
        oai_request["user"] = oai_request.pop("user_id")

    oai_request["stream"] = True

    async def event_stream():
        try:
            # Randomly select a filler
            filler = random.choice(FILLERS)
            logger.debug(f"Selected filler: '{filler}'")

            # Send initial buffer chunk while processing
            initial_chunk = {
                "id": "chatcmpl-buffer",
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": request.model,
                "choices": [{
                    "delta": {"content": f"{filler} "},
                    "index": 0,
                    "finish_reason": None
                }]
            }
            yield f"data: {json.dumps(initial_chunk)}\n\n"

            # Process the actual LLM response
            chat_completion_coroutine = await oai_client.chat.completions.create(**oai_request)

            async for chunk in chat_completion_coroutine:
                chunk_dict = chunk.model_dump()
                yield f"data: {json.dumps(chunk_dict)}\n\n"
            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Error in chat completion: {str(e)}", exc_info=True)
            logger.error(f"Request that caused error: {json.dumps(oai_request, default=str)}")
            yield f"data: {json.dumps({'error': 'Internal error occurred!'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")