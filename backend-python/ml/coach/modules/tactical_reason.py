import chess

from ml.analysis.tactical import analyze_tactical


def detect_tactical_reason(
    before: chess.Board,
    after: chess.Board
):

    before_data = analyze_tactical(
        before,
        list(before.legal_moves)
    )

    after_data = analyze_tactical(
        after,
        list(after.legal_moves)
    )

    reasons = []

    # ==========================================================
    # MATERIAL WINNING COMBINATION
    # ==========================================================

    if (
        after_data["material_winning_combinations"]
        >
        before_data["material_winning_combinations"]
    ):

        reasons.append({

            "reason":
                "material_combination",

            "confidence":
                95,

            "details": {

                "before":
                    before_data[
                        "material_winning_combinations"
                    ],

                "after":
                    after_data[
                        "material_winning_combinations"
                    ],

                "change":
                    (
                        after_data[
                            "material_winning_combinations"
                        ]
                        -
                        before_data[
                            "material_winning_combinations"
                        ]
                    ),

                # IMPORTANT:
                # Actual tactical moves
                "moves":
                    after_data[
                        "material_winning_moves"
                    ],

                "advantage":
                    "material_can_be_won_through_a_tactical_capture"
            }

        })


    # ==========================================================
    # WINNING EXCHANGE
    # ==========================================================

    if (
        after_data["winning_exchanges"]
        >
        before_data["winning_exchanges"]
    ):

        reasons.append({

            "reason":
                "winning_exchange",

            "confidence":
                92,

            "details": {

                "before":
                    before_data[
                        "winning_exchanges"
                    ],

                "after":
                    after_data[
                        "winning_exchanges"
                    ],

                "change":
                    (
                        after_data[
                            "winning_exchanges"
                        ]
                        -
                        before_data[
                            "winning_exchanges"
                        ]
                    ),

                "moves":
                    after_data[
                        "winning_exchange_moves"
                    ],

                "advantage":
                    "a_more_valuable_piece_can_be_captured"
            }

        })


    # ==========================================================
    # HANGING PIECE
    # ==========================================================

    if (
        after_data["hanging_captures"]
        >
        before_data["hanging_captures"]
    ):

        reasons.append({

            "reason":
                "hanging_piece",

            "confidence":
                90,

            "details": {

                "before":
                    before_data[
                        "hanging_captures"
                    ],

                "after":
                    after_data[
                        "hanging_captures"
                    ],

                "change":
                    (
                        after_data[
                            "hanging_captures"
                        ]
                        -
                        before_data[
                            "hanging_captures"
                        ]
                    ),

                "moves":
                    after_data[
                        "hanging_capture_moves"
                    ],

                "advantage":
                    "an_undefended_piece_can_be_captured"
            }

        })


    # ==========================================================
    # TACTICAL CAPTURE
    # ==========================================================

    if (
        after_data["tactical_captures"]
        >
        before_data["tactical_captures"]
    ):

        reasons.append({

            "reason":
                "tactical_capture",

            "confidence":
                88,

            "details": {

                "before":
                    before_data[
                        "tactical_captures"
                    ],

                "after":
                    after_data[
                        "tactical_captures"
                    ],

                "change":
                    (
                        after_data[
                            "tactical_captures"
                        ]
                        -
                        before_data[
                            "tactical_captures"
                        ]
                    ),

                "moves":
                    after_data[
                        "tactical_capture_moves"
                    ],

                "advantage":
                    "a_capture_creates_a_tactical_opportunity"
            }

        })


    # ==========================================================
    # DOUBLE CHECK
    # ==========================================================

    if (
        after_data["double_checks"]
        >
        before_data["double_checks"]
    ):

        reasons.append({

            "reason":
                "double_check",

            "confidence":
                97,

            "details": {

                "before":
                    before_data[
                        "double_checks"
                    ],

                "after":
                    after_data[
                        "double_checks"
                    ],

                "change":
                    (
                        after_data[
                            "double_checks"
                        ]
                        -
                        before_data[
                            "double_checks"
                        ]
                    ),

                "moves":
                    after_data[
                        "double_check_moves"
                    ],

                "advantage":
                    "the_enemy_king_is_attacked_by_two_lines"
            }

        })


    # ==========================================================
    # DISCOVERED CHECK
    # ==========================================================

    if (
        after_data["discovered_checks"]
        >
        before_data["discovered_checks"]
    ):

        reasons.append({

            "reason":
                "discovered_check",

            "confidence":
                96,

            "details": {

                "before":
                    before_data[
                        "discovered_checks"
                    ],

                "after":
                    after_data[
                        "discovered_checks"
                    ],

                "change":
                    (
                        after_data[
                            "discovered_checks"
                        ]
                        -
                        before_data[
                            "discovered_checks"
                        ]
                    ),

                "moves":
                    after_data[
                        "discovered_check_moves"
                    ],

                "advantage":
                    "moving_one_piece_reveals_an_attack_on_the_king"
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
        "DETECTED TACTICAL REASON:",
        result
    )

    return result