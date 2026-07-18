def explain(details, played_move, best_move):

    issue = details.get("issue")

    if issue == "activity":

        return {

            "explanation":
                f"{played_move} improved piece activity.",

            "recommendation":
                "Keep your active pieces coordinated and avoid exchanging them unnecessarily."
        }

    if issue == "coordination":

        return {

            "explanation":
                f"{played_move} improved coordination between your pieces.",

            "recommendation":
                "Continue developing harmoniously and avoid leaving pieces disconnected."
        }

    if issue == "outpost":

        return {

            "explanation":
                f"{played_move} established a strong outpost.",

            "recommendation":
                "Support the outpost and use it as an attacking base."
        }

    return None