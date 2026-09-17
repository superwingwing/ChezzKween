from fastapi import APIRouter, Request
from pydantic import BaseModel
import chess.pgn
import io
from supabase import create_client
import os
import hashlib
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter()

class PGNRequest(BaseModel):
    pgn: str
    user_id: str

def parse_pgn(pgn_text):
    game = chess.pgn.read_game(io.StringIO(pgn_text))
    if game is None:
        return None
    return {
        "white": game.headers.get("White", "Unknown"),
        "black": game.headers.get("Black", "Unknown"),
        "result": game.headers.get("Result", "*"),
        "white_elo": game.headers.get("WhiteElo"),
        "black_elo": game.headers.get("BlackElo")
    }

def extract_moves(pgn_text):
    game = chess.pgn.read_game(io.StringIO(pgn_text))
    if game is None:
        return []

    board = game.board()
    moves = []

    for move in game.mainline_moves():
        moves.append({"move": board.san(move)})
        board.push(move)

    return moves

@router.post("/upload_pgn")
def upload_pgn(data: PGNRequest, request: Request):
    pgn_text = data.pgn

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return {
            "success": False,
            "message": "Missing authorization token."
        }

    access_token = auth_header.replace("Bearer ", "").strip()
    if not access_token:
        return {
            "success": False,
            "message": "Invalid authorization token."
        }

    user_supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    user_supabase.postgrest.auth(access_token)

    if not pgn_text.strip():
        return {
            "success": False,
            "message": "PGN is empty."
        }

    pgn_hash = hashlib.sha256(
        pgn_text.encode("utf-8")
    ).hexdigest()

    existing = (
        user_supabase
        .table("review_games")
        .select("*")
        .eq("pgn_hash", pgn_hash)
        .limit(1)
        .execute()
    )

    if existing.data:
        print("EXISTING PGN FOUND - Game was NOT inserted again")
        return {
            "success": True,
            "message": "Existing game loaded",
            "data": existing.data[0],
            "existing": True
        }

    info = parse_pgn(pgn_text)

    if info is None:
        return {
            "success": False,
            "message": "Invalid PGN."
        }

    moves = extract_moves(pgn_text)

    result = (
        user_supabase
        .table("review_games")
        .insert({
            "pgn": pgn_text,
            "pgn_hash": pgn_hash,
            "user_id": data.user_id,
            "white_name": info["white"],
            "black_name": info["black"],
            "result": info["result"],
            "white_elo": info["white_elo"],
            "black_elo": info["black_elo"],
            "moves": moves
        })
        .execute()
    )

    print("NEW PGN STORED")
    print("PGN Hash:", pgn_hash)
    print("Game ID:", result.data[0]["id"] if result.data else None)

    return {
        "success": True,
        "message": "Game stored successfully",
        "data": result.data,
        "existing": False
    }
