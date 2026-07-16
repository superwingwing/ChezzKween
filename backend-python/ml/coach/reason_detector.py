import chess

from ml.analysis.material import material_balance
from ml.analysis.king import (
    king_safety,
    attack_pressure
)


# ==========================================
# Material Reason
# ==========================================

def check_material_change(
    before,
    after
):

    before_balance = material_balance(before)

    after_balance = material_balance(after)

    change = after_balance - before_balance


    # Large material swing
    if abs(change) >= 3:

        if change > 0:

            return {
                "reason": "material_gain",
                "confidence": 95,
                "details": {
                    "change": change
                }
            }

        else:

            return {
                "reason": "material_loss",
                "confidence": 95,
                "details": {
                    "change": change
                }
            }


    return None



# ==========================================
# King Safety Reason
# ==========================================

def check_king_safety(
    before,
    after
):

    white_before = king_safety(
        before,
        chess.WHITE
    )

    white_after = king_safety(
        after,
        chess.WHITE
    )


    black_before = king_safety(
        before,
        chess.BLACK
    )

    black_after = king_safety(
        after,
        chess.BLACK
    )


    white_change = (
        white_after -
        white_before
    )

    black_change = (
        black_after -
        black_before
    )


    if white_change <= -2:

        return {
            "reason": "king_safety",
            "confidence": 80,
            "details": {
                "side": "white",
                "change": white_change
            }
        }


    if black_change <= -2:

        return {
            "reason": "king_safety",
            "confidence": 80,
            "details": {
                "side": "black",
                "change": black_change
            }
        }


    return None



# ==========================================
# Main Detector
# ==========================================

def detect_reason(
    before,
    after,
    evaluation_before,
    evaluation_after
):

    reasons = []


    material = check_material_change(
        before,
        after
    )

    if material:
        reasons.append(material)



    king = check_king_safety(
        before,
        after
    )

    if king:
        reasons.append(king)



    # No specific reason found

    if not reasons:

        return {

            "reason": "position_change",

            "confidence": 40,

            "details": {

                "evaluation_change":
                    round(
                        evaluation_after -
                        evaluation_before,
                        2
                    )

            }

        }



    # choose strongest reason

    reasons.sort(
        key=lambda x:
        x["confidence"],
        reverse=True
    )


    return reasons[0]