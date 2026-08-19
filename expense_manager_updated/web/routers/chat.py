from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from web.schemas import ChatRequest
from web.streaming import run_turn, stream_turn

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/stream")
async def chat_stream(req: ChatRequest):
    return StreamingResponse(
        stream_turn(req.message), media_type="application/x-ndjson"
    )


@router.post("")
async def chat_complete(req: ChatRequest):
    return await run_turn(req.message)
