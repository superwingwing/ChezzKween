import chess
import chess.pgn
import io

from engine.stockfish_engine import evaluate_position
from ml.coach.move_explanation import explain_move


def analyze_pgn(pgn_text: str):
    game = chess.pgn.read_game(io.StringIO(pgn_text))

    if game is None:
        return {
            "error": "Invalid PGN"
        }

    board = game.board()
    evaluations = []

    # ==========================================================
    # EVALUATE THE INITIAL POSITION
    # ==========================================================

    initial_eval_result = evaluate_position(board)
    prev_eval = initial_eval_result["evaluation"]

    # ==========================================================
    # ANALYZE EVERY MOVE
    # ==========================================================

    for move in game.mainline_moves():

        # ------------------------------------------------------
        # POSITION BEFORE THE MOVE
        # ------------------------------------------------------

        before = board.copy()

        # Convert UCI move to proper SAN notation
        # Example:
        # d4c5 -> Bc5
        san_move = before.san(move)

        # The player who is actually making the move
        mover = board.turn

        # ------------------------------------------------------
        # PLAY THE MOVE
        # ------------------------------------------------------

        board.push(move)

        # Position AFTER the move
        after = board.copy()

        # ------------------------------------------------------
        # STOCKFISH EVALUATION
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # CHECKMATE = ALWAYS BEST
        # ------------------------------------------------------

        if after.is_checkmate():
            quality = "best"

        else:
            if mover == chess.WHITE:
                eval_change = current_eval - prev_eval
            else:
                eval_change = prev_eval - current_eval

            # Only a negative change means the player
            # lost evaluation.
            centipawn_loss = max(0, -eval_change)

            # --------------------------------------------------
            # CLASSIFY MOVE
            # --------------------------------------------------

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

        # ======================================================
        # SAVE RESULT
        # ======================================================

        evaluations.append({
            "fen": board.fen(),

            # Stockfish evaluation
            "evaluation": current_eval,

            # Stockfish engine values remain UCI internally
            "best_move": eval_result["best_move"],
            "pv": eval_result["pv"],
            "candidates": eval_result["candidates"],

            # Move quality
            "quality": quality,

            # Displayed move uses professional SAN notation
            "move": san_move,

            # Coaching information
            "explanation": coach["explanation"],
            "recommendation": coach["recommendation"]
        })

        # ======================================================
        # CURRENT POSITION BECOMES PREVIOUS POSITION
        # ======================================================

        prev_eval = current_eval

    # ==========================================================
    # FINISHED
    # ==========================================================

    print(
        f"Finished analysis. Moves analyzed: {len(evaluations)}"
    )

    return {
        "evaluations": evaluations
    }