import chess


def analyze_move(board: chess.Board, move: chess.Move):
    """
    Analyze a move BEFORE board.push(move)
    Returns facts that will later be converted into explanations.
    """

    analysis = {}

    # -------------------------
    # Basic Move Info
    # -------------------------

    analysis["move"] = board.san(move)

    piece = board.piece_at(move.from_square)

    if piece:
        analysis["piece"] = chess.piece_name(piece.piece_type)
        analysis["color"] = "White" if piece.color else "Black"
    else:
        analysis["piece"] = None
        analysis["color"] = None

    # -------------------------
    # Tactical Events
    # -------------------------

    analysis["capture"] = board.is_capture(move)
    analysis["castle"] = board.is_castling(move)
    analysis["en_passant"] = board.is_en_passant(move)
    analysis["promotion"] = move.promotion is not None

    analysis["check"] = board.gives_check(move)

    # -------------------------
    # Before / After Position
    # -------------------------

    before_fen = board.fen()

    board.push(move)

    after_fen = board.fen()

    analysis["before_fen"] = before_fen
    analysis["after_fen"] = after_fen

    # Is opponent currently in checkmate?

    analysis["checkmate"] = board.is_checkmate()

    # Is position drawn?

    analysis["stalemate"] = board.is_stalemate()

    analysis["insufficient_material"] = (
        board.is_insufficient_material()
    )

    board.pop()

    return analysis