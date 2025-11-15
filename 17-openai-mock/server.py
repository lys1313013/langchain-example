from typing import Any, Dict, List, Optional
import asyncio
import time
import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


app = FastAPI(title="OpenAI Mock API", version="0.1.0")


class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "gpt-4o-mini"
    messages: List[Dict[str, Any]]
    stream: bool = True


def _build_chunk(payload: Dict[str, Any]) -> bytes:
    return ("data: " + json.dumps(payload, ensure_ascii=False) + "\n\n").encode("utf-8")


def _extract_user_content(messages: List[Dict[str, Any]]) -> str:
    for m in reversed(messages):
        if m.get("role") == "user":
            return str(m.get("content", ""))
    return ""


def _make_reply(content: str) -> str:
    if not content:
        content = "你好，我是一个模拟的 OpenAI 接口。"
    return f"这是一个模拟响应：{content}"


def _usage(input_text: str, output_text: str) -> Dict[str, int]:
    return {
        "prompt_tokens": len(input_text),
        "completion_tokens": len(output_text),
        "total_tokens": len(input_text) + len(output_text),
    }


def _nonstream_payload(model: str, content: str, reply: str, now: int) -> Dict[str, Any]:
    return {
        "id": f"mockcmpl_{now}",
        "object": "chat.completion",
        "created": now,
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": reply},
                "finish_reason": "stop",
            }
        ],
        "usage": _usage(content, reply),
    }


async def _chat_stream(messages: List[Dict[str, Any]], model: str):
    now = int(time.time())
    content = _extract_user_content(messages)
    reply = _make_reply(content)

    first_chunk = {
        "id": f"mockcmpl_{now}",
        "object": "chat.completion.chunk",
        "created": now,
        "model": model,
        "choices": [
            {"index": 0, "delta": {"role": "assistant"}, "finish_reason": None}
        ],
    }
    yield _build_chunk(first_chunk)
    await asyncio.sleep(0.02)

    for token in list(reply):
        chunk = {
            "id": f"mockcmpl_{now}",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {"index": 0, "delta": {"content": token}, "finish_reason": None}
            ],
        }
        yield _build_chunk(chunk)
        await asyncio.sleep(0.02)

    yield b"data: [DONE]\n\n"


@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    model = req.model or "gpt-4o-mini"
    if req.stream:
        gen = _chat_stream(req.messages, model)
        headers = {
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
        return StreamingResponse(gen, media_type="text/event-stream", headers=headers)
    else:
        now = int(time.time())
        content = _extract_user_content(req.messages)
        reply = _make_reply(content)
        return _nonstream_payload(model, content, reply, now)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=13130)