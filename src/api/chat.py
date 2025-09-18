import json
import time
import random
import logging
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import List, Optional
from src import config

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
    tools: Optional[List[dict]] = None
    tool_choice: Optional[str] = None

# Fillers
FILLERS = ["Ờ...", "Ah...", "Dạ...", "Vâng..."]

@router.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest) -> StreamingResponse:
    oai_request = request.model_dump(exclude_none=True)
    if "user_id" in oai_request:
        oai_request["user"] = oai_request.pop("user_id")

    oai_request["stream"] = True

    async def event_stream(oai_client, oai_request, request):
        tool_buffers = {}  # lưu arguments đang stream
        tool_names = {}  # map tool_call_id -> name

        try:
            # Random filler để "nói đệm"
            filler = random.choice(FILLERS)
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

            # Gọi OpenAI API (stream)
            stream = await oai_client.chat.completions.create(**oai_request)

            async for chunk in stream:
                chunk_dict = chunk.model_dump()

                for choice in chunk_dict.get("choices", []):
                    delta = choice.get("delta", {})

                    # --- Xử lý content bình thường ---
                    if "content" in delta and delta["content"] is not None:
                        logger.info(f"💬 Content delta: {delta['content']}")

                    # --- Xử lý tool calls ---
                    tool_calls = delta.get("tool_calls") or []
                    for tc in tool_calls:
                        tc_id = tc.get("id")
                        fn = tc.get("function", {})

                        if fn.get("name"):
                            tool_names[tc_id] = fn["name"]
                            logger.info(f"🔧 Tool name: {fn['name']} (id={tc_id})")

                        if "arguments" in fn:
                            tool_buffers.setdefault(tc_id, "")
                            tool_buffers[tc_id] += fn["arguments"]
                            logger.info(f"🧩 Partial args for {tc_id}: {fn['arguments']}")

                    # Yield chunk ra ngoài
                    yield f"data: {json.dumps(chunk_dict)}\n\n"

                    # --- Khi model báo finish tool_calls ---
                    if choice.get("finish_reason") == "tool_calls":
                        for tc_id, args in tool_buffers.items():
                            try:
                                parsed = json.loads(args)
                                tool_name = tool_names.get(tc_id, "unknown")
                                logger.info(f"✅ Final tool args for {tool_name} ({tc_id}): {parsed}")
                            except Exception as e:
                                logger.error(f"❌ Failed to parse args {args}: {e}")

                # (hết vòng for choice)

            # Kết thúc stream
            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Error in chat completion: {str(e)}", exc_info=True)
            logger.error(f"Request that caused error: {json.dumps(oai_request, default=str)}")
            yield f"data: {json.dumps({'error': 'Internal error occurred!'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
