import chess

from ml.analysis.king import analyze_king


def detect_king_reason(before, after):

    reasons = []

    # -----------------------------
    # White king
    # -----------------------------

    white_before = analyze_king(before, chess.WHITE)
    white_after = analyze_king(after, chess.WHITE)

    # -----------------------------
    # Black king
    # -----------------------------

    black_before = analyze_king(before, chess.BLACK)
    black_after = analyze_king(after, chess.BLACK)

    # ======================================
    # WHITE KING
    # ======================================

    if white_before and white_after:

        # Castling

        if (
            not white_before["castled"]
            and
            white_after["castled"]
        ):
            reasons.append({
                "reason": "castled",
                "confidence": 98,
                "details": {
                    "side": "white"
                }
            })

        # Safety

        if (
            white_after["safety"]
            <
            white_before["safety"]
        ):
            reasons.append({
                "reason": "king_safety_weakened",
                "confidence": 90,
                "details": {
                    "side": "white",
                    "change":
                        white_after["safety"]
                        -
                        white_before["safety"]
                }
            })

        elif (
            white_after["safety"]
            >
            white_before["safety"]
        ):
            reasons.append({
                "reason": "king_safety_improved",
                "confidence": 90,
                "details": {
                    "side": "white",
                    "change":
                        white_after["safety"]
                        -
                        white_before["safety"]
                }
            })

        # Pressure

        if (
            white_after["pressure"]
            >
            white_before["pressure"]
        ):
            reasons.append({
                "reason": "king_under_pressure",
                "confidence": 85,
                "details": {
                    "side": "white"
                }
            })

        # Queen attack

        if (
            not white_before["queen_attack"]
            and
            white_after["queen_attack"]
        ):
            reasons.append({
                "reason": "queen_attack_started",
                "confidence": 82,
                "details": {
                    "side": "white"
                }
            })

        # Rook attack

        if (
            white_after["rook_attackers"]
            >
            white_before["rook_attackers"]
        ):
            reasons.append({
                "reason": "rook_attack_started",
                "confidence": 80,
                "details": {
                    "side": "white"
                }
            })

        # Open file

        if (
            not white_before["open_file"]
            and
            white_after["open_file"]
        ):
            reasons.append({
                "reason": "king_file_opened",
                "confidence": 80,
                "details": {
                    "side": "white"
                }
            })


    # ======================================
    # BLACK KING
    # ======================================

    if black_before and black_after:

        if (
            not black_before["castled"]
            and
            black_after["castled"]
        ):
            reasons.append({
                "reason": "castled",
                "confidence": 98,
                "details": {
                    "side": "black"
                }
            })

        if (
            black_after["safety"]
            <
            black_before["safety"]
        ):
            reasons.append({
                "reason": "king_safety_weakened",
                "confidence": 90,
                "details": {
                    "side": "black",
                    "change":
                        black_after["safety"]
                        -
                        black_before["safety"]
                }
            })

        elif (
            black_after["safety"]
            >
            black_before["safety"]
        ):
            reasons.append({
                "reason": "king_safety_improved",
                "confidence": 90,
                "details": {
                    "side": "black",
                    "change":
                        black_after["safety"]
                        -
                        black_before["safety"]
                }
            })

        if (
            black_after["pressure"]
            >
            black_before["pressure"]
        ):
            reasons.append({
                "reason": "king_under_pressure",
                "confidence": 85,
                "details": {
                    "side": "black"
                }
            })

        if (
            not black_before["queen_attack"]
            and
            black_after["queen_attack"]
        ):
            reasons.append({
                "reason": "queen_attack_started",
                "confidence": 82,
                "details": {
                    "side": "black"
                }
            })

        if (
            black_after["rook_attackers"]
            >
            black_before["rook_attackers"]
        ):
            reasons.append({
                "reason": "rook_attack_started",
                "confidence": 80,
                "details": {
                    "side": "black"
                }
            })

        if (
            not black_before["open_file"]
            and
            black_after["open_file"]
        ):
            reasons.append({
                "reason": "king_file_opened",
                "confidence": 80,
                "details": {
                    "side": "black"
                }
            })


    if not reasons:
        return None

    reasons.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    return reasons[0]