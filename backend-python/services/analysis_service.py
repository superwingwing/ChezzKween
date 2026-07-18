import chess.pgn
import io
from engine.stockfish_engine import evaluate_position


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
        board.push(move)
        eval_result = evaluate_position(board)
        current_eval = eval_result["evaluation"]

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
            "move": move.uci()
        })
        prev_eval = current_eval
    print(f"Finished analysis. Moves analyzed: {len(evaluations)}")
    return {
        "evaluations": evaluations
    }