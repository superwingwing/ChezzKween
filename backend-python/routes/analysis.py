from fastapi import APIRouter, Request
from pydantic import BaseModel
from services.analysis_service import analyze_pgn, analyze_explored_move

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

    return analyze_pgn(
        data.pgn,
        access_token
    )

@router.post("/analyze-move")
def analyze_move(data: ExploreMoveRequest):
    return analyze_explored_move(
        fen=data.fen,
        move_uci=data.move_uci
    )
