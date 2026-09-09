import chess


def piece_name(name):
    """
    Make piece names readable.
    """
    if not name:
        return "piece"

    return name.lower()


def format_move(move_data):
    """
    Convert tactical move data into a readable description.

    Full UCI/SAN conversion can be handled elsewhere.
    """

    attacker = piece_name(
        move_data.get("attacker")
        or move_data.get("moving_piece")
    )

    victim = piece_name(
        move_data.get("victim")
    )

    from_square = move_data.get(
        "from",
        "?"
    )

    to_square = move_data.get(
        "to",
        "?"
    )

    if victim:
        return (
            f"{attacker} on {from_square} "
            f"captures the {victim} on {to_square}"
        )

    return (
        f"{attacker} moves from "
        f"{from_square} to {to_square}"
    )


def _find_promotion_in_pv(pv):
    """
    Find a promotion move inside the Stockfish PV.
    """

    if not pv:
        return None

    for uci in pv:

        try:
            move = chess.Move.from_uci(uci)

            if move.promotion:
                return move

        except (ValueError, TypeError):
            continue

    return None


def _find_mate_in_pv(pv):
    """
    Look for mate indicators in a PV.

    Stockfish PV itself normally contains moves rather than
    mate scores, so this function mainly detects whether the
    line ends with a mating move when possible.
    """

    if not pv:
        return False

    return len(pv) >= 2


def _pv_after_best_move(best_move, pv):
    """
    Determine whether the supplied PV begins with Stockfish's
    recommended move.
    """

    if not pv or not best_move:
        return False

    return pv[0] == best_move


def _count_material(board):
    """
    Calculate material on the board.

    This is used to compare the position before and after
    the played move.
    """

    values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9
    }

    white = 0
    black = 0

    for piece_type, value in values.items():

        white += (
            len(board.pieces(piece_type, chess.WHITE))
            * value
        )

        black += (
            len(board.pieces(piece_type, chess.BLACK))
            * value
        )

    return white, black


def explain(
    details,
    played_move,
    best_move,
    pv,
    before,
    after
):

    if details is None:
        details = {}

    moves = details.get(
        "moves",
        []
    )

    advantage = details.get(
        "advantage"
    )

    # ==========================================================
    # ACTUAL POSITION INFORMATION
    # ==========================================================

    position_changed = False
    material_before = None
    material_after = None

    if before is not None and after is not None:

        position_changed = (
            before.board_fen()
            != after.board_fen()
        )

        material_before = _count_material(
            before
        )

        material_after = _count_material(
            after
        )

    # ==========================================================
    # ENGINE PV INFORMATION
    # ==========================================================

    promotion_move = _find_promotion_in_pv(
        pv
    )

    pv_follows_best_move = _pv_after_best_move(
        best_move,
        pv
    )

    # ==========================================================
    # MOST RELEVANT TACTICAL EVENT
    # ==========================================================

    move_data = None

    if moves:
        move_data = moves[0]

    # ==========================================================
    # FORCED CHECK / MATE / PROMOTION
    # ==========================================================
    #
    # This is checked before the older tactical categories
    # because the engine PV can reveal that the real reason
    # a move is strong is a forcing sequence.
    #
    # ==========================================================

    if (
        before is not None
        and after is not None
        and after.is_check()
    ):

        if promotion_move:

            promotion_square = chess.square_name(
                promotion_move.to_square
            )

            return {
                "explanation":
                    (
                        f"{played_move} gives check and "
                        f"starts a forcing sequence. "
                        f"The engine's continuation reaches "
                        f"{promotion_square} with promotion, "
                        f"creating a decisive tactical threat."
                    ),

                "recommendation":
                    (
                        f"Follow the forcing continuation "
                        f"beginning with {best_move} and "
                        f"calculate the king's responses carefully."
                    )
            }

        if pv and pv_follows_best_move:

            return {
                "explanation":
                    (
                        f"{played_move} gives check and forces "
                        f"the opponent to respond to the king threat. "
                        f"Stockfish's principal variation shows a "
                        f"forcing continuation after {played_move}."
                    ),

                "recommendation":
                    (
                        f"Continue calculating the forcing line "
                        f"after {best_move} instead of allowing "
                        f"the opponent to escape the attack."
                    )
            }

    # ==========================================================
    # PROMOTION THREAT FROM THE PV
    # ==========================================================

    if promotion_move:

        promotion_square = chess.square_name(
            promotion_move.to_square
        )

        promotion_piece = piece_name(
            chess.piece_symbol(
                promotion_move.promotion
            )
        )

        return {
            "explanation":
                (
                    f"{played_move} creates a strong promotion "
                    f"threat in the engine's continuation. "
                    f"The principal variation reaches "
                    f"{promotion_square} where the pawn promotes "
                    f"to a {promotion_piece}."
                ),

            "recommendation":
                (
                    f"Follow the forcing continuation beginning "
                    f"with {best_move} and prevent the opponent "
                    f"from stopping the promotion."
                )
        }

    # ==========================================================
    # MATERIAL COMBINATION
    # ==========================================================

    if (
        advantage ==
        "material_can_be_won_through_a_tactical_capture"
    ):

        if move_data:

            action = format_move(
                move_data
            )

            gain = move_data.get(
                "material_gain",
                0
            )

            if gain > 0:

                explanation = (
                    f"{action}, gaining approximately "
                    f"{gain} points of material."
                )

            else:

                explanation = (
                    f"The position contains a tactical "
                    f"capture involving {action}."
                )

            if (
                before is not None
                and after is not None
                and position_changed
            ):

                explanation += (
                    " The resulting position changes the "
                    "material balance."
                )

            return {
                "explanation":
                    explanation,

                "recommendation":
                    (
                        f"Look for {best_move} as the "
                        f"stronger continuation."
                    )
            }

    # ==========================================================
    # WINNING EXCHANGE
    # ==========================================================

    if (
        advantage ==
        "a_more_valuable_piece_can_be_captured"
    ):

        if move_data:

            action = format_move(
                move_data
            )

            gain = move_data.get(
                "material_gain",
                0
            )

            return {
                "explanation":
                    (
                        f"{action}. This exchange is favorable "
                        f"because the captured piece is worth "
                        f"more than the attacking piece."
                    ),

                "recommendation":
                    (
                        f"Consider {best_move}, which Stockfish "
                        f"considers stronger in this position."
                    )
            }

    # ==========================================================
    # HANGING PIECE
    # ==========================================================

    if (
        advantage ==
        "an_undefended_piece_can_be_captured"
    ):

        if move_data:

            victim = piece_name(
                move_data.get(
                    "victim"
                )
            )

            square = move_data.get(
                "to",
                "?"
            )

            attacker = piece_name(
                move_data.get(
                    "attacker"
                )
            )

            return {
                "explanation":
                    (
                        f"The {victim} on {square} is "
                        f"undefended and can be captured "
                        f"by the {attacker}. This leaves "
                        f"you vulnerable to losing material."
                    ),

                "recommendation":
                    (
                        f"{best_move} is stronger because "
                        f"it avoids this tactical weakness."
                    )
            }

    # ==========================================================
    # TACTICAL CAPTURE
    # ==========================================================

    if (
        advantage ==
        "a_capture_creates_a_tactical_opportunity"
    ):

        if move_data:

            action = format_move(
                move_data
            )

            return {
                "explanation":
                    (
                        f"{action}. This capture creates "
                        f"a tactical opportunity in the "
                        f"position."
                    ),

                "recommendation":
                    (
                        f"Compare this with {best_move} "
                        f"and calculate the forcing "
                        f"continuation before committing."
                    )
            }

    # ==========================================================
    # DOUBLE CHECK
    # ==========================================================

    if (
        advantage ==
        "the_enemy_king_is_attacked_by_two_lines"
    ):

        king_square = move_data.get(
            "king_square",
            "?"
        ) if move_data else "?"

        return {
            "explanation":
                (
                    f"The move creates a double check "
                    f"against the king on {king_square}. "
                    f"The king is attacked by two "
                    f"separate lines at once."
                ),

            "recommendation":
                (
                    f"Calculate the forcing sequence "
                    f"after {played_move}. "
                    f"The engine recommends {best_move}."
                )
        }

    # ==========================================================
    # DISCOVERED CHECK
    # ==========================================================

    if (
        advantage ==
        "moving_one_piece_reveals_an_attack_on_the_king"
    ):

        if move_data:

            moving_piece = piece_name(
                move_data.get(
                    "moving_piece"
                )
            )

            from_square = move_data.get(
                "from",
                "?"
            )

            to_square = move_data.get(
                "to",
                "?"
            )

            king_square = move_data.get(
                "king_square",
                "?"
            )

            return {
                "explanation":
                    (
                        f"Moving the {moving_piece} "
                        f"from {from_square} to {to_square} "
                        f"reveals an attack on the king "
                        f"on {king_square}. This is a "
                        f"discovered check."
                    ),

                "recommendation":
                    (
                        f"Calculate the forcing sequence "
                        f"carefully before choosing "
                        f"{best_move}."
                    )
            }

    # ==========================================================
    # OLD ISSUE FORMAT
    # ==========================================================

    issue = details.get(
        "issue"
    )

    if issue == "hanging":

        return {
            "explanation":
                (
                    f"{played_move} left a piece "
                    f"vulnerable to capture."
                ),

            "recommendation":
                (
                    f"Check whether your pieces are "
                    f"properly defended before playing "
                    f"{played_move}."
                )
        }

    if issue == "fork":

        return {
            "explanation":
                (
                    f"{played_move} allowed a fork, "
                    f"letting one piece attack multiple "
                    f"targets at once."
                ),

            "recommendation":
                (
                    f"Look for the tactical consequences "
                    f"before choosing {best_move}."
                )
        }

    if issue == "pin":

        return {
            "explanation":
                (
                    f"{played_move} created or allowed "
                    f"a pin that restricts the movement "
                    f"of a piece."
                ),

            "recommendation":
                (
                    f"Check whether the pinned piece "
                    f"can safely move before choosing "
                    f"{best_move}."
                )
        }

    # ==========================================================
    # POSITION CHANGE USING BEFORE / AFTER + PV
    # ==========================================================

    if position_changed:

        if (
            pv
            and pv_follows_best_move
        ):

            return {
                "explanation":
                    (
                        f"{played_move} changed the position, "
                        f"but Stockfish's principal variation "
                        f"shows that {best_move} leads to the "
                        f"stronger continuation."
                    ),

                "recommendation":
                    (
                        f"Compare the resulting position with "
                        f"the engine line beginning with {best_move}."
                    )
            }

        return {
            "explanation":
                (
                    f"{played_move} changed the position "
                    f"significantly and created new tactical "
                    f"possibilities."
                ),

            "recommendation":
                (
                    f"Calculate the resulting position carefully "
                    f"and compare it with {best_move}."
                )
        }

    # ==========================================================
    # FINAL FALLBACK
    # ==========================================================

    return {
        "explanation":
            (
                f"{played_move} does not show a specific "
                f"tactical pattern from the detected information."
            ),

        "recommendation":
            (
                f"Compare {played_move} with the engine's "
                f"stronger move {best_move}."
            )
    }