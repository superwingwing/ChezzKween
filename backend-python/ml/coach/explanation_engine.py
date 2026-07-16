def generate_explanation(
    reason_data,
    played_move,
    best_move
):

    reason = reason_data["reason"]
    details = reason_data["details"]


    # ==================================
    # Material Loss
    # ==================================

    if reason == "material_loss":

        change = abs(
            details.get("change", 0)
        )

        return {

            "explanation":
                (
                    f"{played_move} lost approximately "
                    f"{change} points of material. "
                    "This gave your opponent a significant advantage."
                ),

            "recommendation":
                (
                    f"Before playing this move, check tactical threats. "
                    f"A stronger continuation was {best_move}."
                )
        }



    # ==================================
    # Material Gain
    # ==================================

    if reason == "material_gain":

        change = details.get(
            "change",
            0
        )


        return {

            "explanation":
                (
                    f"{played_move} successfully gained "
                    f"{change} points of material. "
                    "The position became more favorable."
                ),

            "recommendation":
                (
                    "After gaining material, focus on improving "
                    "piece activity and reducing counterplay."
                )
        }



    # ==================================
    # King Safety
    # ==================================

    if reason == "king_safety":

        side = details.get(
            "side",
            "your"
        )


        return {

            "explanation":
                (
                    f"{played_move} weakened the {side} king's safety. "
                    "The position allowed more attacking possibilities "
                    "against the king."
                ),

            "recommendation":
                (
                    "Improve king safety by protecting the king, "
                    "developing defenders, or creating escape squares."
                )
        }



    # ==================================
    # Unknown Position Change
    # ==================================

    return {

        "explanation":
            (
                f"{played_move} changed the evaluation of the position."
            ),

        "recommendation":
            (
                f"Consider the stronger continuation {best_move}."
            )

    }