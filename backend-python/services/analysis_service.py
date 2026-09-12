import chess
import chess.pgn
import io
from engine.stockfish_engine import evaluate_position
from ml.coach.move_explanation import explain_move

def analyze_single_move(
    before,
    move,
    prev_eval=None
):
    """
    Analyze a single chess move.

    Parameters:
        before:
            chess.Board representing the position before the move.

        move:
            chess.Move object.

        prev_eval:
            Stockfish evaluation before the move.
            Optional. If not supplied, Stockfish evaluates
            the position before the move.

    Returns:
        Dictionary containing:
            - FEN
            - evaluation
            - best move
            - PV
            - candidates
            - move SAN
            - quality
            - explanation
            - recommendation
    """

    # ==========================================================
    # VALIDATE MOVE
    # ==========================================================

    if move not in before.legal_moves:
        return {
            "error": "Illegal move"
        }

    # ==========================================================
    # POSITION BEFORE MOVE
    # ==========================================================

    mover = before.turn

    # Convert UCI -> professional SAN
    #
    # Example:
    # d2d4 -> d4
    # g1f3 -> Nf3
    # f1c4 -> Bc4
    # e1g1 -> O-O
    # c7c8q -> c8=Q
    #
    san_move = before.san(move)

    # ==========================================================
    # STOCKFISH EVALUATION BEFORE MOVE
    # ==========================================================
    #
    # PGN analysis already has prev_eval, so we reuse it.
    #
    # Manual exploration does not have prev_eval, so evaluate
    # the current position here.
    #
    # ==========================================================

    if prev_eval is None:

        before_eval_result = evaluate_position(before)

        prev_eval = before_eval_result["evaluation"]

    # ==========================================================
    # PLAY THE MOVE
    # ==========================================================

    after = before.copy()

    after.push(move)

    # ==========================================================
    # STOCKFISH EVALUATION AFTER MOVE
    # ==========================================================

    eval_result = evaluate_position(after)

    current_eval = eval_result["evaluation"]

    # ==========================================================
    # MOVE EXPLANATION
    # ==========================================================
    #
    # The explanation system receives:
    #
    # - position before
    # - position after
    # - actual move
    # - SAN move
    # - Stockfish best move
    # - Stockfish PV
    # - evaluation before
    # - evaluation after
    #
    # ==========================================================

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

    # ==========================================================
    # MOVE QUALITY
    # ==========================================================

    # Checkmate is always the best move.
    if after.is_checkmate():

        quality = "best"

    else:

        # ------------------------------------------------------
        # Calculate evaluation change from the mover's
        # perspective.
        # ------------------------------------------------------

        if mover == chess.WHITE:

            eval_change = current_eval - prev_eval

        else:

            eval_change = prev_eval - current_eval

        # ------------------------------------------------------
        # Only a negative change means the player lost
        # evaluation.
        # ------------------------------------------------------

        centipawn_loss = max(0, -eval_change)

        # ------------------------------------------------------
        # Classify move
        # ------------------------------------------------------

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

    # ==========================================================
    # RETURN ANALYSIS
    # ==========================================================

    return {
        "fen": after.fen(),

        # ------------------------------------------------------
        # Stockfish evaluation
        # ------------------------------------------------------

        "evaluation": current_eval,
        "best_move": eval_result["best_move"],
        "pv": eval_result["pv"],
        "candidates": eval_result["candidates"],
        # Move quality

        "quality": quality,
        # Actual played move in SAN
        "move": san_move,

        # Coaching
        "explanation": coach["explanation"],
        "recommendation": coach["recommendation"]
    }


# ==============================================================
# ANALYZE UPLOADED PGN
# ==============================================================

def analyze_pgn(pgn_text: str):

    # READ PGN
    game = chess.pgn.read_game(
        io.StringIO(pgn_text)
    )
    # INVALID PGN
    if game is None:
        return {
            "error": "Invalid PGN"
        }

    board = game.board()
    evaluations = []

    initial_eval_result = evaluate_position(board)
    prev_eval = initial_eval_result["evaluation"]

    # ANALYZE EVERY PGN MOVE
    for move in game.mainline_moves():
        before = board.copy()
        # Analyze the move using the shared function
        result = analyze_single_move(
            before=before,
            move=move,
            prev_eval=prev_eval
        )
        # Check for analysis error
        if "error" in result:
            return result
        # Save result
        evaluations.append(result)
        # Move the PGN board forward
        board.push(move)
        prev_eval = result["evaluation"]
    print(
        f"Finished analysis. Moves analyzed: {len(evaluations)}"
    )
    return {
        "evaluations": evaluations
    }

def analyze_explored_move(
    fen: str,
    move_uci: str
):



    try:
        before = chess.Board(fen)
    except ValueError:
        return {
            "error": "Invalid FEN"
        }
    try:
        move = chess.Move.from_uci(move_uci)
    except ValueError:
        return {
            "error": "Invalid move"
        }
    # ==========================================================
    # ANALYZE USING THE SAME FUNCTION
    # ==========================================================
    return analyze_single_move(
        before=before,
        move=move
    )