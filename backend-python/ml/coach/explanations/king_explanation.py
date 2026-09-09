def explain(details, played_move, best_move, pv, before, after):

    side = details.get("side", "your")

    # Use the actual position after the move
    king_in_check = after.is_check()

    if king_in_check:
        return {
            "explanation":
                f"{played_move} puts the {side} king under immediate pressure.",

            "recommendation":
                f"Find the strongest defensive response. The engine recommends {best_move}."
        }

    # Use the engine PV when available to determine whether the attack
    # continues through the recommended line.
    if pv:
        return {
            "explanation":
                f"{played_move} changed the king's safety and gives the opponent "
                f"attacking opportunities in the position.",

            "recommendation":
                f"Prioritize king safety and consider the stronger continuation {best_move}."
        }

    return {
        "explanation":
            f"{played_move} weakened the {side} king's safety and increased attacking chances.",

        "recommendation":
            f"Improve king safety and consider the stronger move {best_move}."
    }