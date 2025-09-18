import json
import time
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
    role: str   # system, user, assistant, tool
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


@router.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest) -> StreamingResponse:
    oai_request = request.model_dump(exclude_none=True)

    # Map user_id to user (OpenAI spec)
    if "user_id" in oai_request:
        oai_request["user"] = oai_request.pop("user_id")

    oai_request["stream"] = True

    # Log toàn bộ request
    logger.info("📩 Incoming ElevenLabs request:\n%s",
                json.dumps(oai_request, ensure_ascii=False, indent=2))

    async def event_stream():
        try:
            # Stream từ OpenAI
            stream = await oai_client.chat.completions.create(**oai_request)

            async for chunk in stream:
                chunk_dict = chunk.model_dump()

                # Debug log
                for choice in chunk_dict.get("choices", []):
                    delta = choice.get("delta", {})
                    if "tool_calls" in delta:
                        logger.info("🔧 Tool delta: %s",
                                    json.dumps(delta["tool_calls"], ensure_ascii=False))
                    if "content" in delta:
                        logger.info("💬 Content delta: %s", delta["content"])
                    if choice.get("finish_reason"):
                        logger.info("🏁 Finish reason: %s", choice["finish_reason"])

                yield f"data: {json.dumps(chunk_dict, ensure_ascii=False)}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"❌ Error in chat completion: {str(e)}", exc_info=True)
            logger.error("🚨 Request that caused error: %s",
                         json.dumps(oai_request, default=str, ensure_ascii=False))
            yield f"data: {json.dumps({'error': 'Internal error occurred!'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
