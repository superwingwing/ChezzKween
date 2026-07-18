import chess

from ml.analysis.piece import (
    analyze_piece
)


def detect_piece_reason(
    before: chess.Board,
    after: chess.Board
):

    reasons = []

    for color in (
        chess.WHITE,
        chess.BLACK
    ):

        side = (
            "white"
            if color == chess.WHITE
            else "black"
        )

        before_data = analyze_piece(
            before,
            color
        )

        after_data = analyze_piece(
            after,
            color
        )

        # Hanging piece fixed

        if (
            after_data["hanging"]
            <
            before_data["hanging"]
        ):

            reasons.append({

                "reason":
                    "piece_saved",

                "confidence":
                    92,

                "details": {

                    "side": side

                }
            })

        # Hanging piece created

        if (
            after_data["hanging"]
            >
            before_data["hanging"]
        ):

            reasons.append({

                "reason":
                    "piece_hanging",

                "confidence":
                    92,

                "details": {

                    "side": side

                }
            })

        # Activity improved

        if (
            after_data["activity"]
            >
            before_data["activity"] + 2
        ):

            reasons.append({

                "reason":
                    "piece_activity",

                "confidence":
                    80,

                "details": {

                    "side": side

                }
            })

        # Coordination improved

        if (
            after_data["coordination"]
            >
            before_data["coordination"]
        ):

            reasons.append({

                "reason":
                    "piece_coordination",

                "confidence":
                    75,

                "details": {

                    "side": side

                }
            })

        # New outpost

        if (
            after_data["outposts"]
            >
            before_data["outposts"]
        ):

            reasons.append({

                "reason":
                    "outpost_created",

                "confidence":
                    88,

                "details": {

                    "side": side

                }
            })

        # Attack concentration

        if (
            after_data["attack_concentration"]
            >
            before_data["attack_concentration"]
        ):

            reasons.append({

                "reason":
                    "attack_concentration",

                "confidence":
                    85,

                "details": {

                    "side": side

                }
            })

    if not reasons:
        return None

    reasons.sort(
        key=lambda x:
        x["confidence"],
        reverse=True
    )

    return reasons[0]