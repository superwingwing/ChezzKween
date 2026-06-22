from fastapi import APIRouter
from pydantic import BaseModel
from services.analysis_service import analyze_pgn

router = APIRouter()

class PGNRequest(BaseModel):
    pgn: str

@router.post("/analyze")
def analyze(data: PGNRequest):
    return analyze_pgn(data.pgn)