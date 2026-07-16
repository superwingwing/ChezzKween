import chess
import chess.engine

STOCKFISH_PATH = "engine/stockfish.exe"

engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)


def score_to_eval(score):

    score = score.white()

    if score.is_mate():

        mate = score.mate()

        return {
            "evaluation": 100 if mate > 0 else -100,
            "mate": mate
        }

    return {
        "evaluation": round(score.score() / 100, 2),
        "mate": None
    }


def evaluate_position(

    board,

    depth=18,

    multipv=3

):

    infos = engine.analyse(

        board,

        chess.engine.Limit(depth=depth),

        multipv=multipv

    )

    candidates = []

    for info in infos:

        score = score_to_eval(
            info["score"]
        )

        pv = []

        if "pv" in info:

            pv = [

                move.uci()

                for move in info["pv"]

            ]

        candidates.append({

            "evaluation":
                score["evaluation"],

            "mate":
                score["mate"],

            "best_move":
                pv[0] if len(pv) else None,

            "pv":
                pv

        })

    return {

        "evaluation":
            candidates[0]["evaluation"],

        "best_move":
            candidates[0]["best_move"],

        "pv":
            candidates[0]["pv"],

        "mate":
            candidates[0]["mate"],

        "candidates":
            candidates

    }