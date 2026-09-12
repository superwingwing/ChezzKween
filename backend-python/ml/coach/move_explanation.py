import chess

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
):
    """
    Generate a specific chess explanation for the played move.

    Stockfish is responsible for:
        - evaluation
        - best move
        - principal variation

    This module converts those engine results and board facts
    into human-readable coaching text.
    """

    # ------------------------------------------------------
    # Convert Stockfish best move from UCI -> SAN
    # ------------------------------------------------------

    best_move_san = convert_uci_to_san(
        before,
        best_move
    )

    # ------------------------------------------------------
    # Convert Stockfish PV from UCI -> SAN
    # ------------------------------------------------------

    pv_san = convert_pv_to_san(
        before,
        pv
    )

    # ======================================================
    # 1. CHECKMATE
    # ======================================================

    if after.is_checkmate():
        return explain_checkmate(
            before,
            after,
            played_move,
            best_move_san
        )

    # ======================================================
    # 2. CASTLING
    # ======================================================

    if before.is_castling(move):
        return explain_castling(
            before,
            after,
            played_move,
            best_move_san
        )

    # ======================================================
    # 3. PROMOTION
    # ======================================================

    if move.promotion:
        return explain_promotion(
            before,
            after,
            move,
            played_move,
            best_move_san
        )

    # ======================================================
    # 4. CAPTURE
    # ======================================================

    if before.is_capture(move):
        return explain_capture(
            before,
            after,
            move,
            played_move,
            best_move_san
        )

    # ======================================================
    # 5. CHECK
    # ======================================================

    if after.is_check():
        return explain_check(
            before,
            after,
            move,
            played_move,
            best_move_san,
            pv_san
        )

    # ======================================================
    # 6. PAWN MOVE
    # ======================================================

    moving_piece = before.piece_at(move.from_square)

    if moving_piece and moving_piece.piece_type == chess.PAWN:
        return explain_pawn_move(
            before,
            after,
            move,
            played_move,
            best_move_san
        )

    # ======================================================
    # 7. PIECE MOVE
    # ======================================================

    if moving_piece:
        return explain_piece_move(
            before,
            after,
            move,
            played_move,
            best_move_san
        )

    # ======================================================
    # 8. FALLBACK
    # ======================================================

    return explain_general_move(
        before,
        after,
        move,
        played_move,
        best_move_san,
        pv_san
    )


# ==========================================================
# UCI -> SAN
# ==========================================================

def convert_uci_to_san(board, uci_move):
    """
    Convert a Stockfish UCI move into professional SAN.

    Example:
        g1f3 -> Nf3
        e2e4 -> e4
        e1g1 -> O-O
        f7f8q -> f8=Q
    """

    if not uci_move:
        return None

    try:
        move = chess.Move.from_uci(uci_move)

        if move not in board.legal_moves:
            return uci_move

        return board.san(move)

    except Exception:
        return uci_move


# ==========================================================
# PV UCI -> SAN
# ==========================================================

def convert_pv_to_san(board, pv):
    """
    Convert an entire Stockfish PV from UCI to SAN.

    Example:
        ["e2e4", "e7e5", "g1f3"]

    becomes:

        ["e4", "e5", "Nf3"]
    """

    if not pv:
        return []

    result = []
    temp_board = board.copy()

    for uci_move in pv:

        try:
            move = chess.Move.from_uci(uci_move)
            if move not in temp_board.legal_moves:
                result.append(uci_move)
                break
            san = temp_board.san(move)
            result.append(san)
            temp_board.push(move)

        except Exception:
            result.append(uci_move)
            break

    return result


# ==========================================================
# CHECKMATE
# ==========================================================

def explain_checkmate(
    before,
    after,
    played_move,
    best_move_san
):

    explanation = (
        f"{played_move} delivers checkmate. "
        "The opposing king has no legal move, "
        "cannot capture the attacking piece, "
        "and cannot block the check."
    )

    if best_move_san == played_move:
        recommendation = (
            f"Stockfish agrees with {played_move}; "
            "this is the strongest continuation because it "
            "ends the game immediately."
        )
    else:
        recommendation = (
            f"{played_move} finishes the game immediately. "
            "There is no stronger practical continuation than checkmate."
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
    played_move,
    best_move_san
):

    if played_move in ("O-O", "0-0"):
        side = "kingside"

    else:
        side = "queenside"

    explanation = (
        f"{played_move} castles {side}, moving the king to a safer "
        "position while connecting the rook to the game."
    )

    if best_move_san == played_move:
        recommendation = (
            f"Stockfish also recommends {played_move}, "
            "confirming that castling is the strongest move."
        )
    elif best_move_san:
        recommendation = (
            f"Stockfish prefers {best_move_san}, "
            f"which should be considered before choosing {played_move}."
        )
    else:
        recommendation = (
            "The move improves king safety and rook activity."
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
        "creating a major material advantage and advancing the "
        "position toward a decisive result."
    )

    if best_move_san == played_move:
        recommendation = (
            f"Stockfish agrees with {played_move}; "
            "promotion is the strongest continuation."
        )
    elif best_move_san:
        recommendation = (
            f"Stockfish prefers {best_move_san}, "
            f"so compare that continuation with {played_move}."
        )
    else:
        recommendation = (
            "Promotion creates a new major piece and is usually the "
            "critical continuation in this position."
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

    if captured_piece is None:
        captured_name = "piece"

    else:
        captured_name = PIECE_NAMES[
            captured_piece.piece_type
        ]

    moving_name = (
        PIECE_NAMES[moving_piece.piece_type]
        if moving_piece
        else "piece"
    )

    captured_value = (
        PIECE_VALUES[captured_piece.piece_type]
        if captured_piece
        else 0
    )

    # ------------------------------------------------------
    # Basic capture explanation
    # ------------------------------------------------------

    if captured_piece:

        explanation = (
            f"{played_move} uses the {moving_name} to capture "
            f"the opponent's {captured_name}, gaining "
            f"{captured_value} point"
        )

        if captured_value != 1:
            explanation += "s"

        explanation += " of material."

    else:

        explanation = (
            f"{played_move} captures an opposing piece "
            "and changes the material balance."
        )

    # ------------------------------------------------------
    # Check whether the capturing piece is immediately
    # attacked after the capture
    # ------------------------------------------------------

    destination = move.to_square

    attackers = after.attackers(
        not moving_piece.color,
        destination
    )

    if attackers:

        attacker_names = []

        for square in attackers:

            piece = after.piece_at(square)

            if piece:
                attacker_names.append(
                    PIECE_NAMES[piece.piece_type]
                )

        if attacker_names:

            names = ", ".join(
                sorted(set(attacker_names))
            )

            explanation += (
                f" However, the {moving_name} on "
                f"{chess.square_name(destination)} "
                f"is now attacked by the opponent's "
                f"{names}."
            )

    # ------------------------------------------------------
    # Recommendation
    # ------------------------------------------------------

    recommendation = recommendation_text(
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

    # ------------------------------------------------------
    # Show Stockfish continuation when available
    # ------------------------------------------------------

    if pv_san and len(pv_san) >= 2:

        continuation = " ".join(
            pv_san[:4]
        )

        explanation += (
            f" Stockfish's continuation is {continuation}."
        )

    recommendation = recommendation_text(
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
    best_move_san
):

    from_file = chess.square_file(
        move.from_square
    )

    to_file = chess.square_file(
        move.to_square
    )

    from_rank = chess.square_rank(
        move.from_square
    )

    to_rank = chess.square_rank(
        move.to_square
    )

    # ------------------------------------------------------
    # Center pawn
    # ------------------------------------------------------

    if move.to_square in (
        chess.D4,
        chess.E4,
        chess.D5,
        chess.E5,
    ):

        controlled = attacked_square_names(
            after,
            move.to_square
        )

        explanation = (
            f"{played_move} advances a central pawn and "
            "strengthens control of the center."
        )

        if controlled:

            explanation += (
                f" The pawn also helps control "
                f"{format_square_list(controlled)}."
            )

    # ------------------------------------------------------
    # Pawn attacks center
    # ------------------------------------------------------

    elif to_file in (3, 4):

        explanation = (
            f"{played_move} advances the pawn toward the center, "
            "helping gain space and influence important central squares."
        )

    # ------------------------------------------------------
    # Pawn advance
    # ------------------------------------------------------

    else:

        explanation = (
            f"{played_move} advances the pawn and changes the "
            "structure of the position."
        )

    recommendation = recommendation_text(
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
    best_move_san
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

    # ======================================================
    # KNIGHT
    # ======================================================

    if piece.piece_type == chess.KNIGHT:

        attacks = attacked_square_names(
            after,
            move.to_square
        )

        explanation = (
            f"{played_move} develops the knight to "
            f"{destination}, improving its activity."
        )

        if attacks:

            explanation += (
                f" From there, the knight attacks "
                f"{format_square_list(attacks)}."
            )

        # If knight moves from starting rank
        if move.from_square in (
            chess.B1,
            chess.G1,
            chess.B8,
            chess.G8,
        ):

            explanation = (
                f"{played_move} develops the knight from "
                f"its starting square, bringing a new piece "
                "into the game and increasing control of "
                "important central squares."
            )

            if attacks:

                explanation += (
                    f" The knight now attacks "
                    f"{format_square_list(attacks)}."
                )

    # ======================================================
    # BISHOP
    # ======================================================

    elif piece.piece_type == chess.BISHOP:

        explanation = (
            f"{played_move} develops the bishop to "
            f"{destination}, activating its diagonal."
        )

        attacks = attacked_square_names(
            after,
            move.to_square
        )

        if attacks:

            explanation += (
                f" The bishop now influences "
                f"{format_square_list(attacks)}."
            )

        # Common attacking targets
        target = get_bishop_target(
            after,
            move.to_square
        )

        if target:

            explanation += (
                f" This also puts pressure on "
                f"{target}."
            )

    # ======================================================
    # ROOK
    # ======================================================

    elif piece.piece_type == chess.ROOK:

        file_name = chess.square_file(
            move.to_square
        )

        rank_name = chess.square_rank(
            move.to_square
        )

        if is_open_file(
            after,
            file_name
        ):

            explanation = (
                f"{played_move} activates the rook on an "
                "open file, allowing it to pressure "
                "squares along the file."
            )

        elif is_semi_open_file(
            after,
            file_name,
            piece.color
        ):

            explanation = (
                f"{played_move} places the rook on a "
                "semi-open file, giving it useful pressure "
                "against the opposing position."
            )

        else:

            explanation = (
                f"{played_move} improves the rook's activity "
                f"by moving it to {destination}."
            )

    # ======================================================
    # QUEEN
    # ======================================================

    elif piece.piece_type == chess.QUEEN:

        explanation = (
            f"{played_move} moves the queen to "
            f"{destination}, changing its activity and "
            "the pressure it can apply to the position."
        )

    # ======================================================
    # KING
    # ======================================================

    elif piece.piece_type == chess.KING:

        explanation = (
            f"{played_move} moves the king to "
            f"{destination}, changing the king's position "
            "and its influence over nearby squares."
        )

    # ======================================================
    # GENERAL PIECE
    # ======================================================

    else:

        explanation = (
            f"{played_move} develops the {piece_name} to "
            f"{destination}, improving its position."
        )

    recommendation = recommendation_text(
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
        f"{played_move} changes the position by improving "
        "the placement of the moving piece."
    )

    if pv_san:

        continuation = " ".join(
            pv_san[:4]
        )

        explanation += (
            f" Stockfish's principal variation begins "
            f"with {continuation}."
        )

    recommendation = recommendation_text(
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
    played_move,
    best_move_san
):

    if not best_move_san:

        return (
            "Stockfish did not provide a replacement move."
        )

    # ------------------------------------------------------
    # Played move is Stockfish's best move
    # ------------------------------------------------------

    if played_move == best_move_san:

        return (
            f"Stockfish recommends {best_move_san}, "
            "so the move played matches the engine's "
            "strongest continuation."
        )

    # ------------------------------------------------------
    # Different move
    # ------------------------------------------------------

    return (
        f"Stockfish prefers {best_move_san} "
        f"instead of {played_move}. "
        f"Consider {best_move_san} as the stronger "
        "continuation in this position."
    )


# ==========================================================
# CAPTURED PIECE
# ==========================================================

def get_captured_piece(
    board,
    move
):

    # Normal capture
    captured_piece = board.piece_at(
        move.to_square
    )

    if captured_piece:
        return captured_piece

    # En passant
    if board.is_en_passant(move):

        captured_square = chess.square(
            chess.square_file(move.to_square),
            chess.square_rank(move.from_square)
        )

        return board.piece_at(
            captured_square
        )

    return None


# ==========================================================
# ATTACKED SQUARES
# ==========================================================

def attacked_square_names(
    board,
    square
):

    attacks = board.attacks(square)

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

        piece = board.piece_at(square)

        if piece and piece.piece_type == chess.PAWN:

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

        piece = board.piece_at(square)

        if piece and piece.piece_type == chess.PAWN:

            if piece.color == rook_color:
                own_pawn = True
            else:
                enemy_pawn = True

    return not own_pawn and enemy_pawn


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
        return f"{squares[0]} and {squares[1]}"

    return (
        ", ".join(squares[:-1])
        + ", and "
        + squares[-1]
    )