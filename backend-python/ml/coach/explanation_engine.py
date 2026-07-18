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

    if reason in ("material_gain", "material_loss"):
        return material(details, played_move, best_move)

    if reason == "king_safety":
        return king(details, played_move, best_move)

    if reason.startswith("pawn_"):
        return pawn(details, played_move, best_move)

    if reason.startswith("board_"):
        return board(details, played_move, best_move)

    if reason.startswith("piece_"):
        return piece(details, played_move, best_move)

    if reason.startswith("tactical_"):
        return tactical(details, played_move, best_move)

    return default(details, played_move, best_move)