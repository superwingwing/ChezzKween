import chess

from ml.analysis.pawn import (
    passed_pawns,
    isolated_pawns,
    doubled_pawns,
    pawn_chain_count,
    pawn_structure_score
)


def detect_pawn_reason(before, after):

    reasons = []

    # -----------------------------------
    # White Pawn Features
    # -----------------------------------

    white_passed_before = passed_pawns(before, chess.WHITE)
    white_passed_after = passed_pawns(after, chess.WHITE)

    white_isolated_before = isolated_pawns(before, chess.WHITE)
    white_isolated_after = isolated_pawns(after, chess.WHITE)

    white_doubled_before = doubled_pawns(before, chess.WHITE)
    white_doubled_after = doubled_pawns(after, chess.WHITE)

    white_chain_before = pawn_chain_count(before, chess.WHITE)
    white_chain_after = pawn_chain_count(after, chess.WHITE)

    white_score_before = pawn_structure_score(before, chess.WHITE)
    white_score_after = pawn_structure_score(after, chess.WHITE)


    # -----------------------------------
    # Black Pawn Features
    # -----------------------------------

    black_passed_before = passed_pawns(before, chess.BLACK)
    black_passed_after = passed_pawns(after, chess.BLACK)

    black_isolated_before = isolated_pawns(before, chess.BLACK)
    black_isolated_after = isolated_pawns(after, chess.BLACK)

    black_doubled_before = doubled_pawns(before, chess.BLACK)
    black_doubled_after = doubled_pawns(after, chess.BLACK)

    black_chain_before = pawn_chain_count(before, chess.BLACK)
    black_chain_after = pawn_chain_count(after, chess.BLACK)

    black_score_before = pawn_structure_score(before, chess.BLACK)
    black_score_after = pawn_structure_score(after, chess.BLACK)


    # ===================================
    # Passed Pawn
    # ===================================

    if white_passed_after > white_passed_before:
        reasons.append({
            "reason": "passed_pawn_created",
            "confidence": 95,
            "details": {
                "side": "white"
            }
        })

    if black_passed_after > black_passed_before:
        reasons.append({
            "reason": "passed_pawn_created",
            "confidence": 95,
            "details": {
                "side": "black"
            }
        })


    # ===================================
    # Isolated Pawn
    # ===================================

    if white_isolated_after > white_isolated_before:
        reasons.append({
            "reason": "isolated_pawn_created",
            "confidence": 90,
            "details": {
                "side": "white"
            }
        })

    if black_isolated_after > black_isolated_before:
        reasons.append({
            "reason": "isolated_pawn_created",
            "confidence": 90,
            "details": {
                "side": "black"
            }
        })


    # ===================================
    # Doubled Pawn
    # ===================================

    if white_doubled_after > white_doubled_before:
        reasons.append({
            "reason": "doubled_pawn_created",
            "confidence": 88,
            "details": {
                "side": "white"
            }
        })

    if black_doubled_after > black_doubled_before:
        reasons.append({
            "reason": "doubled_pawn_created",
            "confidence": 88,
            "details": {
                "side": "black"
            }
        })


    # ===================================
    # Pawn Chain
    # ===================================

    if white_chain_after > white_chain_before:
        reasons.append({
            "reason": "pawn_chain_strengthened",
            "confidence": 82,
            "details": {
                "side": "white"
            }
        })

    if black_chain_after > black_chain_before:
        reasons.append({
            "reason": "pawn_chain_strengthened",
            "confidence": 82,
            "details": {
                "side": "black"
            }
        })


    # ===================================
    # Pawn Structure Score
    # ===================================

    white_change = white_score_after - white_score_before

    if white_change >= 2:
        reasons.append({
            "reason": "pawn_structure_improved",
            "confidence": 75,
            "details": {
                "side": "white",
                "change": white_change
            }
        })

    elif white_change <= -2:
        reasons.append({
            "reason": "pawn_structure_weakened",
            "confidence": 75,
            "details": {
                "side": "white",
                "change": white_change
            }
        })


    black_change = black_score_after - black_score_before

    if black_change >= 2:
        reasons.append({
            "reason": "pawn_structure_improved",
            "confidence": 75,
            "details": {
                "side": "black",
                "change": black_change
            }
        })

    elif black_change <= -2:
        reasons.append({
            "reason": "pawn_structure_weakened",
            "confidence": 75,
            "details": {
                "side": "black",
                "change": black_change
            }
        })


    # ===================================
    # Nothing Found
    # ===================================

    if not reasons:
        return None


    # Highest Confidence Pawn Reason

    reasons.sort(
        key=lambda r: r["confidence"],
        reverse=True
    )

    return reasons[0]