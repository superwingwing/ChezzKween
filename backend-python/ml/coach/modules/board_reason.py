import chess

from ml.analysis.board import (
    center_control,
    extended_center_control,
    space_advantage,
    open_files_to_king,
    rook_on_open_file,
    queen_on_open_file
)


def detect_board_reason(
    before: chess.Board,
    after: chess.Board
):

    reasons = []

    for color in (chess.WHITE, chess.BLACK):

        side = "white" if color == chess.WHITE else "black"
        opponent = not color

        # ======================================================
        # CENTER CONTROL
        # ======================================================

        before_center = center_control(
            before,
            color
        )

        after_center = center_control(
            after,
            color
        )

        center_change = after_center - before_center

        if center_change > 0:

            reasons.append({
                "reason": "board_center_control",
                "confidence": 82,

                "details": {
                    "side": side,

                    "change": center_change,

                    "before": before_center,
                    "after": after_center,

                    "advantage":
                        "increased_center_control",

                    "meaning":
                        "controls_more_central_squares"
                }
            })

        # ======================================================
        # EXTENDED CENTER
        # ======================================================

        before_extended = extended_center_control(
            before,
            color
        )

        after_extended = extended_center_control(
            after,
            color
        )

        extended_change = (
            after_extended
            -
            before_extended
        )

        if extended_change > 0:

            reasons.append({
                "reason": "board_extended_center",
                "confidence": 78,

                "details": {
                    "side": side,

                    "change": extended_change,

                    "before": before_extended,
                    "after": after_extended,

                    "advantage":
                        "increased_extended_center_control",

                    "meaning":
                        "controls_more_space_around_center"
                }
            })

        # ======================================================
        # SPACE
        # ======================================================

        before_space = space_advantage(
            before,
            color
        )

        after_space = space_advantage(
            after,
            color
        )

        space_change = (
            after_space
            -
            before_space
        )

        if space_change > 0:

            reasons.append({
                "reason": "board_space_advantage",
                "confidence": 80,

                "details": {
                    "side": side,

                    "change": space_change,

                    "before": before_space,
                    "after": after_space,

                    "advantage":
                        "increased_space",

                    "meaning":
                        "pieces_have_more_room_to_operate"
                }
            })

        # ======================================================
        # OPEN FILE TOWARD ENEMY KING
        # ======================================================

        before_open = open_files_to_king(
            before,
            opponent
        )

        after_open = open_files_to_king(
            after,
            opponent
        )

        open_change = (
            after_open
            -
            before_open
        )

        if open_change > 0:

            reasons.append({
                "reason": "board_opened_king_file",
                "confidence": 85,

                "details": {
                    "side": side,

                    "change": open_change,

                    "before": before_open,
                    "after": after_open,

                    "advantage":
                        "opened_file_toward_enemy_king",

                    "target":
                        "enemy_king",

                    "meaning":
                        "created_more_direct_access_to_enemy_king"
                }
            })

        # ======================================================
        # ROOK ON OPEN FILE
        # ======================================================

        before_rook = rook_on_open_file(
            before,
            color
        )

        after_rook = rook_on_open_file(
            after,
            color
        )

        rook_change = (
            after_rook
            -
            before_rook
        )

        if rook_change > 0:

            reasons.append({
                "reason": "board_rook_on_open_file",
                "confidence": 84,

                "details": {
                    "side": side,

                    "change": rook_change,

                    "before": before_rook,
                    "after": after_rook,

                    "advantage":
                        "rook_activity",

                    "meaning":
                        "rook_gained_access_to_open_file"
                }
            })

        # ======================================================
        # QUEEN ON OPEN FILE
        # ======================================================

        before_queen = queen_on_open_file(
            before,
            color
        )

        after_queen = queen_on_open_file(
            after,
            color
        )

        queen_change = (
            after_queen
            -
            before_queen
        )

        if queen_change > 0:

            reasons.append({
                "reason": "board_queen_on_open_file",
                "confidence": 76,

                "details": {
                    "side": side,

                    "change": queen_change,

                    "before": before_queen,
                    "after": after_queen,

                    "advantage":
                        "queen_activity",

                    "meaning":
                        "queen_gained_access_to_open_file"
                }
            })

    # ==========================================================
    # NO BOARD REASON
    # ==========================================================

    if not reasons:
        return None

    # ==========================================================
    # STRONGEST BOARD ADVANTAGE
    # ==========================================================

    reasons.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    result = reasons[0]

    print(
        "BOARD REASON:",
        result
    )

    return result