def build_explanation(analysis):

    explanations = []
    recommendations = []

    # ======================================
    # Capture
    # ======================================

    if analysis["capture"]:

        explanations.append(
            "This move captures an opponent's piece and gains material."
        )

        recommendations.append(
            "Look for ways to maintain your material advantage while continuing your development."
        )

    # ======================================
    # Check
    # ======================================

    if analysis["check"]:

        explanations.append(
            "This move places the opponent's king in check, forcing an immediate response."
        )

        recommendations.append(
            "Take advantage of the forced response to improve your position or continue your attack."
        )

    # ======================================
    # Castling
    # ======================================

    if analysis["castle"]:

        explanations.append(
            "Castling improves king safety and connects your rooks."
        )

        recommendations.append(
            "With your king safer, continue developing your remaining pieces."
        )

    # ======================================
    # Promotion
    # ======================================

    if analysis["promotion"]:

        explanations.append(
            "This move promotes a pawn into a stronger piece, greatly increasing your attacking potential."
        )

        recommendations.append(
            "Use your newly promoted piece to create threats while avoiding unnecessary exchanges."
        )

    # ======================================
    # Checkmate
    # ======================================

    if analysis["checkmate"]:

        explanations.append(
            "This move delivers checkmate and ends the game."
        )

        recommendations.append(
            "Excellent finish. Look for similar mating patterns in future games."
        )

    # ======================================
    # Stalemate
    # ======================================

    if analysis["stalemate"]:

        explanations.append(
            "This move results in a stalemate, ending the game in a draw."
        )

        recommendations.append(
            "When you have an advantage, always check whether your opponent has any legal moves remaining."
        )

    # ======================================
    # Quiet Move
    # ======================================

    if len(explanations) == 0:

        explanations.append(
            "This move improves your position without creating immediate tactical threats."
        )

        recommendations.append(
            "Continue improving your piece activity and coordinate your forces."
        )

    return {

        "move": analysis["move"],

        "explanation": " ".join(explanations),

        "recommendation": " ".join(recommendations)

    }