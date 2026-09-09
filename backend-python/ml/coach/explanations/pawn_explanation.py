import chess


def explain(details, played_move, best_move, pv, before, after):

    issue = details.get("issue")

    # ==========================================
    # ISOLATED PAWN
    # ==========================================

    if issue == "isolated":

        return {
            "explanation":
                f"{played_move} created an isolated pawn, leaving it without "
                f"support from neighboring pawns.",

            "recommendation":
                f"Support the isolated pawn with your pieces or consider "
                f"the stronger continuation {best_move}."
        }

    # ==========================================
    # DOUBLED PAWNS
    # ==========================================

    if issue == "doubled":

        return {
            "explanation":
                f"{played_move} created doubled pawns on the same file, "
                f"which can become a long-term structural weakness.",

            "recommendation":
                f"Avoid creating unnecessary pawn weaknesses unless you gain "
                f"something concrete. Consider {best_move}."
        }

    # ==========================================
    # PASSED PAWN
    # ==========================================

    if issue == "passed":

        return {
            "explanation":
                f"{played_move} created a passed pawn with no opposing pawn "
                f"on its file or adjacent files to stop its advance.",

            "recommendation":
                "Advance the passed pawn when safe and support it with your pieces."
        }

    # ==========================================
    # PAWN CHAIN
    # ==========================================

    if issue == "chain":

        return {
            "explanation":
                f"{played_move} strengthened the pawn structure by improving "
                f"the connection between your pawns.",

            "recommendation":
                "Maintain the pawn chain and use it to support your central pieces."
        }

    # ==========================================
    # POSITION COMPARISON
    # ==========================================

    if before is not None and after is not None:

        # Check whether the played move actually changed the pawn structure.
        before_pawns = {
            chess.WHITE: before.pieces(chess.PAWN, chess.WHITE),
            chess.BLACK: before.pieces(chess.PAWN, chess.BLACK)
        }

        after_pawns = {
            chess.WHITE: after.pieces(chess.PAWN, chess.WHITE),
            chess.BLACK: after.pieces(chess.PAWN, chess.BLACK)
        }

        if before_pawns != after_pawns:

            return {
                "explanation":
                    f"{played_move} changed the pawn structure of the position.",

                "recommendation":
                    f"Evaluate the resulting pawn weaknesses before continuing. "
                    f"The engine recommends {best_move}."
            }

    return None