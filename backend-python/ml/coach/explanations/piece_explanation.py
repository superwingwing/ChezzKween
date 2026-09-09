import chess


def explain(details, played_move, best_move, pv, before, after):

    issue = details.get("issue")

    # ==========================================
    # PIECE ACTIVITY
    # ==========================================

    if issue == "activity":

        return {
            "explanation":
                f"{played_move} improved the activity of your pieces "
                f"by giving them more useful squares and lines.",

            "recommendation":
                f"Keep your active pieces coordinated and avoid exchanging "
                f"them unnecessarily. Consider {best_move} if further improvement is possible."
        }

    # ==========================================
    # PIECE COORDINATION
    # ==========================================

    if issue == "coordination":

        return {
            "explanation":
                f"{played_move} improved coordination between your pieces, "
                f"allowing them to support each other more effectively.",

            "recommendation":
                "Continue developing harmoniously and avoid leaving pieces "
                "disconnected or undefended."
        }

    # ==========================================
    # OUTPOST
    # ==========================================

    if issue == "outpost":

        return {
            "explanation":
                f"{played_move} established a strong outpost that can be "
                f"used as a stable square for your pieces.",

            "recommendation":
                "Support the outpost and use it as a base for improving "
                "piece activity or launching an attack."
        }

    # ==========================================
    # VERIFY POSITION CHANGE
    # ==========================================

    if before is not None and after is not None:

        # Compare piece placement before and after the move.
        before_board = before.board_fen()
        after_board = after.board_fen()

        if before_board != after_board:

            return {
                "explanation":
                    f"{played_move} changed the piece placement and "
                    f"affected the activity of the position.",

                "recommendation":
                    f"Evaluate the new piece placement carefully. "
                    f"The engine's stronger continuation is {best_move}."
            }

    return None