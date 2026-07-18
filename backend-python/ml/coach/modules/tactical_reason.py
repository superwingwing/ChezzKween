import chess

from ml.analysis.tactical import analyze_tactical


def detect_tactical_reason(before: chess.Board, after: chess.Board):

    before_data = analyze_tactical(
        before,
        list(before.legal_moves)
    )

    after_data = analyze_tactical(
        after,
        list(after.legal_moves)
    )

    reasons = []

    if (
        after_data["material_winning_combinations"] >
        before_data["material_winning_combinations"]
    ):

        reasons.append({

            "reason": "material_combination",

            "confidence": 95,

            "details": {}

        })


    if (
        after_data["winning_exchanges"] >
        before_data["winning_exchanges"]
    ):

        reasons.append({

            "reason": "winning_exchange",

            "confidence": 92,

            "details": {}

        })


    if (
        after_data["hanging_captures"] >
        before_data["hanging_captures"]
    ):

        reasons.append({

            "reason": "hanging_piece",

            "confidence": 90,

            "details": {}

        })


    if (
        after_data["tactical_captures"] >
        before_data["tactical_captures"]
    ):

        reasons.append({

            "reason": "tactical_capture",

            "confidence": 88,

            "details": {}

        })


    if (
        after_data["double_checks"] >
        before_data["double_checks"]
    ):

        reasons.append({

            "reason": "double_check",

            "confidence": 97,

            "details": {}

        })


    if (
        after_data["discovered_checks"] >
        before_data["discovered_checks"]
    ):

        reasons.append({

            "reason": "discovered_check",

            "confidence": 96,

            "details": {}

        })


    if not reasons:
        return None

    reasons.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    return reasons[0]