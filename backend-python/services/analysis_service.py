import chess.pgn
import io
from engine.stockfish_engine import evaluate_position


def analyze_pgn(pgn_text: str):
    game = chess.pgn.read_game(io.StringIO(pgn_text))
    board = game.board()

    evaluations = []

    for move in game.mainline_moves():
        board.push(move)

        eval_result = evaluate_position(board.fen())

        evaluations.append({
            "fen": board.fen(),
            "evaluation": eval_result
        })

    return {
        "evaluations": evaluations
    }