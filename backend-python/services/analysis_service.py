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
    prev_eval = 0

    for move in game.mainline_moves():
        before = board.copy() # Position before the move
        board.push(move)  # Play move
        after = board.copy() # Position after move
        eval_result = evaluate_position(after)  # Evaluate position
        # eval_result = evaluate_position(board)
        current_eval = eval_result["evaluation"]

        # Detect why the position changed
        reason_data = detect_reason(
            before,
            after,
            prev_eval,
            current_eval
        )

        # Generate coaching text
        coach = generate_explanation(
            reason_data,
            move.uci(),
            eval_result["best_move"]
        )

        # MOVE QUALITY
        diff = abs(current_eval - prev_eval)
        if diff < 0.3:
            quality = "best"
        elif diff < 0.7:
            quality = "good"
        elif diff < 1.5:
            quality = "inaccuracy"
        elif diff < 3:
            quality = "mistake"
        else:
            quality = "blunder"

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
        
        prev_eval = current_eval
    print(f"Finished analysis. Moves analyzed: {len(evaluations)}")
    return {
        "evaluations": evaluations
    }