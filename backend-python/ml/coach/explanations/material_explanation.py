def explain(details, played_move, best_move):

    change = abs(details.get("change", 0))

    if details.get("change", 0) < 0:

        return {
            "explanation":
                f"{played_move} lost approximately {change} points of material, giving your opponent a significant advantage.",

            "recommendation":
                f"Before playing this move, look for tactical threats. A stronger continuation was {best_move}."
        }

    return {
        "explanation":
            f"{played_move} gained approximately {change} points of material.",

        "recommendation":
            "After winning material, simplify the position and avoid unnecessary complications."
    }