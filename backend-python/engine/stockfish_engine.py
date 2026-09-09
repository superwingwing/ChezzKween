import chess
import chess.engine

STOCKFISH_PATH = "engine/stockfish.exe"

# One engine for the whole application
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)


def score_to_eval(score, board):
    """
    Convert Stockfish's PovScore into a consistent evaluation
    from White's perspective.

    Positive = White is winning
    Negative = Black is winning

    Special handling is required for mate because after a
    checkmate the side to move is the side that has been mated.
    """

    score = score.white()

    if score.is_mate():
        mate = score.mate()

        # If the side to move is checkmated, the winner is the
        # opposite side.
        #
        # Example:
        # White plays Bc5#
        # board.turn == BLACK
        # Black is checkmated
        # Therefore White has won -> +100
        #
        # Example:
        # Black plays ...Qh2#
        # board.turn == WHITE
        # White is checkmated
        # Therefore Black has won -> -100

        if board.is_checkmate():
            if board.turn == chess.BLACK:
                return 100
            else:
                return -100

        # For non-checkmate mate scores, use the normal
        # White-perspective mate sign.
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