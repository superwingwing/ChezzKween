from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from services.analysis_service import (
    analyze_pgn,
    analyze_explored_move
)

import asyncio
import json
import queue
import threading


router = APIRouter()


class PGNRequest(BaseModel):
    pgn: str


class ExploreMoveRequest(BaseModel):
    fen: str
    move_uci: str


@router.post("/analyze")
def analyze(data: PGNRequest, request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return {
            "error": "Missing authorization token"
        }

    access_token = auth_header.replace(
        "Bearer ",
        ""
    ).strip()

    if not access_token:
        return {
            "error": "Invalid authorization token"
        }

    progress_queue = queue.Queue()

    def progress_callback(progress_data):
        progress_queue.put({
            "type": "progress",
            **progress_data
        })

    def worker():
        try:
            result = analyze_pgn(
                data.pgn,
                access_token,
                progress_callback
            )

            progress_queue.put({
                "type": "complete",
                "analysis": result
            })

        except Exception as error:
            progress_queue.put({
                "type": "error",
                "message": str(error)
            })

        finally:
            progress_queue.put(None)

    threading.Thread(
        target=worker,
        daemon=True
    ).start()

    async def event_stream():
        while True:
            item = await asyncio.to_thread(
                progress_queue.get
            )

            if item is None:
                break

            yield (
                f"data: {json.dumps(item)}\n\n"
            )

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )


@router.post("/analyze-move")
def analyze_move(data: ExploreMoveRequest):
    return analyze_explored_move(
        fen=data.fen,
        move_uci=data.move_uci
    )