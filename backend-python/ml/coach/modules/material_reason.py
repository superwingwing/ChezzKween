import chess

from ml.analysis.material import (
    analyze_material,
    material_count,
    material_balance,
)


PIECE_NAMES = {
    chess.PAWN: "pawn",
    chess.KNIGHT: "knight",
    chess.BISHOP: "bishop",
    chess.ROOK: "rook",
    chess.QUEEN: "queen",
    chess.KING: "king",
}

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}


def get_removed_pieces(
    before: chess.Board,
    after: chess.Board
):
    """
    Find pieces that disappeared between the two positions.

    This gives us concrete material information for the
    coaching explanation.
    """

    removed = []

    for square in chess.SQUARES:

        before_piece = before.piece_at(square)
        after_piece = after.piece_at(square)

        # A piece existed before but no longer exists
        if before_piece is not None and after_piece is None:

            # Never treat the king as captured
            if before_piece.piece_type == chess.KING:
                continue

            removed.append({
                "color": (
                    "white"
                    if before_piece.color == chess.WHITE
                    else "black"
                ),

                "piece": PIECE_NAMES[
                    before_piece.piece_type
                ],

                "piece_type": before_piece.piece_type,

                "square": chess.square_name(square),

                "value": PIECE_VALUES[
                    before_piece.piece_type
                ],
            })

    return removed


def detect_material_reason(
    before: chess.Board,
    after: chess.Board
):

    # ==========================================================
    # EXISTING MATERIAL ANALYSIS
    # ==========================================================

    material = analyze_material(
        before,
        after
    )

    reasons = []

    # ==========================================================
    # CONCRETE PIECES THAT DISAPPEARED
    # ==========================================================

    removed_pieces = get_removed_pieces(
        before,
        after
    )

    # Separate white and black losses
    white_removed = [
        piece
        for piece in removed_pieces
        if piece["color"] == "white"
    ]

    black_removed = [
        piece
        for piece in removed_pieces
        if piece["color"] == "black"
    ]

    # ==========================================================
    # WHITE GAINED MATERIAL
    # ==========================================================

    if material["white_change"] > 0:

        details = {
            "side": "white",
            "change": material["white_change"],

            "material_before": material["white_before"],
            "material_after": material["white_after"],

            "balance_before": material["balance_before"],
            "balance_after": material["balance_after"],

            "advantage": "white_gained_material",

            "lost_pieces": black_removed,
        }

        reasons.append({
            "reason": "material_gain",
            "confidence": 95,
            "details": details
        })

    # ==========================================================
    # WHITE LOST MATERIAL
    # ==========================================================

    elif material["white_change"] < 0:

        details = {
            "side": "white",
            "change": abs(material["white_change"]),

            "material_before": material["white_before"],
            "material_after": material["white_after"],

            "balance_before": material["balance_before"],
            "balance_after": material["balance_after"],

            "advantage": "white_lost_material",

            "lost_pieces": white_removed,
        }

        reasons.append({
            "reason": "material_loss",
            "confidence": 95,
            "details": details
        })

    # ==========================================================
    # BLACK GAINED MATERIAL
    # ==========================================================

    if material["black_change"] > 0:

        details = {
            "side": "black",
            "change": material["black_change"],

            "material_before": material["black_before"],
            "material_after": material["black_after"],

            "balance_before": material["balance_before"],
            "balance_after": material["balance_after"],

            "advantage": "black_gained_material",

            "lost_pieces": white_removed,
        }

        reasons.append({
            "reason": "material_gain",
            "confidence": 95,
            "details": details
        })

    # ==========================================================
    # BLACK LOST MATERIAL
    # ==========================================================

    elif material["black_change"] < 0:

        details = {
            "side": "black",
            "change": abs(material["black_change"]),

            "material_before": material["black_before"],
            "material_after": material["black_after"],

            "balance_before": material["balance_before"],
            "balance_after": material["balance_after"],

            "advantage": "black_lost_material",

            "lost_pieces": black_removed,
        }

        reasons.append({
            "reason": "material_loss",
            "confidence": 95,
            "details": details
        })

    # ==========================================================
    # MATERIAL BALANCE IMPROVED
    # ==========================================================

    balance_change = (
        material["balance_after"]
        -
        material["balance_before"]
    )

    if balance_change > 0:

        reasons.append({
            "reason": "material_advantage",
            "confidence": 90,
            "details": {
                "side": "white",
                "change": balance_change,

                "balance_before":
                    material["balance_before"],

                "balance_after":
                    material["balance_after"],

                "advantage":
                    "white_material_advantage"
            }
        })

    elif balance_change < 0:

        reasons.append({
            "reason": "material_advantage",
            "confidence": 90,
            "details": {
                "side": "black",
                "change": abs(balance_change),

                "balance_before":
                    material["balance_before"],

                "balance_after":
                    material["balance_after"],

                "advantage":
                    "black_material_advantage"
            }
        })

    # ==========================================================
    # NOTHING CHANGED
    # ==========================================================

    if not reasons:
        return None

    # ==========================================================
    # STRONGEST REASON
    # ==========================================================

    reasons.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    result = reasons[0]

    # Debugging
    print(
        "MATERIAL REASON:",
        result
    )

    return result