import chess

from ml.analysis.pawn import (
    passed_pawns,
    isolated_pawns,
    doubled_pawns,
    pawn_chain_count,
    pawn_structure_score
)


def _pawn_details(
    side,
    passed_before,
    passed_after,
    isolated_before,
    isolated_after,
    doubled_before,
    doubled_after,
    chain_before,
    chain_after,
    score_before,
    score_after
):
    """
    Collect all pawn-structure changes for one side.

    The underlying pawn-analysis module remains responsible
    for calculating the features.
    """

    return {
        "side": side,

        # Passed pawns
        "passed_before": passed_before,
        "passed_after": passed_after,
        "passed_change":
            passed_after - passed_before,

        # Isolated pawns
        "isolated_before": isolated_before,
        "isolated_after": isolated_after,
        "isolated_change":
            isolated_after - isolated_before,

        # Doubled pawns
        "doubled_before": doubled_before,
        "doubled_after": doubled_after,
        "doubled_change":
            doubled_after - doubled_before,

        # Pawn chains
        "chain_before": chain_before,
        "chain_after": chain_after,
        "chain_change":
            chain_after - chain_before,

        # Overall structure
        "structure_before": score_before,
        "structure_after": score_after,
        "structure_change":
            score_after - score_before
    }


def detect_pawn_reason(
    before: chess.Board,
    after: chess.Board
):

    reasons = []

    # ==========================================================
    # WHITE PAWN FEATURES
    # ==========================================================

    white_passed_before = passed_pawns(
        before,
        chess.WHITE
    )

    white_passed_after = passed_pawns(
        after,
        chess.WHITE
    )

    white_isolated_before = isolated_pawns(
        before,
        chess.WHITE
    )

    white_isolated_after = isolated_pawns(
        after,
        chess.WHITE
    )

    white_doubled_before = doubled_pawns(
        before,
        chess.WHITE
    )

    white_doubled_after = doubled_pawns(
        after,
        chess.WHITE
    )

    white_chain_before = pawn_chain_count(
        before,
        chess.WHITE
    )

    white_chain_after = pawn_chain_count(
        after,
        chess.WHITE
    )

    white_score_before = pawn_structure_score(
        before,
        chess.WHITE
    )

    white_score_after = pawn_structure_score(
        after,
        chess.WHITE
    )

    white_details = _pawn_details(
        "white",
        white_passed_before,
        white_passed_after,
        white_isolated_before,
        white_isolated_after,
        white_doubled_before,
        white_doubled_after,
        white_chain_before,
        white_chain_after,
        white_score_before,
        white_score_after
    )

    # ==========================================================
    # BLACK PAWN FEATURES
    # ==========================================================

    black_passed_before = passed_pawns(
        before,
        chess.BLACK
    )

    black_passed_after = passed_pawns(
        after,
        chess.BLACK
    )

    black_isolated_before = isolated_pawns(
        before,
        chess.BLACK
    )

    black_isolated_after = isolated_pawns(
        after,
        chess.BLACK
    )

    black_doubled_before = doubled_pawns(
        before,
        chess.BLACK
    )

    black_doubled_after = doubled_pawns(
        after,
        chess.BLACK
    )

    black_chain_before = pawn_chain_count(
        before,
        chess.BLACK
    )

    black_chain_after = pawn_chain_count(
        after,
        chess.BLACK
    )

    black_score_before = pawn_structure_score(
        before,
        chess.BLACK
    )

    black_score_after = pawn_structure_score(
        after,
        chess.BLACK
    )

    black_details = _pawn_details(
        "black",
        black_passed_before,
        black_passed_after,
        black_isolated_before,
        black_isolated_after,
        black_doubled_before,
        black_doubled_after,
        black_chain_before,
        black_chain_after,
        black_score_before,
        black_score_after
    )

    # ==========================================================
    # WHITE PASSED PAWN
    # ==========================================================

    if white_passed_after > white_passed_before:

        reasons.append({
            "reason": "pawn_passed_pawn_created",
            "confidence": 95,

            "details": {
                **white_details,

                "advantage":
                    "created_passed_pawn",

                "meaning":
                    "white_has_a_pawn_with_no_enemy_pawn_blocking_its_file_or_adjacent_files"
            }
        })

    # ==========================================================
    # BLACK PASSED PAWN
    # ==========================================================

    if black_passed_after > black_passed_before:

        reasons.append({
            "reason": "pawn_passed_pawn_created",
            "confidence": 95,

            "details": {
                **black_details,

                "advantage":
                    "created_passed_pawn",

                "meaning":
                    "black_has_a_pawn_with_no_enemy_pawn_blocking_its_file_or_adjacent_files"
            }
        })

    # ==========================================================
    # WHITE ISOLATED PAWN
    # ==========================================================

    if white_isolated_after > white_isolated_before:

        reasons.append({
            "reason": "pawn_isolated_pawn_created",
            "confidence": 90,

            "details": {
                **white_details,

                "advantage":
                    "created_isolated_pawn",

                "meaning":
                    "white_created_a_pawn_without_support_from_adjacent_pawns"
            }
        })

    # ==========================================================
    # BLACK ISOLATED PAWN
    # ==========================================================

    if black_isolated_after > black_isolated_before:

        reasons.append({
            "reason": "pawn_isolated_pawn_created",
            "confidence": 90,

            "details": {
                **black_details,

                "advantage":
                    "created_isolated_pawn",

                "meaning":
                    "black_created_a_pawn_without_support_from_adjacent_pawns"
            }
        })

    # ==========================================================
    # WHITE DOUBLED PAWN
    # ==========================================================

    if white_doubled_after > white_doubled_before:

        reasons.append({
            "reason": "pawn_doubled_pawn_created",
            "confidence": 88,

            "details": {
                **white_details,

                "advantage":
                    "created_doubled_pawns",

                "meaning":
                    "white_has_multiple_pawns_on_the_same_file"
            }
        })

    # ==========================================================
    # BLACK DOUBLED PAWN
    # ==========================================================

    if black_doubled_after > black_doubled_before:

        reasons.append({
            "reason": "pawn_doubled_pawn_created",
            "confidence": 88,

            "details": {
                **black_details,

                "advantage":
                    "created_doubled_pawns",

                "meaning":
                    "black_has_multiple_pawns_on_the_same_file"
            }
        })

    # ==========================================================
    # WHITE PAWN CHAIN IMPROVED
    # ==========================================================

    if white_chain_after > white_chain_before:

        reasons.append({
            "reason": "pawn_chain_strengthened",
            "confidence": 82,

            "details": {
                **white_details,

                "advantage":
                    "stronger_pawn_chain",

                "meaning":
                    "white_pawns_provide_more_support_to_each_other"
            }
        })

    # ==========================================================
    # BLACK PAWN CHAIN IMPROVED
    # ==========================================================

    if black_chain_after > black_chain_before:

        reasons.append({
            "reason": "pawn_chain_strengthened",
            "confidence": 82,

            "details": {
                **black_details,

                "advantage":
                    "stronger_pawn_chain",

                "meaning":
                    "black_pawns_provide_more_support_to_each_other"
            }
        })

    # ==========================================================
    # WHITE STRUCTURE IMPROVED
    # ==========================================================

    white_change = (
        white_score_after
        -
        white_score_before
    )

    if white_change >= 2:

        reasons.append({
            "reason": "pawn_structure_improved",
            "confidence": 75,

            "details": {
                **white_details,

                "advantage":
                    "improved_pawn_structure",

                "meaning":
                    "white_pawn_structure_became_more_favorable"
            }
        })

    # ==========================================================
    # WHITE STRUCTURE WEAKENED
    # ==========================================================

    elif white_change <= -2:

        reasons.append({
            "reason": "pawn_structure_weakened",
            "confidence": 75,

            "details": {
                **white_details,

                "advantage":
                    "weakened_pawn_structure",

                "meaning":
                    "white_pawn_structure_became_more_vulnerable"
            }
        })

    # ==========================================================
    # BLACK STRUCTURE IMPROVED
    # ==========================================================

    black_change = (
        black_score_after
        -
        black_score_before
    )

    if black_change >= 2:

        reasons.append({
            "reason": "pawn_structure_improved",
            "confidence": 75,

            "details": {
                **black_details,

                "advantage":
                    "improved_pawn_structure",

                "meaning":
                    "black_pawn_structure_became_more_favorable"
            }
        })

    # ==========================================================
    # BLACK STRUCTURE WEAKENED
    # ==========================================================

    elif black_change <= -2:

        reasons.append({
            "reason": "pawn_structure_weakened",
            "confidence": 75,

            "details": {
                **black_details,

                "advantage":
                    "weakened_pawn_structure",

                "meaning":
                    "black_pawn_structure_became_more_vulnerable"
            }
        })

    # ==========================================================
    # NOTHING FOUND
    # ==========================================================

    if not reasons:
        return None

    # ==========================================================
    # STRONGEST REASON
    # ==========================================================

    reasons.sort(
        key=lambda r: r["confidence"],
        reverse=True
    )

    result = reasons[0]

    print(
        "PAWN REASON:",
        result
    )

    return result