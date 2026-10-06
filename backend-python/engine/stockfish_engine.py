import chess
import os
import chess.engine

STOCKFISH_PATH = os.getenv(
    "STOCKFISH_PATH",
    "engine/stockfish"
    if os.name != "nt"
    else "engine/stockfish.exe"
)

engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)


def score_to_eval(score, board):
    score = score.white()

    if score.is_mate():
        mate = score.mate()

        if board.is_checkmate():
            if board.turn == chess.BLACK:
                return 100
            return -100

        return 100 if mate > 0 else -100

    return round(score.score() / 100, 2)


def evaluate_position(board, depth=12, multipv=1):
    infos = engine.analyse(
        board,
        chess.engine.Limit(depth=depth),
        multipv=multipv
    )

    if isinstance(infos, dict):
        infos = [infos]

    candidates = []

    for info in infos:
        if "score" not in info:
            continue

        evaluation = score_to_eval(
            info["score"],
            board
        )

        pv = []

        if "pv" in info:
            pv = [
                move.uci()
                for move in info["pv"]
            ]

        candidates.append({
            "evaluation": evaluation,
            "best_move": pv[0] if pv else None,
            "pv": pv
        })

    if not candidates:
        raise Exception("Stockfish returned no analysis.")

    return {
        "evaluation": candidates[0]["evaluation"],
        "best_move": candidates[0]["best_move"],
        "pv": candidates[0]["pv"],
        "candidates": candidates
    }


def evaluate_fast(board):
    return evaluate_position(
        board,
        depth=12,
        multipv=1
    )


def evaluate_critical(board):
    return evaluate_position(
        board,
        depth=16,
        multipv=3
    )


def evaluate_deep(board):
    return evaluate_position(
        board,
        depth=18,
        multipv=3
    )