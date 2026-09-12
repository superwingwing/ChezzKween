from fastapi import APIRouter
from pydantic import BaseModel
from services.analysis_service import (
    analyze_pgn,
    analyze_explored_move
)

router = APIRouter()

# PGN ANALYSIS REQUEST
class PGNRequest(BaseModel):
    pgn: str

# MANUAL MOVE ANALYSIS REQUEST
class ExploreMoveRequest(BaseModel):
    fen: str
    move_uci: str

# ANALYZE UPLOADED PGN
@router.post("/analyze")
def analyze(data: PGNRequest):
    return analyze_pgn(data.pgn)

# ANALYZE MANUALLY EXPLORED MOVE
@router.post("/analyze-move")
def analyze_move(data: ExploreMoveRequest):
    return analyze_explored_move(
        fen=data.fen,
        move_uci=data.move_uci
    )