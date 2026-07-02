import chess

# ----------------------------------------
# Center squares
# ----------------------------------------
CENTER_SQUARES = {
    chess.D4,
    chess.E4,
    chess.D5,
    chess.E5
}

# ----------------------------------------
# Count material
# ----------------------------------------
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9
}


def material_count(board, color):
    score = 0

    for piece_type, value in PIECE_VALUES.items():
        score += len(board.pieces(piece_type, color)) * value

    return score


# ----------------------------------------
# Material imbalance
# ----------------------------------------
def material_difference(board):
    white = material_count(board, chess.WHITE)
    black = material_count(board, chess.BLACK)
    return abs(white - black)


# ----------------------------------------
# Is move a capture?
# ----------------------------------------
def is_capture(board, move):
    return board.is_capture(move)


# ----------------------------------------
# Is move a check?
# ----------------------------------------
def gives_check(board, move):
    board.push(move)
    check = board.is_check()
    board.pop()
    return check


# ----------------------------------------
# Is castling?
# ----------------------------------------
def is_castle(board, move):
    return board.is_castling(move)


# ----------------------------------------
# Controls center?
# ----------------------------------------
def controls_center(move):
    return move.to_square in CENTER_SQUARES


# ----------------------------------------
# Piece development
# ----------------------------------------
def is_development(board, move):

    piece = board.piece_at(move.from_square)

    if piece is None:
        return False

    if piece.piece_type == chess.KNIGHT:
        return move.from_square in [
            chess.B1,
            chess.G1,
            chess.B8,
            chess.G8
        ]

    if piece.piece_type == chess.BISHOP:
        return move.from_square in [
            chess.C1,
            chess.F1,
            chess.C8,
            chess.F8
        ]

    return False


# ----------------------------------------
# Queen activity
# ----------------------------------------
def queen_move(board, move):

    piece = board.piece_at(move.from_square)

    return (
        piece is not None and
        piece.piece_type == chess.QUEEN
    )


# ----------------------------------------
# Rook activity
# ----------------------------------------
def rook_move(board, move):

    piece = board.piece_at(move.from_square)

    return (
        piece is not None and
        piece.piece_type == chess.ROOK
    )


# ----------------------------------------
# Pawn move
# ----------------------------------------
def pawn_move(board, move):

    piece = board.piece_at(move.from_square)

    return (
        piece is not None and
        piece.piece_type == chess.PAWN
    )


# ----------------------------------------
# Enemy king zone
# (8 surrounding squares)
# ----------------------------------------
def king_zone(board, color):

    king = board.king(color)

    if king is None:
        return []

    zone = []

    file = chess.square_file(king)
    rank = chess.square_rank(king)

    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):

            nf = file + df
            nr = rank + dr

            if 0 <= nf <= 7 and 0 <= nr <= 7:
                zone.append(chess.square(nf, nr))

    return zone


# ----------------------------------------
# Move attacks king zone?
# ----------------------------------------
def attacks_king_zone(board, move):

    board.push(move)

    attacker = not board.turn

    enemy = board.turn

    zone = king_zone(board, enemy)

    attacked = False

    for sq in zone:
        if board.is_attacked_by(attacker, sq):
            attacked = True
            break

    board.pop()

    return attacked