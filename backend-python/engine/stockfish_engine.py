import chess
import chess.engine

STOCKFISH_PATH = "engine/stockfish.exe"

engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)


def evaluate_position(board: chess.Board):
    info = engine.analyse(
        board,
        chess.engine.Limit(time=0.3)
    )

    score = info["score"].white()

    # ✅ numeric eval
    if score.is_mate():
        eval_value = 100 if score.mate() > 0 else -100
    else:
        eval_value = score.score() / 100

    # ✅ best move (for arrows)
    best_move = None
    if "pv" in info and len(info["pv"]) > 0:
        best_move = info["pv"][0].uci()

    return {
        "evaluation": eval_value,   # 🔥 NUMBER ONLY
        "best_move": best_move
    }