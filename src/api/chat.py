import json
import os
import random
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
import logging
from pydantic import BaseModel
from typing import List, Optional
from src import config

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

# List of fillers to randomize
FILLERS = [
    "Uhm… ",
    "Ah… ",
    "Let me think… ",
    "Yes… ",
]

@router.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest) -> StreamingResponse:
    oai_request = request.model_dump(exclude_none=True)
    if "user_id" in oai_request:
        oai_request["user"] = oai_request.pop("user_id")

    async def event_stream():
        try:
            # Pick a random filler for this turn
            filler = random.choice(FILLERS)
            initial_chunk = {
                "id": "chatcmpl-buffer",
                "object": "chat.completion.chunk",
                "created": int(os.times().elapsed),
                "model": request.model,
                "choices": [{
                    "delta": {"content": filler},
                    "index": 0,
                    "finish_reason": None
                }]
            }
            yield f"data: {json.dumps(initial_chunk)}\n\n"

            # Now forward actual LLM response
            stream = await oai_client.chat.completions.create(**oai_request, stream=True)
            async for chunk in stream:
                yield f"data: {json.dumps(chunk.model_dump())}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            logging.error("An error occurred: %s", str(e))
            yield f"data: {json.dumps({'error': 'Internal error occurred'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
