import chess
import chess.engine

STOCKFISH_PATH = "engine/stockfish.exe"

engine = chess.engine.SimpleEngine.popen_uci(
    STOCKFISH_PATH
)


def evaluate_position(
    board: chess.Board,
    depth: int = 18
):

    info = engine.analyse(

        board,

        chess.engine.Limit(
            depth=depth
        )

    )

    score = info["score"].white()

    # ==========================================
    # Evaluation
    # ==========================================

    mate = None

    if score.is_mate():

        mate = score.mate()

        evaluation = (
            100
            if mate > 0
            else -100
        )

    else:

        evaluation = round(
            score.score() / 100,
            2
        )

    # ==========================================
    # Principal Variation
    # ==========================================

    pv = []

    if "pv" in info:

        pv = [

            move.uci()

            for move in info["pv"]

        ]

    # ==========================================
    # Best Move
    # ==========================================

    best_move = None

    if len(pv):

        best_move = pv[0]

    # ==========================================
    # Return Rich Analysis
    # ==========================================

    return {

        "evaluation": evaluation,

        "best_move": best_move,

        "pv": pv,

        "mate": mate,

        "depth": depth

    }