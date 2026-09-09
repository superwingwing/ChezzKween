import chess


def explain(details, played_move, best_move, pv, before, after):

    change = details.get("change", 0)
    material_change = abs(change)

    # Determine whether the position actually changed materially
    before_material = sum(
        len(before.pieces(piece_type, chess.WHITE)) * value +
        len(before.pieces(piece_type, chess.BLACK)) * value
        for piece_type, value in {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9
        }.items()
    )

    after_material = sum(
        len(after.pieces(piece_type, chess.WHITE)) * value +
        len(after.pieces(piece_type, chess.BLACK)) * value
        for piece_type, value in {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9
        }.items()
    )

    actual_material_change = after_material - before_material

    # Material was lost
    if change < 0:

        explanation = (
            f"{played_move} resulted in approximately "
            f"{material_change} points of material being lost."
        )

        # Use the actual board transition to make sure material really changed
        if actual_material_change < 0:
            explanation = (
                f"{played_move} gave up material, leaving your position "
                f"with fewer material resources."
            )

        return {
            "explanation": explanation,

            "recommendation":
                f"Look for the tactical consequences before committing to the move. "
                f"A stronger continuation was {best_move}."
        }

    # Material was gained
    if change > 0:

        explanation = (
            f"{played_move} gained approximately "
            f"{material_change} points of material."
        )

        if actual_material_change > 0:
            explanation = (
                f"{played_move} won material and improved your material advantage."
            )

        return {
            "explanation": explanation,

            "recommendation":
                "After winning material, look to consolidate the advantage "
                "and avoid unnecessary complications."
        }

    # No meaningful material change
    return {
        "explanation":
            f"{played_move} did not create a significant material change.",

        "recommendation":
            f"Focus on the positional and tactical consequences of the move. "
            f"Consider {best_move} if it is the stronger continuation."
    }