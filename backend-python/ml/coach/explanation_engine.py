from ml.coach.explanations.material_explanation import explain as material
from ml.coach.explanations.king_explanation import explain as king
from ml.coach.explanations.pawn_explanation import explain as pawn
from ml.coach.explanations.board_explanation import explain as board
from ml.coach.explanations.piece_explanation import explain as piece
from ml.coach.explanations.tactical_explanation import explain as tactical
from ml.coach.explanations.default_explanation import explain as default


def generate_explanation(reason_data, played_move, best_move):

    reason = reason_data["reason"]
    details = reason_data["details"]

    result = None

    if reason in ("material_gain", "material_loss"):
        result = material(
            details,
            played_move,
            best_move
        )

    elif reason == "king_safety":
        result = king(
            details,
            played_move,
            best_move
        )

    elif reason.startswith("pawn_"):
        result = pawn(
            details,
            played_move,
            best_move
        )

    elif reason.startswith("board_"):
        result = board(
            details,
            played_move,
            best_move
        )

    elif reason.startswith("piece_"):
        result = piece(
            details,
            played_move,
            best_move
        )

    elif reason.startswith("tactical_"):
        result = tactical(
            details,
            played_move,
            best_move
        )

    else:
        result = default(
            details,
            played_move,
            best_move
        )


    # Safety fallback
    if result is None:
        return {
            "explanation":
                f"{played_move} changed the position.",

            "recommendation":
                f"Try {best_move} instead."
        }


    return result