import chess
import chess.pgn
import io

from engine.stockfish_engine import evaluate_position
from ml.coach.reason_detector import detect_reason
from ml.coach.explanation_engine import generate_explanation


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

        # Position BEFORE the move
        before = board.copy()

        # The player who is actually making the move
        mover = board.turn

        # Play the move
        board.push(move)

        # Position AFTER the move
        after = board.copy()

        # Evaluate the resulting position
        eval_result = evaluate_position(after)

        current_eval = eval_result["evaluation"]

        # ======================================================
        # DETECT WHY THE POSITION CHANGED
        # ======================================================

        reason_data = detect_reason(
            before,
            after,
            prev_eval,
            current_eval
        )

        # ======================================================
        # GENERATE COACHING EXPLANATION
        # ======================================================

        coach = generate_explanation(
            reason_data,
            move.uci(),
            eval_result["best_move"],
            eval_result["pv"],
            before,
            after
        )

        # ======================================================
        # MOVE QUALITY
        # ======================================================

        # ------------------------------------------------------
        # CHECKMATE = ALWAYS BEST
        # ------------------------------------------------------

        if after.is_checkmate():

            quality = "best"

        else:

            # --------------------------------------------------
            # Convert evaluation change to the perspective
            # of the player who actually made the move.
            #
            # Stockfish evaluation is White-perspective:
            #
            #   +3 = good for White
            #   -3 = good for Black
            #
            # Therefore:
            #
            # White move:
            #   current - previous
            #
            # Black move:
            #   previous - current
            # --------------------------------------------------

            if mover == chess.WHITE:
                eval_change = current_eval - prev_eval
            else:
                eval_change = prev_eval - current_eval

            # --------------------------------------------------
            # Only negative change means the player lost
            # evaluation.
            #
            # Example:
            #
            # White:
            # +2 → +3
            # change = +1
            # Good move
            #
            # White:
            # +3 → +1
            # change = -2
            # Mistake
            #
            # Black:
            # +2 → +3
            # change = -1
            # Bad for Black
            # --------------------------------------------------

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
            "evaluation": current_eval,
            "best_move": eval_result["best_move"],
            "pv": eval_result["pv"],
            "candidates": eval_result["candidates"],
            "quality": quality,
            "move": move.uci(),
            "reason": reason_data["reason"],
            "confidence": reason_data["confidence"],
            "explanation": coach["explanation"],
            "recommendation": coach["recommendation"]
        })

        # Current position becomes the previous position
        # for the next move.
        prev_eval = current_eval

    print(
        f"Finished analysis. Moves analyzed: {len(evaluations)}"
    )

    return {
        "evaluations": evaluations
    }