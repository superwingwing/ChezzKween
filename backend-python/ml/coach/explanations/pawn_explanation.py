def explain(details, played_move, best_move):

    issue = details.get("issue")

    if issue == "isolated":

        return {
            "explanation":
                f"{played_move} created an isolated pawn.",

            "recommendation":
                "Try to support the isolated pawn or avoid creating isolated pawn structures."
        }

    if issue == "doubled":

        return {
            "explanation":
                f"{played_move} created doubled pawns.",

            "recommendation":
                "Avoid unnecessary pawn weaknesses unless compensated by activity."
        }

    if issue == "passed":

        return {
            "explanation":
                f"{played_move} created a passed pawn.",

            "recommendation":
                "Advance the passed pawn while supporting it with your pieces."
        }

    if issue == "chain":

        return {
            "explanation":
                f"{played_move} improved the pawn chain.",

            "recommendation":
                "Maintain the pawn chain and use it to support central control."
        }

    return None