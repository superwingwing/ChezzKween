import chess


# ==========================================================
# PIECE NAMES
# ==========================================================

PIECE_NAMES = {
    chess.PAWN: "pawn",
    chess.KNIGHT: "knight",
    chess.BISHOP: "bishop",
    chess.ROOK: "rook",
    chess.QUEEN: "queen",
    chess.KING: "king",
}


PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}


# ==========================================================
# MOVE QUALITY
# ==========================================================

def calculate_move_quality(
    before,
    after,
    evaluation_before,
    evaluation_after
):
    """
    Calculate move quality using the same thresholds used
    by the analysis service.

    Evaluation is assumed to be from White's perspective.
    """

    if after.is_checkmate():
        return "best"

    if evaluation_before is None or evaluation_after is None:
        return None

    if before.turn == chess.WHITE:
        eval_change = evaluation_after - evaluation_before
    else:
        eval_change = evaluation_before - evaluation_after

    centipawn_loss = max(0, -eval_change)

    if centipawn_loss < 0.3:
        return "best"

    if centipawn_loss < 0.7:
        return "good"

    if centipawn_loss < 1.5:
        return "inaccuracy"

    if centipawn_loss < 3:
        return "mistake"

    return "blunder"


# ==========================================================
# QUALITY VERDICT
# ==========================================================

def quality_verdict(
    played_move,
    quality
):
    """
    Generate the opening sentence that describes the
    quality of the move.
    """

    if quality == "best":
        return (
            f"{played_move} is a strong move in this position."
        )

    if quality == "good":
        return (
            f"{played_move} is a good move in this position."
        )

    if quality == "inaccuracy":
        return (
            f"{played_move} is slightly inaccurate in this position. "
            "The move is playable, but a stronger continuation was available."
        )

    if quality == "mistake":
        return (
            f"{played_move} is a mistake in this position. "
            "It allows the opponent to improve their position or "
            "creates a concrete positional or tactical problem."
        )

    if quality == "blunder":
        return (
            f"{played_move} is a bad move in this position. "
            "It causes a significant deterioration in the position."
        )

    return ""


# ==========================================================
# MAIN EXPLANATION FUNCTION
# ==========================================================

def explain_move(
    before,
    after,
    move,
    played_move,
    best_move=None,
    pv=None,
    evaluation_before=None,
    evaluation_after=None,
    quality=None,
):
    """
    Generate a position-aware explanation for the played move.

    Stockfish provides:
        - evaluation
        - best move
        - principal variation

    This module converts those engine results and board facts
    into human-readable coaching.

    The quality verdict is calculated here so that the function
    does not depend on the order of calculations in
    analysis_service.py.
    """

    # ------------------------------------------------------
    # Calculate quality if it was not explicitly supplied
    # ------------------------------------------------------

    if quality is None:
        quality = calculate_move_quality(
            before,
            after,
            evaluation_before,
            evaluation_after
        )

    # ------------------------------------------------------
    # Convert Stockfish best move UCI -> SAN
    # ------------------------------------------------------

    best_move_san = convert_uci_to_san(
        before,
        best_move
    )

    # ------------------------------------------------------
    # Convert Stockfish PV UCI -> SAN
    # ------------------------------------------------------

    pv_san = convert_pv_to_san(
        before,
        pv
    )

    # ======================================================
    # CHECKMATE
    # ======================================================

    if after.is_checkmate():

        result = explain_checkmate(
            before,
            after,
            move,
            played_move,
            best_move_san
        )

        return add_quality_to_result(
            result,
            played_move,
            quality
        )

    # ======================================================
    # CASTLING
    # ======================================================

    if before.is_castling(move):

        result = explain_castling(
            before,
            after,
            move,
            played_move,
            best_move_san
        )

        return add_quality_to_result(
            result,
            played_move,
            quality
        )

    # ======================================================
    # PROMOTION
    # ======================================================

    if move.promotion:

        result = explain_promotion(
            before,
            after,
            move,
            played_move,
            best_move_san
        )

        return add_quality_to_result(
            result,
            played_move,
            quality
        )

    # ======================================================
    # CAPTURE
    # ======================================================

    if before.is_capture(move):

        result = explain_capture(
            before,
            after,
            move,
            played_move,
            best_move_san
        )

        return add_quality_to_result(
            result,
            played_move,
            quality
        )

    # ======================================================
    # CHECK
    # ======================================================

    if after.is_check():

        result = explain_check(
            before,
            after,
            move,
            played_move,
            best_move_san,
            pv_san
        )

        return add_quality_to_result(
            result,
            played_move,
            quality
        )

    # ======================================================
    # PAWN MOVE
    # ======================================================

    moving_piece = before.piece_at(
        move.from_square
    )

    if (
        moving_piece
        and moving_piece.piece_type == chess.PAWN
    ):

        result = explain_pawn_move(
            before,
            after,
            move,
            played_move,
            best_move_san,
            quality
        )

        return add_quality_to_result(
            result,
            played_move,
            quality
        )

    # ======================================================
    # PIECE MOVE
    # ======================================================

    if moving_piece:

        result = explain_piece_move(
            before,
            after,
            move,
            played_move,
            best_move_san,
            quality
        )

        return add_quality_to_result(
            result,
            played_move,
            quality
        )

    # ======================================================
    # FALLBACK
    # ======================================================

    result = explain_general_move(
        before,
        after,
        move,
        played_move,
        best_move_san,
        pv_san
    )

    return add_quality_to_result(
        result,
        played_move,
        quality
    )


# ==========================================================
# ADD QUALITY TO RESULT
# ==========================================================
def add_quality_to_result(
    result,
    played_move,
    quality
):
    verdict = quality_verdict(
        played_move,
        quality
    )

    if verdict:
        result["explanation"] = (
            f"{verdict} {result['explanation']}"
        )

    if quality not in ("inaccuracy", "mistake", "blunder"):
        result["recommendation"] = None

    return result


# ==========================================================
# UCI -> SAN
# ==========================================================

def convert_uci_to_san(
    board,
    uci_move
):
    """
    Convert a Stockfish UCI move into SAN.

    Examples:
        g1f3 -> Nf3
        e2e4 -> e4
        e1g1 -> O-O
        f7f8q -> f8=Q
    """

    if not uci_move:
        return None

    try:

        move = chess.Move.from_uci(
            uci_move
        )

        if move not in board.legal_moves:
            return uci_move

        return board.san(move)

    except Exception:
        return uci_move


# ==========================================================
# PV UCI -> SAN
# ==========================================================

def convert_pv_to_san(
    board,
    pv
):
    """
    Convert Stockfish principal variation from UCI to SAN.
    """

    if not pv:
        return []

    result = []

    temp_board = board.copy()

    for uci_move in pv:

        try:

            move = chess.Move.from_uci(
                uci_move
            )

            if move not in temp_board.legal_moves:

                result.append(
                    uci_move
                )

                break

            san = temp_board.san(
                move
            )

            result.append(
                san
            )

            temp_board.push(
                move
            )

        except Exception:

            result.append(
                uci_move
            )

            break

    return result


# ==========================================================
# CHECKMATE
# ==========================================================

def explain_checkmate(
    before,
    after,
    move,
    played_move,
    best_move_san
):

    explanation = (
        f"{played_move} delivers checkmate. "
        "The opposing king has no legal way to escape the check."
    )

    if best_move_san == played_move:

        recommendation = (
            f"Stockfish recommends {best_move_san}. "
            "The move immediately ends the game, so there is "
            "no stronger continuation."
        )

    elif best_move_san:

        recommendation = (
            f"Stockfish also identified {best_move_san} as its "
            "engine continuation, but the played move already "
            "finishes the game with checkmate."
        )

    else:

        recommendation = (
            "The played move already ends the game with checkmate."
        )

    return {
        "explanation": explanation,
        "recommendation": recommendation
    }


# ==========================================================
# CASTLING
# ==========================================================

def explain_castling(
    before,
    after,
    move,
    played_move,
    best_move_san
):

    if chess.square_file(
        move.to_square
    ) > chess.square_file(
        move.from_square
    ):

        side = "kingside"

    else:

        side = "queenside"

    explanation = (
        f"{played_move} castles {side}, moving the king toward "
        "safety and bringing the rook into a more active position."
    )

    recommendation = recommendation_text(
        before,
        after,
        played_move,
        best_move_san
    )

    return {
        "explanation": explanation,
        "recommendation": recommendation
    }


# ==========================================================
# PROMOTION
# ==========================================================

def explain_promotion(
    before,
    after,
    move,
    played_move,
    best_move_san
):

    promoted_piece = PIECE_NAMES.get(
        move.promotion,
        "piece"
    )

    explanation = (
        f"{played_move} promotes the pawn to a {promoted_piece}, "
        "creating a new major piece and significantly changing "
        "the material balance."
    )

    recommendation = recommendation_text(
        before,
        after,
        played_move,
        best_move_san
    )

    return {
        "explanation": explanation,
        "recommendation": recommendation
    }


# ==========================================================
# CAPTURE
# ==========================================================

def explain_capture(
    before,
    after,
    move,
    played_move,
    best_move_san
):

    captured_piece = get_captured_piece(
        before,
        move
    )

    moving_piece = before.piece_at(
        move.from_square
    )

    if captured_piece:

        captured_name = PIECE_NAMES[
            captured_piece.piece_type
        ]

        captured_value = PIECE_VALUES[
            captured_piece.piece_type
        ]

    else:

        captured_name = "piece"
        captured_value = 0

    moving_name = (
        PIECE_NAMES[moving_piece.piece_type]
        if moving_piece
        else "piece"
    )

    if captured_piece:

        if captured_value == 1:
            material_text = "1 point of material"
        else:
            material_text = (
                f"{captured_value} points of material"
            )

        explanation = (
            f"{played_move} uses the {moving_name} to capture "
            f"the opponent's {captured_name}, gaining "
            f"{material_text}."
        )

    else:

        explanation = (
            f"{played_move} captures an opposing piece and "
            "changes the material balance."
        )

    # ------------------------------------------------------
    # Is the capturing piece attacked?
    # ------------------------------------------------------

    destination = move.to_square

    if moving_piece:

        attackers = after.attackers(
            not moving_piece.color,
            destination
        )

        if attackers:

            attacker_names = []

            for square in attackers:

                attacker = after.piece_at(
                    square
                )

                if attacker:

                    attacker_names.append(
                        PIECE_NAMES[
                            attacker.piece_type
                        ]
                    )

            if attacker_names:

                names = ", ".join(
                    sorted(
                        set(attacker_names)
                    )
                )

                explanation += (
                    f" However, the {moving_name} on "
                    f"{chess.square_name(destination)} "
                    f"is attacked by the opponent's {names}, "
                    "so the resulting position should be checked carefully."
                )

    recommendation = recommendation_text(
        before,
        after,
        played_move,
        best_move_san
    )

    return {
        "explanation": explanation,
        "recommendation": recommendation
    }


# ==========================================================
# CHECK
# ==========================================================

def explain_check(
    before,
    after,
    move,
    played_move,
    best_move_san,
    pv_san
):

    moving_piece = before.piece_at(
        move.from_square
    )

    if moving_piece:

        piece_name = PIECE_NAMES[
            moving_piece.piece_type
        ]

    else:

        piece_name = "piece"

    explanation = (
        f"{played_move} gives check, forcing the opponent "
        f"to respond to the {piece_name}'s attack on the king."
    )

    if pv_san and len(pv_san) >= 2:

        continuation = " ".join(
            pv_san[:4]
        )

        explanation += (
            f" The engine continuation begins with "
            f"{continuation}."
        )

    recommendation = recommendation_text(
        before,
        after,
        played_move,
        best_move_san
    )

    return {
        "explanation": explanation,
        "recommendation": recommendation
    }


# ==========================================================
# PAWN MOVE
# ==========================================================

def explain_pawn_move(
    before,
    after,
    move,
    played_move,
    best_move_san,
    quality
):
    """
    Explain pawn moves using concrete board characteristics.

    The function distinguishes:
        - central expansion
        - space gain
        - pawn support
        - opening/closing lines
        - attacks on pieces
        - weaknesses created by the pawn move
        - opponent counterplay
    """

    from_square = move.from_square
    to_square = move.to_square

    from_file = chess.square_file(
        from_square
    )

    to_file = chess.square_file(
        to_square
    )

    from_rank = chess.square_rank(
        from_square
    )

    to_rank = chess.square_rank(
        to_square
    )

    destination = chess.square_name(
        to_square
    )

    pawn = before.piece_at(
        from_square
    )

    explanation_parts = []

    # ------------------------------------------------------
    # Determine whether this is a central pawn
    # ------------------------------------------------------

    is_central = to_file in (2, 3, 4, 5)

    is_d_or_e_pawn = to_file in (3, 4)

    reaches_center = to_square in (
        chess.C4,
        chess.D4,
        chess.E4,
        chess.F4,
        chess.C5,
        chess.D5,
        chess.E5,
        chess.F5,
    )

    # ------------------------------------------------------
    # Central pawn explanation
    # ------------------------------------------------------

    if is_d_or_e_pawn or reaches_center:

        controlled = pawn_controlled_squares(
            after,
            to_square
        )

        if quality in ("best", "good"):

            explanation_parts.append(
                f"{played_move} is useful because the pawn "
                "claims space in the center and helps control "
                "important central squares."
            )

        elif quality == "inaccuracy":

            explanation_parts.append(
                f"{played_move} gains central space, but in this "
                "position the pawn advance gives up some flexibility "
                "or allows a stronger opposing plan."
            )

        elif quality in ("mistake", "blunder"):

            explanation_parts.append(
                f"{played_move} changes the center, but here the "
                "pawn advance creates a concrete problem and gives "
                "the opponent a useful way to challenge the position."
            )

        else:

            explanation_parts.append(
                f"{played_move} advances a central pawn and changes "
                "the structure of the position."
            )

        if controlled:

            explanation_parts.append(
                f"The pawn now controls "
                f"{format_square_list(controlled)}."
            )

    # ------------------------------------------------------
    # Flank pawn
    # ------------------------------------------------------

    else:

        if quality in ("best", "good"):

            explanation_parts.append(
                f"{played_move} advances the pawn on the "
                f"{destination[0]}-file, gaining space and "
                "changing the structure on that side of the board."
            )

        elif quality == "inaccuracy":

            explanation_parts.append(
                f"{played_move} is playable, but the pawn advance "
                "commits the structure before the position requires it."
            )

        elif quality in ("mistake", "blunder"):

            explanation_parts.append(
                f"{played_move} creates a pawn commitment that is "
                "unfavorable in this position and gives the opponent "
                "useful targets or counterplay."
            )

        else:

            explanation_parts.append(
                f"{played_move} advances the pawn and changes the "
                "pawn structure."
            )

    # ------------------------------------------------------
    # Pawn support
    # ------------------------------------------------------

    supporters = []

    for square in after.attackers(
        pawn.color if pawn else before.turn,
        to_square
    ):

        piece = after.piece_at(
            square
        )

        if piece and piece.piece_type != chess.PAWN:

            supporters.append(
                PIECE_NAMES[
                    piece.piece_type
                ]
            )

    if supporters:

        unique_supporters = sorted(
            set(supporters)
        )

        explanation_parts.append(
            f"The pawn is supported by the "
            f"{format_piece_list(unique_supporters)}, "
            "which makes the advance easier to maintain."
        )

    # ------------------------------------------------------
    # Detect lines opened by the pawn move
    # ------------------------------------------------------

    opened_files = detect_opened_files(
        before,
        after
    )

    if opened_files:

        explanation_parts.append(
            f"The advance also opens the "
            f"{format_file_list(opened_files)}, "
            "which can give rooks or queens new lines."
        )

    # ------------------------------------------------------
    # Detect attacks created by the pawn
    # ------------------------------------------------------

    attacks = pawn_controlled_squares(
        after,
        to_square
    )

    attacked_enemy_pieces = []

    for square_name in attacks:

        square = chess.parse_square(
            square_name
        )

        piece = after.piece_at(
            square
        )

        if piece and piece.color != pawn.color:

            attacked_enemy_pieces.append(
                PIECE_NAMES[
                    piece.piece_type
                ]
            )

    if attacked_enemy_pieces:

        names = sorted(
            set(attacked_enemy_pieces)
        )

        explanation_parts.append(
            f"The pawn also puts pressure on the "
            f"{format_piece_list(names)}."
        )

    # ------------------------------------------------------
    # Detect pawn weaknesses
    # ------------------------------------------------------

    weaknesses = detect_pawn_weaknesses(
        after,
        pawn.color if pawn else before.turn,
        to_square
    )

    if weaknesses:

        explanation_parts.append(
            f"The move also leaves "
            f"{format_square_list(weaknesses)} "
            "as potential targets."
        )

    explanation = " ".join(
        explanation_parts
    )

    recommendation = recommendation_text(
        before,
        after,
        played_move,
        best_move_san
    )

    return {
        "explanation": explanation,
        "recommendation": recommendation
    }


# ==========================================================
# PIECE MOVE
# ==========================================================

def explain_piece_move(
    before,
    after,
    move,
    played_move,
    best_move_san,
    quality
):

    piece = before.piece_at(
        move.from_square
    )

    if piece is None:

        return explain_general_move(
            before,
            after,
            move,
            played_move,
            best_move_san,
            []
        )

    piece_name = PIECE_NAMES[
        piece.piece_type
    ]

    destination = chess.square_name(
        move.to_square
    )

    explanation_parts = []

    # ======================================================
    # KNIGHT
    # ======================================================

    if piece.piece_type == chess.KNIGHT:

        attacks = attacked_square_names(
            after,
            move.to_square
        )

        if move.from_square in (
            chess.B1,
            chess.G1,
            chess.B8,
            chess.G8,
        ):

            explanation_parts.append(
                f"{played_move} develops the knight from "
                "its starting square, bringing a new piece "
                "into the game and increasing control of "
                "important central squares."
            )

        else:

            explanation_parts.append(
                f"{played_move} moves the knight to "
                f"{destination}, improving or changing its activity."
            )

        if attacks:

            explanation_parts.append(
                f"The knight now attacks "
                f"{format_square_list(attacks)}."
            )

    # ======================================================
    # BISHOP
    # ======================================================

    elif piece.piece_type == chess.BISHOP:

        explanation_parts.append(
            f"{played_move} develops the bishop to "
            f"{destination}, activating its diagonal."
        )

        attacks = attacked_square_names(
            after,
            move.to_square
        )

        if attacks:

            explanation_parts.append(
                f"From there, the bishop influences "
                f"{format_square_list(attacks)}."
            )

        target = get_bishop_target(
            after,
            move.to_square
        )

        if target:

            explanation_parts.append(
                f"It also puts pressure on {target}."
            )

        if destination in ("g7", "b7", "g2", "b2"):

            explanation_parts.append(
                "The bishop can become especially active along "
                "the long diagonal, increasing pressure toward "
                "the center and the opponent's king side."
            )

    # ======================================================
    # ROOK
    # ======================================================

    elif piece.piece_type == chess.ROOK:

        file_index = chess.square_file(
            move.to_square
        )

        file_name = chess.square_name(
            move.to_square
        )[0]

        if is_open_file(
            after,
            file_index
        ):

            explanation_parts.append(
                f"{played_move} activates the rook on the "
                f"open {file_name}-file, giving it a clear "
                "line for pressure and penetration."
            )

        elif is_semi_open_file(
            after,
            file_index,
            piece.color
        ):

            explanation_parts.append(
                f"{played_move} places the rook on the "
                f"semi-open {file_name}-file, allowing it "
                "to pressure the opposing pawn structure."
            )

        else:

            explanation_parts.append(
                f"{played_move} improves the rook's activity "
                f"by moving it to {destination}."
            )

    # ======================================================
    # QUEEN
    # ======================================================

    elif piece.piece_type == chess.QUEEN:

        explanation_parts.append(
            f"{played_move} moves the queen to "
            f"{destination}, changing the lines and targets "
            "the queen can influence."
        )

        if move.from_square in (
            chess.D1,
            chess.D8
        ):

            explanation_parts.append(
                "Moving the queen also frees the starting square "
                "and can help coordinate the remaining pieces."
            )

    # ======================================================
    # KING
    # ======================================================

    elif piece.piece_type == chess.KING:

        explanation_parts.append(
            f"{played_move} moves the king to "
            f"{destination}, changing its safety and "
            "control of nearby squares."
        )

    # ======================================================
    # GENERAL PIECE
    # ======================================================

    else:

        explanation_parts.append(
            f"{played_move} moves the {piece_name} to "
            f"{destination}, changing its activity and "
            "coordination."
        )

    # ------------------------------------------------------
    # Detect whether destination is attacked
    # ------------------------------------------------------

    opponent_attackers = after.attackers(
        not piece.color,
        move.to_square
    )

    if opponent_attackers:

        attacker_names = []

        for square in opponent_attackers:

            attacker = after.piece_at(
                square
            )

            if attacker:

                attacker_names.append(
                    PIECE_NAMES[
                        attacker.piece_type
                    ]
                )

        if attacker_names:

            names = sorted(
                set(attacker_names)
            )

            explanation_parts.append(
                f"The {piece_name} on {destination} is "
                f"also attacked by the opponent's "
                f"{format_piece_list(names)}, so its safety "
                "should be considered."
            )

    explanation = " ".join(
        explanation_parts
    )

    recommendation = recommendation_text(
        before,
        after,
        played_move,
        best_move_san
    )

    return {
        "explanation": explanation,
        "recommendation": recommendation
    }


# ==========================================================
# GENERAL MOVE
# ==========================================================

def explain_general_move(
    before,
    after,
    move,
    played_move,
    best_move_san,
    pv_san
):

    explanation = (
        f"{played_move} changes the position by "
        "improving the placement or coordination of the "
        "moving piece."
    )

    if pv_san:

        continuation = " ".join(
            pv_san[:4]
        )

        explanation += (
            f" The engine continuation begins with "
            f"{continuation}."
        )

    recommendation = recommendation_text(
        before,
        after,
        played_move,
        best_move_san
    )

    return {
        "explanation": explanation,
        "recommendation": recommendation
    }


# ==========================================================
# RECOMMENDATION
# ==========================================================

def recommendation_text(
    before,
    after,
    played_move,
    best_move_san
):
    """
    Explain the purpose of the engine's recommended move.

    This is intentionally separate from the explanation of
    the move that the user actually played.
    """

    if not best_move_san:

        return (
            "Stockfish did not provide a replacement move."
        )

    # ------------------------------------------------------
    # Played move is already best
    # ------------------------------------------------------

    if played_move == best_move_san:

        idea = describe_move_idea(
            before,
            after,
            best_move_san
        )

        if idea:

            return (
                f"Stockfish recommends {best_move_san}. "
                f"The idea is to {idea}."
            )

        return (
            f"Stockfish recommends {best_move_san}, "
            "so the move played matches the engine's "
            "strongest continuation."
        )

    # ------------------------------------------------------
    # Different engine recommendation
    # ------------------------------------------------------

    idea = describe_move_idea(
        before,
        after,
        best_move_san
    )

    if idea:

        return (
            f"Stockfish recommends {best_move_san}. "
            f"The idea is to {idea}. "
            f"This gives the position a clearer continuation "
            f"than {played_move}."
        )

    return (
        f"Stockfish recommends {best_move_san} instead of "
        f"{played_move}. The recommended move provides the "
        "engine's stronger continuation in this position."
    )


# ==========================================================
# DESCRIBE ENGINE MOVE IDEA
# ==========================================================

def describe_move_idea(
    before,
    after,
    best_move_san
):
    """
    Explain the chess idea behind the engine's recommended move.
    """

    if not best_move_san:
        return ""

    try:

        best_move = before.parse_san(
            best_move_san
        )

    except Exception:

        return ""

    piece = before.piece_at(
        best_move.from_square
    )

    if piece is None:
        return ""

    destination = chess.square_name(
        best_move.to_square
    )

    piece_name = PIECE_NAMES[
        piece.piece_type
    ]

    # ======================================================
    # CASTLING
    # ======================================================

    if before.is_castling(best_move):

        return (
            "improve king safety and connect the rook to the game"
        )

    # ======================================================
    # PAWN
    # ======================================================

    if piece.piece_type == chess.PAWN:

        ideas = []

        to_file = chess.square_file(
            best_move.to_square
        )

        if to_file in (3, 4):

            ideas.append(
                "strengthen control of the center"
            )

        elif to_file in (2, 5):

            ideas.append(
                "gain useful space and influence the position on that side"
            )

        else:

            ideas.append(
                "improve the pawn structure or gain useful space"
            )

        controlled = pawn_controlled_squares(
            after,
            best_move.to_square
        )

        if controlled:

            ideas.append(
                f"control {format_square_list(controlled)}"
            )

        opened_files = detect_opened_files(
            before,
            after
        )

        if opened_files:

            ideas.append(
                f"open the {format_file_list(opened_files)} for the pieces"
            )

        return combine_ideas(
            ideas
        )

    # ======================================================
    # KNIGHT
    # ======================================================

    if piece.piece_type == chess.KNIGHT:

        ideas = [
            "develop the knight",
            "improve piece activity",
        ]

        if best_move.from_square in (
            chess.B1,
            chess.G1,
            chess.B8,
            chess.G8,
        ):

            ideas.append(
                "increase control of important central squares"
            )

        attacks = attacked_square_names(
            after,
            best_move.to_square
        )

        if attacks:

            ideas.append(
                f"control {format_square_list(attacks)}"
            )

        return combine_ideas(
            ideas
        )

    # ======================================================
    # BISHOP
    # ======================================================

    if piece.piece_type == chess.BISHOP:

        ideas = [
            "develop the bishop",
            "activate its diagonal",
        ]

        if destination in (
            "g7",
            "b7",
            "g2",
            "b2"
        ):

            ideas.append(
                "increase pressure along the long diagonal"
            )

        target = get_bishop_target(
            after,
            best_move.to_square
        )

        if target:

            ideas.append(
                f"put pressure on {target}"
            )

        if (
            destination in ("g7", "b7")
            and not before.has_castling_rights(
                piece.color
            ) is False
        ):

            ideas.append(
                "prepare or support king safety"
            )

        return combine_ideas(
            ideas
        )

    # ======================================================
    # ROOK
    # ======================================================

    if piece.piece_type == chess.ROOK:

        file_index = chess.square_file(
            best_move.to_square
        )

        file_name = chess.square_name(
            best_move.to_square
        )[0]

        if is_open_file(
            after,
            file_index
        ):

            return (
                f"activate the rook on the open {file_name}-file "
                "and increase pressure along it"
            )

        if is_semi_open_file(
            after,
            file_index,
            piece.color
        ):

            return (
                f"place the rook on the semi-open {file_name}-file "
                "to pressure the opposing pawn structure"
            )

        return (
            f"improve the rook's activity on {destination} "
            "and improve coordination"
        )

    # ======================================================
    # QUEEN
    # ======================================================

    if piece.piece_type == chess.QUEEN:

        attacks = attacked_square_names(
            after,
            best_move.to_square
        )

        if attacks:

            return (
                f"improve the queen's activity and increase "
                f"pressure on {format_square_list(attacks)}"
            )

        return (
            f"improve the queen's activity and coordination "
            f"from {destination}"
        )

    # ======================================================
    # KING
    # ======================================================

    if piece.piece_type == chess.KING:

        return (
            "improve the king's safety or centralize the king "
            "for the next phase of the game"
        )

    # ======================================================
    # FALLBACK
    # ======================================================

    return (
        f"improve the {piece_name}'s activity and coordination "
        f"from {destination}"
    )


# ==========================================================
# COMBINE IDEAS
# ==========================================================

def combine_ideas(
    ideas
):

    cleaned = []

    for idea in ideas:

        if idea and idea not in cleaned:

            cleaned.append(
                idea
            )

    if not cleaned:
        return ""

    if len(cleaned) == 1:

        return cleaned[0]

    if len(cleaned) == 2:

        return (
            f"{cleaned[0]} and {cleaned[1]}"
        )

    return (
        ", ".join(cleaned[:-1])
        + ", and "
        + cleaned[-1]
    )


# ==========================================================
# CAPTURED PIECE
# ==========================================================

def get_captured_piece(
    board,
    move
):

    # ------------------------------------------------------
    # Normal capture
    # ------------------------------------------------------

    captured_piece = board.piece_at(
        move.to_square
    )

    if captured_piece:

        return captured_piece

    # ------------------------------------------------------
    # En passant
    # ------------------------------------------------------

    if board.is_en_passant(
        move
    ):

        captured_square = chess.square(
            chess.square_file(
                move.to_square
            ),
            chess.square_rank(
                move.from_square
            )
        )

        return board.piece_at(
            captured_square
        )

    return None


# ==========================================================
# PAWN CONTROLLED SQUARES
# ==========================================================

def pawn_controlled_squares(
    board,
    pawn_square
):
    """
    Return squares controlled by the pawn on pawn_square.
    """

    pawn = board.piece_at(
        pawn_square
    )

    if pawn is None:
        return []

    if pawn.piece_type != chess.PAWN:
        return []

    result = []

    attacks = board.attacks(
        pawn_square
    )

    for square in attacks:

        result.append(
            chess.square_name(square)
        )

    return result


# ==========================================================
# ATTACKED SQUARE NAMES
# ==========================================================

def attacked_square_names(
    board,
    square
):

    attacks = board.attacks(
        square
    )

    result = []

    for target in attacks:

        result.append(
            chess.square_name(target)
        )

    return result


# ==========================================================
# BISHOP TARGET
# ==========================================================

def get_bishop_target(
    board,
    bishop_square
):

    bishop = board.piece_at(
        bishop_square
    )

    if bishop is None:
        return None

    if bishop.piece_type != chess.BISHOP:
        return None

    color = bishop.color

    targets = [
        chess.F7,
        chess.F2,
        chess.H7,
        chess.H2,
        chess.B7,
        chess.B2,
    ]

    for target in targets:

        if board.is_attacked_by(
            color,
            target
        ):

            return chess.square_name(
                target
            )

    return None


# ==========================================================
# OPEN FILE
# ==========================================================

def is_open_file(
    board,
    file_index
):

    for rank in range(8):

        square = chess.square(
            file_index,
            rank
        )

        piece = board.piece_at(
            square
        )

        if (
            piece
            and piece.piece_type == chess.PAWN
        ):

            return False

    return True


# ==========================================================
# SEMI-OPEN FILE
# ==========================================================

def is_semi_open_file(
    board,
    file_index,
    rook_color
):

    own_pawn = False
    enemy_pawn = False

    for rank in range(8):

        square = chess.square(
            file_index,
            rank
        )

        piece = board.piece_at(
            square
        )

        if (
            piece
            and piece.piece_type == chess.PAWN
        ):

            if piece.color == rook_color:

                own_pawn = True

            else:

                enemy_pawn = True

    return (
        not own_pawn
        and enemy_pawn
    )


# ==========================================================
# DETECT OPENED FILES
# ==========================================================

def detect_opened_files(
    before,
    after
):

    opened = []

    for file_index in range(8):

        was_open = is_open_file(
            before,
            file_index
        )

        is_open = is_open_file(
            after,
            file_index
        )

        if not was_open and is_open:

            opened.append(
                chr(
                    ord("a")
                    + file_index
                )
                + "-file"
            )

    return opened


# ==========================================================
# DETECT PAWN WEAKNESSES
# ==========================================================

def detect_pawn_weaknesses(
    board,
    color,
    moved_square
):
    """
    Detect simple pawn weaknesses created or exposed by
    the pawn structure.

    This is deliberately conservative. It does not claim
    that every isolated or backward pawn is automatically bad.
    """

    weaknesses = []

    moved_file = chess.square_file(
        moved_square
    )

    # ------------------------------------------------------
    # Check adjacent files
    # ------------------------------------------------------

    for file_index in (
        moved_file - 1,
        moved_file + 1
    ):

        if file_index < 0 or file_index > 7:
            continue

        has_supporting_pawn = False

        for rank in range(8):

            square = chess.square(
                file_index,
                rank
            )

            piece = board.piece_at(
                square
            )

            if (
                piece
                and piece.color == color
                and piece.piece_type == chess.PAWN
            ):

                has_supporting_pawn = True
                break

        if not has_supporting_pawn:

            square = chess.square(
                moved_file,
                chess.square_rank(
                    moved_square
                )
            )

            weaknesses.append(
                chess.square_name(square)
            )

    return sorted(
        set(weaknesses)
    )


# ==========================================================
# FORMAT SQUARE LIST
# ==========================================================

def format_square_list(
    squares
):

    if not squares:
        return ""

    if len(squares) == 1:

        return squares[0]

    if len(squares) == 2:

        return (
            f"{squares[0]} and {squares[1]}"
        )

    return (
        ", ".join(
            squares[:-1]
        )
        + ", and "
        + squares[-1]
    )


# ==========================================================
# FORMAT PIECE LIST
# ==========================================================

def format_piece_list(
    pieces
):

    if not pieces:
        return ""

    if len(pieces) == 1:

        return pieces[0]

    if len(pieces) == 2:

        return (
            f"{pieces[0]} and {pieces[1]}"
        )

    return (
        ", ".join(
            pieces[:-1]
        )
        + ", and "
        + pieces[-1]
    )


# ==========================================================
# FORMAT FILE LIST
# ==========================================================

def format_file_list(
    files
):

    if not files:
        return ""

    if len(files) == 1:

        return files[0]

    if len(files) == 2:

        return (
            f"{files[0]} and {files[1]}"
        )

    return (
        ", ".join(
            files[:-1]
        )
        + ", and "
        + files[-1]
    )