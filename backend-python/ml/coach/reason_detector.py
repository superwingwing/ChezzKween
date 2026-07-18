import chess

from ml.coach.modules.material_reason import detect_material_reason
from ml.coach.modules.king_reason import detect_king_reason
from ml.coach.modules.pawn_reason import detect_pawn_reason
from ml.coach.modules.board_reason import detect_board_reason
from ml.coach.modules.piece_reason import detect_piece_reason
from ml.coach.modules.tactical_reason import detect_tactical_reason


def detect_reason(before, after, evaluation_before, evaluation_after):
    reasons = []

    material = detect_material_reason(before, after)
    if material:
        reasons.append(material)

    king = detect_king_reason(before, after)
    if king:
        reasons.append(king)

    pawn = detect_pawn_reason(before, after)
    if pawn:
        reasons.append(pawn)

    board = detect_board_reason(before, after)
    if board:
        reasons.append(board)

    piece = detect_piece_reason(before, after)
    if piece:
        reasons.append(piece)

    tactical = detect_tactical_reason(before, after)
    if tactical:
        reasons.append(tactical)

    # No specific reason detected
    if not reasons:
        result = {
            "reason": "position_change",
            "confidence": 40,
            "details": {
                "evaluation_change": round(
                    evaluation_after - evaluation_before,
                    2
                )
            }
        }

        print("DETECTED REASON:", result)
        return result

    # Return strongest detected reason
    reasons.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    print("DETECTED REASON:", reasons[0])
    return reasons[0]