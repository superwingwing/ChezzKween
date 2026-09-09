from ml.coach.explanations.material_explanation import explain as material
from ml.coach.explanations.king_explanation import explain as king
from ml.coach.explanations.pawn_explanation import explain as pawn
from ml.coach.explanations.board_explanation import explain as board
from ml.coach.explanations.piece_explanation import explain as piece
from ml.coach.explanations.tactical_explanation import explain as tactical
from ml.coach.explanations.default_explanation import explain as default


def generate_explanation(
    reason_data,
    played_move,
    best_move,
    pv,
    before,
    after
):

    reason = reason_data["reason"]
    details = reason_data["details"]

    result = None

    # ==========================================================
    # CHECKMATE HAS ABSOLUTE PRIORITY
    # ==========================================================

    if after is not None and after.is_checkmate():

        return {
            "explanation":
                (
                    f"{played_move} is checkmate! "
                    f"The move leaves the opponent's king "
                    f"with no legal escape."
                ),

            "recommendation":
                (
                    "No further move is required — "
                    "the position is already checkmate."
                )
        }

    # ==========================================================
    # MATERIAL
    # ==========================================================

    if reason in ("material_gain", "material_loss"):

        result = material(
            details,
            played_move,
            best_move,
            pv,
            before,
            after
        )

    # ==========================================================
    # KING SAFETY
    # ==========================================================

    elif reason.startswith("king_safety"):

        result = king(
            details,
            played_move,
            best_move,
            pv,
            before,
            after
        )

    # ==========================================================
    # PAWN
    # ==========================================================

    elif reason.startswith("pawn_"):

        result = pawn(
            details,
            played_move,
            best_move,
            pv,
            before,
            after
        )

    # ==========================================================
    # BOARD
    # ==========================================================

    elif reason.startswith("board_"):

        result = board(
            details,
            played_move,
            best_move,
            pv,
            before,
            after
        )

    # ==========================================================
    # PIECE
    # ==========================================================

    elif reason.startswith("piece_"):

        result = piece(
            details,
            played_move,
            best_move,
            pv,
            before,
            after
        )

    # ==========================================================
    # TACTICAL
    # ==========================================================

    elif reason.startswith("tactical_"):

        result = tactical(
            details,
            played_move,
            best_move,
            pv,
            before,
            after
        )

    # ==========================================================
    # DEFAULT
    # ==========================================================

    else:

        result = default(
            details,
            played_move,
            best_move,
            pv,
            before,
            after
        )

    # ==========================================================
    # FALLBACK
    # ==========================================================

    if result is None:

        if best_move:

            return {
                "explanation":
                    (
                        f"{played_move} does not have a specific "
                        f"explanation from the detected reason."
                    ),

                "recommendation":
                    f"Stockfish recommends {best_move} instead."
            }

        return {
            "explanation":
                (
                    f"{played_move} does not have a specific "
                    f"explanation from the detected reason."
                ),

            "recommendation":
                (
                    "There is no stronger continuation because "
                    "the position has no legal continuation."
                )
        }

    return result