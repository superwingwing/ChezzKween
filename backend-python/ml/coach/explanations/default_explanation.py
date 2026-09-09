def explain(details, played_move, best_move, pv, before, after):

    return {

        "explanation":
            f"{played_move} changed the evaluation of the position.",

        "recommendation":
            f"Consider the stronger continuation {best_move}."
    }