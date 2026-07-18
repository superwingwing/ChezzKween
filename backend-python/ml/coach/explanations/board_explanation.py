def explain(details, played_move, best_move):

    issue = details.get("issue")

    if issue == "center":

        return {
            "explanation":
                f"{played_move} improved control of the center.",

            "recommendation":
                "Continue occupying central squares and coordinate your pieces."
        }

    if issue == "space":

        return {
            "explanation":
                f"{played_move} increased your space advantage.",

            "recommendation":
                "Use the extra space to improve piece activity."
        }

    if issue == "open_file":

        return {
            "explanation":
                f"{played_move} opened an important file.",

            "recommendation":
                "Place a rook on the open file to maximize pressure."
        }

    return None