def explain(details, played_move, best_move):

    issue = details.get("issue")

    if issue == "hanging":

        return {

            "explanation":
                f"{played_move} left a piece hanging.",

            "recommendation":
                "Always check whether every piece is defended before ending your turn."
        }

    if issue == "fork":

        return {

            "explanation":
                f"{played_move} allowed a tactical fork.",

            "recommendation":
                "Watch for forks and double attacks before committing your move."
        }

    if issue == "pin":

        return {

            "explanation":
                f"{played_move} created or allowed a pin.",

            "recommendation":
                "Evaluate whether pinned pieces can safely move."
        }

    return None