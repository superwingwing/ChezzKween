import chess


def explain(details, played_move, best_move, pv, before, after):

    issue = details.get("issue")

    # ==========================================
    # CENTER CONTROL
    # ==========================================

    if issue == "center":

        return {
            "explanation":
                f"{played_move} improved control of the center.",

            "recommendation":
                "Continue occupying central squares and coordinate your pieces."
        }

    # ==========================================
    # SPACE
    # ==========================================

    if issue == "space":

        return {
            "explanation":
                f"{played_move} increased your space advantage.",

            "recommendation":
                "Use the extra space to improve piece activity."
        }

    # ==========================================
    # OPEN FILE
    # ==========================================

    if issue == "open_file":

        return {
            "explanation":
                f"{played_move} opened an important file.",

            "recommendation":
                "Place a rook on the open file to maximize pressure."
        }

    # ==========================================
    # POSITION CHANGE USING BEFORE / AFTER
    # ==========================================

    if before is not None and after is not None:

        # Detect check created by the played move
        if after.is_check():

            return {
                "explanation":
                    f"{played_move} gives check and forces the opponent "
                    f"to respond to the king threat.",

                "recommendation":
                    f"Look for the strongest continuation after the check. "
                    f"The engine recommends {best_move}."
            }

        # Detect whether the position contains a promotion
        if pv:

            for uci in pv:

                try:
                    move = chess.Move.from_uci(uci)

                    if move.promotion:
                        return {
                            "explanation":
                                f"{played_move} creates a strong pawn "
                                f"promotion threat in the engine's continuation.",

                            "recommendation":
                                f"Follow the engine continuation beginning "
                                f"with {best_move} to maintain the promotion threat."
                        }

                except ValueError:
                    continue

    # ==========================================
    # NO SPECIFIC BOARD EXPLANATION
    # ==========================================

    return None