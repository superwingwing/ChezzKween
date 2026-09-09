import chess

from ml.analysis.piece import analyze_piece


# ==========================================================
# Helpers
# ==========================================================

def piece_name(piece: chess.Piece) -> str:
    names = {
        chess.PAWN: "pawn",
        chess.KNIGHT: "knight",
        chess.BISHOP: "bishop",
        chess.ROOK: "rook",
        chess.QUEEN: "queen",
        chess.KING: "king"
    }

    return names.get(piece.piece_type, "piece")


def find_hanging_pieces(
    board: chess.Board,
    color: chess.Color
):
    """
    Find pieces belonging to 'color' that are attacked
    by the opponent and have insufficient protection.

    This is intentionally conservative.
    """

    hanging = []

    opponent = not color

    for square, piece in board.piece_map().items():

        if piece.color != color:
            continue

        # Kings are not treated as hanging pieces.
        if piece.piece_type == chess.KING:
            continue

        attackers = board.attackers(
            opponent,
            square
        )

        if not attackers:
            continue

        defenders = board.attackers(
            color,
            square
        )

        # A piece attacked with no defender is a strong
        # candidate for being hanging.
        if not defenders:

            hanging.append({
                "square": chess.square_name(square),
                "piece": piece_name(piece),
                "piece_type": piece.piece_type,
                "value": {
                    chess.PAWN: 1,
                    chess.KNIGHT: 3,
                    chess.BISHOP: 3,
                    chess.ROOK: 5,
                    chess.QUEEN: 9,
                    chess.KING: 0
                }.get(piece.piece_type, 0)
            })

    return hanging


def find_new_hanging_pieces(
    before: chess.Board,
    after: chess.Board,
    color: chess.Color
):
    """
    Find pieces that became hanging after the move.
    """

    before_hanging = find_hanging_pieces(
        before,
        color
    )

    after_hanging = find_hanging_pieces(
        after,
        color
    )

    before_keys = {
        (p["square"], p["piece"])
        for p in before_hanging
    }

    return [
        p
        for p in after_hanging
        if (p["square"], p["piece"])
        not in before_keys
    ]


def find_saved_pieces(
    before: chess.Board,
    after: chess.Board,
    color: chess.Color
):
    """
    Find pieces that were hanging before but are no longer
    hanging after the move.
    """

    before_hanging = find_hanging_pieces(
        before,
        color
    )

    after_hanging = find_hanging_pieces(
        after,
        color
    )

    after_keys = {
        (p["square"], p["piece"])
        for p in after_hanging
    }

    return [
        p
        for p in before_hanging
        if (p["square"], p["piece"])
        not in after_keys
    ]


# ==========================================================
# Main detector
# ==========================================================

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

        # ==================================================
        # HANGING PIECE CREATED
        # ==================================================

        if (
            after_data["hanging"]
            >
            before_data["hanging"]
        ):

            new_hanging = find_new_hanging_pieces(
                before,
                after,
                color
            )

            reasons.append({

                "reason":
                    "piece_hanging",

                "confidence":
                    94,

                "details": {

                    "side":
                        side,

                    "hanging_before":
                        before_data["hanging"],

                    "hanging_after":
                        after_data["hanging"],

                    "hanging_change":
                        (
                            after_data["hanging"]
                            -
                            before_data["hanging"]
                        ),

                    "pieces":
                        new_hanging,

                    "advantage":
                        "opponent_can_target_an_undefended_piece",

                    "meaning":
                        "a_piece_became_vulnerable_to_capture"
                }
            })

        # ==================================================
        # HANGING PIECE SAVED
        # ==================================================

        if (
            after_data["hanging"]
            <
            before_data["hanging"]
        ):

            saved = find_saved_pieces(
                before,
                after,
                color
            )

            reasons.append({

                "reason":
                    "piece_saved",

                "confidence":
                    92,

                "details": {

                    "side":
                        side,

                    "hanging_before":
                        before_data["hanging"],

                    "hanging_after":
                        after_data["hanging"],

                    "hanging_change":
                        (
                            after_data["hanging"]
                            -
                            before_data["hanging"]
                        ),

                    "pieces":
                        saved,

                    "advantage":
                        "reduced_piece_vulnerability",

                    "meaning":
                        "a_vulnerable_piece_was_protected_or_repositioned"
                }
            })

        # ==================================================
        # PIECE ACTIVITY
        # ==================================================

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

                    "side":
                        side,

                    "activity_before":
                        before_data["activity"],

                    "activity_after":
                        after_data["activity"],

                    "activity_change":
                        (
                            after_data["activity"]
                            -
                            before_data["activity"]
                        ),

                    "advantage":
                        "more_active_piece_placement",

                    "meaning":
                        "the_pieces_gained_more_active_squares_or_targets"
                }
            })

        # ==================================================
        # PIECE COORDINATION
        # ==================================================

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

                    "side":
                        side,

                    "coordination_before":
                        before_data["coordination"],

                    "coordination_after":
                        after_data["coordination"],

                    "coordination_change":
                        (
                            after_data["coordination"]
                            -
                            before_data["coordination"]
                        ),

                    "advantage":
                        "better_piece_coordination",

                    "meaning":
                        "the_pieces_support_each_other_more_effectively"
                }
            })

        # ==================================================
        # OUTPOST
        # ==================================================

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

                    "side":
                        side,

                    "outposts_before":
                        before_data["outposts"],

                    "outposts_after":
                        after_data["outposts"],

                    "outposts_change":
                        (
                            after_data["outposts"]
                            -
                            before_data["outposts"]
                        ),

                    "advantage":
                        "created_strong_outpost",

                    "meaning":
                        "a_piece_can_use_a_square_that_is_difficult_for_enemy_pawns_to_challenge"
                }
            })

        # ==================================================
        # ATTACK CONCENTRATION
        # ==================================================

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

                    "side":
                        side,

                    "attack_concentration_before":
                        before_data[
                            "attack_concentration"
                        ],

                    "attack_concentration_after":
                        after_data[
                            "attack_concentration"
                        ],

                    "attack_concentration_change":
                        (
                            after_data[
                                "attack_concentration"
                            ]
                            -
                            before_data[
                                "attack_concentration"
                            ]
                        ),

                    "advantage":
                        "more_pieces_concentrated_against_a_target",

                    "meaning":
                        "multiple_pieces_are_focusing_on_the_same_area_or_target"
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
        key=lambda x:
        x["confidence"],
        reverse=True
    )

    result = reasons[0]

    print(
        "PIECE REASON:",
        result
    )

    return result