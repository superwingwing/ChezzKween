import chess
import chess.engine

STOCKFISH_PATH = "engine/stockfish.exe"

# One engine for the whole application
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)


def score_to_eval(score):
    score = score.white()
    if score.is_mate():
        mate = score.mate()
        return 100 if mate > 0 else -100
    return round(score.score() / 100, 2)


def evaluate_position(board):
    infos = engine.analyse(
        board,
        chess.engine.Limit(depth=18),
        multipv=3
    )
     
    print("\n==============================")
    print("FEN:", board.fen())
    print("Stockfish returned:")
    print(infos)
    print("==============================\n")

    if isinstance(infos, dict):
        infos = [infos]
    candidates = []
    for info in infos:
        if "score" not in info:
            continue
        evaluation = score_to_eval(info["score"])
        pv = []
        if "pv" in info:
            pv = [move.uci() for move in info["pv"]]
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