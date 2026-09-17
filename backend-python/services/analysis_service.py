import chess
import chess.pgn
import io
import os
import hashlib
from dotenv import load_dotenv
from supabase import create_client
from engine.stockfish_engine import evaluate_position
from ml.coach.move_explanation import explain_move

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("SUPABASE_URL:", SUPABASE_URL)
print("SUPABASE_KEY loaded:", bool(SUPABASE_KEY))


def analyze_single_move(before, move, prev_eval=None):
    if move not in before.legal_moves:
        return {"error": "Illegal move"}

    mover = before.turn
    san_move = before.san(move)

    if prev_eval is None:
        before_eval_result = evaluate_position(before)
        prev_eval = before_eval_result["evaluation"]

    after = before.copy()
    after.push(move)

    eval_result = evaluate_position(after)
    current_eval = eval_result["evaluation"]

    coach = explain_move(
        before=before,
        after=after,
        move=move,
        played_move=san_move,
        best_move=eval_result["best_move"],
        pv=eval_result["pv"],
        evaluation_before=prev_eval,
        evaluation_after=current_eval
    )

    if after.is_checkmate():
        quality = "best"
    else:
        if mover == chess.WHITE:
            eval_change = current_eval - prev_eval
        else:
            eval_change = prev_eval - current_eval

        centipawn_loss = max(0, -eval_change)

        if centipawn_loss < 0.3:
            quality = "best"
        elif centipawn_loss < 0.7:
            quality = "good"
        elif centipawn_loss < 1.5:
            quality = "inaccuracy"
        elif centipawn_loss < 3:
            quality = "mistake"
        else:
            quality = "blunder"

    return {
        "fen": after.fen(),
        "evaluation": current_eval,
        "best_move": eval_result["best_move"],
        "pv": eval_result["pv"],
        "candidates": eval_result["candidates"],
        "quality": quality,
        "move": san_move,
        "explanation": coach["explanation"],
        "recommendation": coach["recommendation"]
    }


def analyze_pgn(pgn_text: str, access_token: str):
    if not access_token:
        return {
            "error": "Missing authentication token"
        }

    user_supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

    user_supabase.postgrest.auth(access_token)

    pgn_hash = hashlib.sha256(
        pgn_text.encode("utf-8")
    ).hexdigest()

    existing_game = (
        user_supabase
        .table("review_games")
        .select("id")
        .eq("pgn_hash", pgn_hash)
        .limit(1)
        .execute()
    )

    if not existing_game.data:
        return {
            "error": "Game was not found in review_games"
        }

    game_id = existing_game.data[0]["id"]

    print("Game ID:", game_id)
    print("PGN Hash:", pgn_hash)

    cached_analysis = (
        user_supabase
        .table("game_analysis")
        .select("*")
        .eq("game_id", game_id)
        .limit(1)
        .execute()
    )

    if cached_analysis.data:
        print("====================================")
        print("CACHED ANALYSIS FOUND")
        print("Game ID:", game_id)
        print("Stockfish analysis SKIPPED")
        print("====================================")

        return cached_analysis.data[0]["analysis_json"]

    game = chess.pgn.read_game(
        io.StringIO(pgn_text)
    )

    if game is None:
        return {
            "error": "Invalid PGN"
        }

    board = game.board()
    evaluations = []

    initial_eval_result = evaluate_position(board)
    prev_eval = initial_eval_result["evaluation"]

    move_number = 0

    for move in game.mainline_moves():
        move_number += 1
        before = board.copy()

        result = analyze_single_move(
            before=before,
            move=move,
            prev_eval=prev_eval
        )

        if "error" in result:
            return result

        result["move_number"] = move_number
        evaluations.append(result)

        board.push(move)
        prev_eval = result["evaluation"]

    print(
        f"Finished analysis. Moves analyzed: {len(evaluations)}"
    )

    analysis_result = {
        "evaluations": evaluations
    }

    try:
        user_supabase.table("game_analysis").insert({
            "game_id": game_id,
            "analysis_json": analysis_result
        }).execute()

        print("====================================")
        print("NEW ANALYSIS SAVED")
        print("Game ID:", game_id)
        print("Stockfish analysis stored")
        print("====================================")

    except Exception as error:
        print("FAILED TO SAVE ANALYSIS:", error)

    return analysis_result


def analyze_explored_move(
    fen: str,
    move_uci: str
):
    try:
        before = chess.Board(fen)
    except ValueError:
        return {"error": "Invalid FEN"}

    try:
        move = chess.Move.from_uci(move_uci)
    except ValueError:
        return {"error": "Invalid move"}

    return analyze_single_move(
        before=before,
        move=move
    )
