import chess

from ml.analysis.board import (
    center_control,
    extended_center_control,
    space_advantage,
    open_files_to_king,
    rook_on_open_file,
    queen_on_open_file
)


def detect_board_reason(before: chess.Board, after: chess.Board):

    reasons = []

    for color in (chess.WHITE, chess.BLACK):

        side = "white" if color == chess.WHITE else "black"

        # Center control
        before_center = center_control(before, color)
        after_center = center_control(after, color)

        if after_center > before_center:
            reasons.append({
                "reason": "center_control",
                "confidence": 82,
                "details": {
                    "side": side,
                    "change": after_center - before_center
                }
            })

        # Extended center
        before_extended = extended_center_control(before, color)
        after_extended = extended_center_control(after, color)

        if after_extended > before_extended:
            reasons.append({
                "reason": "extended_center_control",
                "confidence": 78,
                "details": {
                    "side": side,
                    "change": after_extended - before_extended
                }
            })

        # Space
        before_space = space_advantage(before, color)
        after_space = space_advantage(after, color)

        if after_space > before_space:
            reasons.append({
                "reason": "space_advantage",
                "confidence": 80,
                "details": {
                    "side": side,
                    "change": after_space - before_space
                }
            })

        # Open files toward enemy king
        before_open = open_files_to_king(before, not color)
        after_open = open_files_to_king(after, not color)

        if after_open > before_open:
            reasons.append({
                "reason": "opened_king_file",
                "confidence": 85,
                "details": {
                    "side": side
                }
            })

        # Rook on open file
        before_rook = rook_on_open_file(before, color)
        after_rook = rook_on_open_file(after, color)

        if after_rook > before_rook:
            reasons.append({
                "reason": "rook_on_open_file",
                "confidence": 84,
                "details": {
                    "side": side
                }
            })

        # Queen on open file
        before_queen = queen_on_open_file(before, color)
        after_queen = queen_on_open_file(after, color)

        if after_queen > before_queen:
            reasons.append({
                "reason": "queen_on_open_file",
                "confidence": 76,
                "details": {
                    "side": side
                }
            })

    if not reasons:
        return None

    reasons.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    return reasons[0]