def explain(details, played_move, best_move):

    side = details.get("side", "your")

    return {

        "explanation":
            f"{played_move} weakened the {side} king's safety and increased attacking chances.",

        "recommendation":
            "Improve king safety by castling, defending key squares, and reducing attacking lines."
    }