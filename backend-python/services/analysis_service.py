import chess
import chess.pgn
import io
import os
import hashlib

from dotenv import load_dotenv
from supabase import create_client

from engine.stockfish_engine import (
    evaluate_fast,
    evaluate_critical
)

from ml.coach.move_explanation import explain_move
from ml.coach.style_move_filter import filter_candidates_by_style


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_player_style(user_supabase):
    try:
        response = (
            user_supabase
            .table("style")
            .select("predicted_style")
            .execute()
        )

        data = response.data or []

        aggressive = sum(
            1
            for game in data
            if game.get("predicted_style") == "Aggressive"
        )

        positional = sum(
            1
            for game in data
            if game.get("predicted_style") == "Positional"
        )

        total = aggressive + positional

        if total == 0:
            return {
                "Aggressive": 50.0,
                "Positional": 50.0
            }

        return {
            "Aggressive": round(aggressive / total * 100, 2),
            "Positional": round(positional / total * 100, 2)
        }

    except Exception as error:
        print("FAILED TO LOAD PLAYER STYLE:", error)

        return {
            "Aggressive": 50.0,
            "Positional": 50.0
        }


def determine_quality(
    before,
    after,
    prev_eval,
    current_eval
):
    if after.is_checkmate():
        return "best"

    if prev_eval is None or current_eval is None:
        return None

    if before.turn == chess.WHITE:
        eval_change = current_eval - prev_eval
    else:
        eval_change = prev_eval - current_eval

    centipawn_loss = max(0, -eval_change)

    if centipawn_loss < 0.3:
        return "best"

    if centipawn_loss < 0.7:
        return "good"

    if centipawn_loss < 1.5:
        return "inaccuracy"

    if centipawn_loss < 3:
        return "mistake"

    return "blunder"


def analyze_single_move(
    before,
    move,
    prev_eval=None,
    player_style=None,
    position_analysis=None,
    after_analysis=None
):
    if move not in before.legal_moves:
        return {"error": "Illegal move"}

    if player_style is None:
        player_style = {
            "Aggressive": 50.0,
            "Positional": 50.0
        }

    mover = before.turn
    san_move = before.san(move)

    if position_analysis is None:
        position_analysis = evaluate_fast(before)

    if prev_eval is None:
        prev_eval = position_analysis["evaluation"]

    stockfish_best = position_analysis["best_move"]

    after = before.copy()
    after.push(move)

    if after_analysis is None:
        after_analysis = evaluate_fast(after)

    current_eval = after_analysis["evaluation"]

    quality = determine_quality(
        before,
        after,
        prev_eval,
        current_eval
    )

    if quality in [
        "inaccuracy",
        "mistake",
        "blunder"
    ]:
        position_analysis = evaluate_critical(before)
        after_analysis = evaluate_critical(after)

        current_eval = after_analysis["evaluation"]
        stockfish_best = position_analysis["best_move"]

        quality = determine_quality(
            before,
            after,
            prev_eval,
            current_eval
        )

    candidates = position_analysis["candidates"]

    style_result = {
        "style_recommended": None,
        "playable_alternatives": []
    }

    style_recommended = None

    if quality in [
        "inaccuracy",
        "mistake",
        "blunder"
    ]:
        style_result = filter_candidates_by_style(
            board=before,
            candidates=candidates,
            player_aggressive=player_style["Aggressive"],
            player_positional=player_style["Positional"]
        )

        style_recommended = style_result.get(
            "style_recommended"
        )

    coach = explain_move(
        before=before,
        after=after,
        move=move,
        played_move=san_move,
        best_move=stockfish_best,
        pv=position_analysis["pv"],
        evaluation_before=prev_eval,
        evaluation_after=current_eval
    )

    recommendation = None

    if quality in [
        "inaccuracy",
        "mistake",
        "blunder"
    ]:
        recommendation = coach.get("recommendation")

    return {
        "fen": after.fen(),
        "evaluation": current_eval,
        "best_move": stockfish_best,
        "pv": position_analysis["pv"],
        "candidates": candidates,
        "player_style": player_style,
        "quality": quality,
        "move": san_move,
        "explanation": coach.get("explanation"),
        "recommendation": recommendation,
        "style_recommended_move": (
            style_recommended.get("move")
            if style_recommended
            else None
        ),
        "style_alternatives": (
            style_result.get(
                "playable_alternatives",
                []
            )
            if quality in [
                "inaccuracy",
                "mistake",
                "blunder"
            ]
            else []
        )
    }


def analyze_pgn(
    pgn_text: str,
    access_token: str
):
    if not access_token:
        return {
            "error": "Missing authentication token"
        }

    user_supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

    user_supabase.postgrest.auth(
        access_token
    )

    player_style = get_player_style(
        user_supabase
    )

    print(
        "PLAYER STYLE:",
        player_style
    )

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
            "error":
            "Game was not found in review_games"
        }

    game_id = existing_game.data[0]["id"]

    cached_analysis = (
        user_supabase
        .table("game_analysis")
        .select("*")
        .eq("game_id", game_id)
        .limit(1)
        .execute()
    )

    if cached_analysis.data:
        return cached_analysis.data[0][
            "analysis_json"
        ]

    game = chess.pgn.read_game(
        io.StringIO(pgn_text)
    )

    if game is None:
        return {
            "error": "Invalid PGN"
        }

    board = game.board()

    evaluations = []

    current_analysis = evaluate_fast(
        board
    )

    prev_eval = current_analysis[
        "evaluation"
    ]

    for move_number, move in enumerate(
        game.mainline_moves(),
        start=1
    ):
        before = board.copy()

        after = before.copy()
        after.push(move)

        next_analysis = evaluate_fast(
            after
        )

        result = analyze_single_move(
            before=before,
            move=move,
            prev_eval=prev_eval,
            player_style=player_style,
            position_analysis=current_analysis,
            after_analysis=next_analysis
        )

        if "error" in result:
            return result

        result["move_number"] = move_number

        evaluations.append(
            result
        )

        board.push(move)

        prev_eval = result[
            "evaluation"
        ]

        current_analysis = next_analysis

    analysis_result = {
        "evaluations": evaluations
    }

    try:
        (
            user_supabase
            .table("game_analysis")
            .insert({
                "game_id": game_id,
                "analysis_json": analysis_result
            })
            .execute()
        )

    except Exception as error:
        print(
            "FAILED TO SAVE ANALYSIS:",
            error
        )

    return analysis_result


def analyze_explored_move(
    fen: str,
    move_uci: str
):
    try:
        before = chess.Board(fen)
        move = chess.Move.from_uci(
            move_uci
        )

    except ValueError:
        return {
            "error":
            "Invalid FEN or move"
        }

    return analyze_single_move(
        before=before,
        move=move
    )