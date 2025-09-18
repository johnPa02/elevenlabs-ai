import json
import os
import random
import time

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
import logging
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from src import config

# Configure logger for this module
logger = logging.getLogger(__name__)

router = APIRouter()
oai_client = AsyncOpenAI(api_key=config.openai_api_key)

class Message(BaseModel):
    role: str  # "user", "assistant", "tool", "system"
    content: Optional[str] = None  # text content
    tool_calls: Optional[List[Dict[str, Any]]] = None  # khi assistant gọi function
    tool_call_id: Optional[str] = None  # khi tool trả về kết quả
    name: Optional[str] = None  # tên tool (trong message role=tool)

class ChatCompletionRequest(BaseModel):
    messages: List[Message]
    model: str
    temperature: Optional[float] = 0.3
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False
    user_id: Optional[str] = None
    tools: Optional[List[dict]] = None
    tool_choice: Optional[str] = None

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

            # Send initial filler chunk
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

            # Call OpenAI
            chat_completion_coroutine = await oai_client.chat.completions.create(**oai_request)

            tool_call_buffers = {}

            async for chunk in chat_completion_coroutine:
                chunk_dict = chunk.model_dump()

                for choice in chunk_dict.get("choices", []):
                    delta = choice.get("delta", {})

                    # Content -> stream ngay
                    if "content" in delta and delta["content"] is not None:
                        logger.info(f"💬 Assistant delta: {delta['content']}")
                        yield f"data: {json.dumps(chunk_dict)}\n\n"

                    # Tool calls -> chỉ buffer, không stream ra
                    if "tool_calls" in delta and delta["tool_calls"] is not None:
                        for call in delta["tool_calls"]:
                            idx = call["index"]
                            buf = tool_call_buffers.setdefault(idx, {"arguments": ""})
                            fn = call.get("function", {})

                            if call.get("id"):
                                buf["id"] = call["id"]
                            if fn.get("name"):
                                buf["name"] = fn["name"]
                            if fn.get("arguments"):
                                buf["arguments"] += fn["arguments"]

                    # Finish reason
                    if choice.get("finish_reason") == "tool_calls":
                        for idx, buf in tool_call_buffers.items():
                            try:
                                args = json.loads(buf["arguments"])
                            except Exception as e:
                                logger.error(f"❌ Failed to parse tool args: {buf['arguments']} ({e})")
                                args = buf["arguments"]

                            # Emit 1 chunk hoàn chỉnh duy nhất cho tool_call
                            tool_chunk = {
                                "id": buf.get("id", f"tool_{idx}"),
                                "object": "chat.completion.chunk",
                                "created": int(time.time()),
                                "model": request.model,
                                "choices": [{
                                    "delta": {
                                        "tool_calls": [{
                                            "index": idx,
                                            "id": buf.get("id", f"tool_{idx}"),
                                            "type": "function",
                                            "function": {
                                                "name": buf.get("name"),
                                                "arguments": json.dumps(args, ensure_ascii=False)
                                            }
                                        }]
                                    },
                                    "index": 0,
                                    "finish_reason": "tool_calls"
                                }]
                            }
                            logger.info(f"✅ Final tool call emitted: {tool_chunk}")
                            yield f"data: {json.dumps(tool_chunk)}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Error in chat completion: {str(e)}", exc_info=True)
            logger.error(f"Request that caused error: {json.dumps(oai_request, default=str)}")
            yield f"data: {json.dumps({'error': 'Internal error occurred!'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")