from fastapi import APIRouter
from pydantic import BaseModel
import chess.pgn
import io
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter()

class PGNRequest(BaseModel):
    pgn: str


def parse_pgn(pgn_text):
    game = chess.pgn.read_game(io.StringIO(pgn_text))

    return {
        "white": game.headers.get("White", "Unknown"),
        "black": game.headers.get("Black", "Unknown"),
        "result": game.headers.get("Result", "*"),
        "white_elo": game.headers.get("WhiteElo"),
        "black_elo": game.headers.get("BlackElo"),
    }


def extract_moves(pgn_text):
    game = chess.pgn.read_game(io.StringIO(pgn_text))
    board = game.board()

    moves = []

    for move in game.mainline_moves():
        san = board.san(move)
        moves.append({"move": san})
        board.push(move)

    return moves


@router.post("/upload_pgn")
def upload_pgn(data: PGNRequest):
    pgn_text = data.pgn

    info = parse_pgn(pgn_text)
    moves = extract_moves(pgn_text)

    result = supabase.table("review_games").insert({
        "pgn": pgn_text,
        "white_name": info["white"],
        "black_name": info["black"],
        "result": info["result"],
        "white_elo": info["white_elo"],
        "black_elo": info["black_elo"],
        "moves": moves
    }).execute()

    return {
        "message": "Game stored successfully",
        "data": result.data
    }