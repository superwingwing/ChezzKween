import chess

from ml.analysis.king import analyze_king


def _build_king_details(
    side,
    before_data,
    after_data
):
    """
    Build detailed king-safety information.

    analyze_king() remains responsible for calculating
    the actual king metrics. This function interprets
    the changes for the coaching system.
    """

    safety_change = (
        after_data["safety"]
        -
        before_data["safety"]
    )

    pressure_change = (
        after_data["pressure"]
        -
        before_data["pressure"]
    )

    rook_change = (
        after_data["rook_attackers"]
        -
        before_data["rook_attackers"]
    )

    return {
        "side": side,

        # Raw values
        "safety_before": before_data["safety"],
        "safety_after": after_data["safety"],
        "safety_change": safety_change,

        "pressure_before": before_data["pressure"],
        "pressure_after": after_data["pressure"],
        "pressure_change": pressure_change,

        "rook_attackers_before":
            before_data["rook_attackers"],

        "rook_attackers_after":
            after_data["rook_attackers"],

        "rook_attackers_change":
            rook_change,

        # State changes
        "castled_before":
            before_data["castled"],

        "castled_after":
            after_data["castled"],

        "queen_attack_before":
            before_data["queen_attack"],

        "queen_attack_after":
            after_data["queen_attack"],

        "open_file_before":
            before_data["open_file"],

        "open_file_after":
            after_data["open_file"],
    }


def detect_king_reason(
    before: chess.Board,
    after: chess.Board
):

    reasons = []

    # ==========================================================
    # ANALYZE BOTH KINGS
    # ==========================================================

    white_before = analyze_king(
        before,
        chess.WHITE
    )

    white_after = analyze_king(
        after,
        chess.WHITE
    )

    black_before = analyze_king(
        before,
        chess.BLACK
    )

    black_after = analyze_king(
        after,
        chess.BLACK
    )

    # ==========================================================
    # WHITE KING
    # ==========================================================

    if white_before and white_after:

        details = _build_king_details(
            "white",
            white_before,
            white_after
        )

        # ------------------------------------------------------
        # CASTLING
        # ------------------------------------------------------

        if (
            not white_before["castled"]
            and
            white_after["castled"]
        ):

            reasons.append({
                "reason": "king_safety_castled",
                "confidence": 98,

                "details": {
                    **details,

                    "advantage":
                        "king_safety_and_rook_activation",

                    "meaning":
                        "king_castled_and_rook_activated"
                }
            })

        # ------------------------------------------------------
        # KING SAFETY WEAKENED
        # ------------------------------------------------------

        if (
            white_after["safety"]
            <
            white_before["safety"]
        ):

            reasons.append({
                "reason": "king_safety_weakened",
                "confidence": 90,

                "details": {
                    **details,

                    "advantage":
                        "opponent_gained_king_pressure",

                    "meaning":
                        "white_king_became_less_safe"
                }
            })

        # ------------------------------------------------------
        # KING SAFETY IMPROVED
        # ------------------------------------------------------

        elif (
            white_after["safety"]
            >
            white_before["safety"]
        ):

            reasons.append({
                "reason": "king_safety_improved",
                "confidence": 90,

                "details": {
                    **details,

                    "advantage":
                        "improved_king_safety",

                    "meaning":
                        "white_king_became_safer"
                }
            })

        # ------------------------------------------------------
        # INCREASED PRESSURE ON WHITE KING
        # ------------------------------------------------------

        if (
            white_after["pressure"]
            >
            white_before["pressure"]
        ):

            reasons.append({
                "reason": "king_under_pressure",
                "confidence": 85,

                "details": {
                    **details,

                    "advantage":
                        "increased_pressure_against_king",

                    "meaning":
                        "opponent_increased_attacking_pressure"
                }
            })

        # ------------------------------------------------------
        # QUEEN STARTED ATTACKING WHITE KING
        # ------------------------------------------------------

        if (
            not white_before["queen_attack"]
            and
            white_after["queen_attack"]
        ):

            reasons.append({
                "reason": "king_queen_attack_started",
                "confidence": 88,

                "details": {
                    **details,

                    "advantage":
                        "queen_joined_attack_on_king",

                    "meaning":
                        "enemy_queen_began_attacking_king"
                }
            })

        # ------------------------------------------------------
        # ROOK ATTACKERS INCREASED
        # ------------------------------------------------------

        if (
            white_after["rook_attackers"]
            >
            white_before["rook_attackers"]
        ):

            reasons.append({
                "reason": "king_rook_attack_started",
                "confidence": 86,

                "details": {
                    **details,

                    "advantage":
                        "rook_pressure_against_king",

                    "meaning":
                        "enemy_rook_pressure_increased"
                }
            })

        # ------------------------------------------------------
        # FILE OPENED TOWARD WHITE KING
        # ------------------------------------------------------

        if (
            not white_before["open_file"]
            and
            white_after["open_file"]
        ):

            reasons.append({
                "reason": "king_file_opened",
                "confidence": 89,

                "details": {
                    **details,

                    "advantage":
                        "opened_attack_line_to_king",

                    "meaning":
                        "file_opened_toward_white_king"
                }
            })

    # ==========================================================
    # BLACK KING
    # ==========================================================

    if black_before and black_after:

        details = _build_king_details(
            "black",
            black_before,
            black_after
        )

        # ------------------------------------------------------
        # CASTLING
        # ------------------------------------------------------

        if (
            not black_before["castled"]
            and
            black_after["castled"]
        ):

            reasons.append({
                "reason": "king_safety_castled",
                "confidence": 98,

                "details": {
                    **details,

                    "advantage":
                        "king_safety_and_rook_activation",

                    "meaning":
                        "king_castled_and_rook_activated"
                }
            })

        # ------------------------------------------------------
        # KING SAFETY WEAKENED
        # ------------------------------------------------------

        if (
            black_after["safety"]
            <
            black_before["safety"]
        ):

            reasons.append({
                "reason": "king_safety_weakened",
                "confidence": 90,

                "details": {
                    **details,

                    "advantage":
                        "opponent_gained_king_pressure",

                    "meaning":
                        "black_king_became_less_safe"
                }
            })

        # ------------------------------------------------------
        # KING SAFETY IMPROVED
        # ------------------------------------------------------

        elif (
            black_after["safety"]
            >
            black_before["safety"]
        ):

            reasons.append({
                "reason": "king_safety_improved",
                "confidence": 90,

                "details": {
                    **details,

                    "advantage":
                        "improved_king_safety",

                    "meaning":
                        "black_king_became_safer"
                }
            })

        # ------------------------------------------------------
        # INCREASED PRESSURE ON BLACK KING
        # ------------------------------------------------------

        if (
            black_after["pressure"]
            >
            black_before["pressure"]
        ):

            reasons.append({
                "reason": "king_under_pressure",
                "confidence": 85,

                "details": {
                    **details,

                    "advantage":
                        "increased_pressure_against_king",

                    "meaning":
                        "opponent_increased_attacking_pressure"
                }
            })

        # ------------------------------------------------------
        # QUEEN STARTED ATTACKING BLACK KING
        # ------------------------------------------------------

        if (
            not black_before["queen_attack"]
            and
            black_after["queen_attack"]
        ):

            reasons.append({
                "reason": "king_queen_attack_started",
                "confidence": 88,

                "details": {
                    **details,

                    "advantage":
                        "queen_joined_attack_on_king",

                    "meaning":
                        "enemy_queen_began_attacking_king"
                }
            })

        # ------------------------------------------------------
        # ROOK ATTACKERS INCREASED
        # ------------------------------------------------------

        if (
            black_after["rook_attackers"]
            >
            black_before["rook_attackers"]
        ):

            reasons.append({
                "reason": "king_rook_attack_started",
                "confidence": 86,

                "details": {
                    **details,

                    "advantage":
                        "rook_pressure_against_king",

                    "meaning":
                        "enemy_rook_pressure_increased"
                }
            })

        # ------------------------------------------------------
        # FILE OPENED TOWARD BLACK KING
        # ------------------------------------------------------

        if (
            not black_before["open_file"]
            and
            black_after["open_file"]
        ):

            reasons.append({
                "reason": "king_file_opened",
                "confidence": 89,

                "details": {
                    **details,

                    "advantage":
                        "opened_attack_line_to_king",

                    "meaning":
                        "file_opened_toward_black_king"
                }
            })

    # ==========================================================
    # NO KING REASON
    # ==========================================================

    if not reasons:
        return None

    # ==========================================================
    # STRONGEST KING REASON
    # ==========================================================

    reasons.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    result = reasons[0]

    print(
        "KING REASON:",
        result
    )

    return result