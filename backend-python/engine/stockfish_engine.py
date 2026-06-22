import chess
import chess.engine

STOCKFISH_PATH = "engine/stockfish.exe"

engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)


def evaluate_position(fen: str):
    board = chess.Board(fen)

    info = engine.analyse(
        board,
        chess.engine.Limit(time=0.5)
    )

    # ✅ ALWAYS from White perspective
    score = info["score"].white()

    if score.is_mate():
        return {
            "type": "mate",
            "value": score.mate()
        }
    else:
        return {
            "type": "cp",
            "value": score.score() / 100  # ✅ convert to pawn units
        }