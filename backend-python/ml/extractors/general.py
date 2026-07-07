# ==========================================
# general.py
#
# General helper functions for feature
# extraction.
#
# Thesis:
# Chess Playing Style Classification
#
# Author: Your Name
# ==========================================

import chess

# ==========================================
# Piece Values
# ==========================================

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}


# ==========================================
# Center Squares
# ==========================================

CENTER = {
    chess.D4,
    chess.E4,
    chess.D5,
    chess.E5
}

EXTENDED_CENTER = {
    chess.C3, chess.D3, chess.E3, chess.F3,
    chess.C4, chess.D4, chess.E4, chess.F4,
    chess.C5, chess.D5, chess.E5, chess.F5,
    chess.C6, chess.D6, chess.E6, chess.F6
}


# ==========================================
# Piece Helpers
# ==========================================

def piece_value(piece):

    if piece is None:
        return 0

    return PIECE_VALUES.get(piece.piece_type, 0)


def is_minor_piece(piece):

    return (
        piece is not None
        and piece.piece_type in (
            chess.KNIGHT,
            chess.BISHOP
        )
    )


def is_major_piece(piece):

    return (
        piece is not None
        and piece.piece_type in (
            chess.ROOK,
            chess.QUEEN
        )
    )


# ==========================================
# Material
# ==========================================

def material_value(board, color):

    total = 0

    for piece_type, value in PIECE_VALUES.items():

        total += len(board.pieces(piece_type, color)) * value

    return total


def material_balance(board):

    return (
        material_value(board, chess.WHITE)
        -
        material_value(board, chess.BLACK)
    )


# ==========================================
# Check Detection
# ==========================================

def gives_check(board, move):

    board.push(move)

    result = board.is_check()

    board.pop()

    return result


# ==========================================
# Castling
# ==========================================

def is_castle(board, move):

    return board.is_castling(move)


# ==========================================
# Development
# ==========================================

def is_development(board, move):

    piece = board.piece_at(move.from_square)

    if piece is None:
        return False

    if piece.color == chess.WHITE:

        return (
            (piece.piece_type == chess.KNIGHT and move.from_square in (chess.B1, chess.G1))
            or
            (piece.piece_type == chess.BISHOP and move.from_square in (chess.C1, chess.F1))
        )

    return (
        (piece.piece_type == chess.KNIGHT and move.from_square in (chess.B8, chess.G8))
        or
        (piece.piece_type == chess.BISHOP and move.from_square in (chess.C8, chess.F8))
    )


# ==========================================
# Pawn Move
# ==========================================

def is_pawn_move(board, move):

    piece = board.piece_at(move.from_square)

    return (
        piece is not None
        and piece.piece_type == chess.PAWN
    )


# ==========================================
# Center Control
# ==========================================

def controls_center(move):

    return move.to_square in CENTER


def controls_extended_center(move):

    return move.to_square in EXTENDED_CENTER


# ==========================================
# Queen / Rook Activity
# ==========================================

def is_queen_move(board, move):

    piece = board.piece_at(move.from_square)

    return (
        piece is not None
        and piece.piece_type == chess.QUEEN
    )


def is_rook_move(board, move):

    piece = board.piece_at(move.from_square)

    return (
        piece is not None
        and piece.piece_type == chess.ROOK
    )


# ==========================================
# Capture Value
#
# Supports En Passant
# ==========================================

def capture_value(board, move):

    if not board.is_capture(move):
        return 0

    if board.is_en_passant(move):
        return PIECE_VALUES[chess.PAWN]

    captured = board.piece_at(move.to_square)

    if captured is None:
        return 0

    return piece_value(captured)


# ==========================================
# Mobility
# ==========================================

def mobility(board):

    return board.legal_moves.count()


# ==========================================
# King Zone
# ==========================================

def king_zone(board, color):

    king = board.king(color)

    if king is None:
        return set()

    zone = set()

    rank = chess.square_rank(king)
    file = chess.square_file(king)

    for dr in (-1, 0, 1):

        for df in (-1, 0, 1):

            if dr == 0 and df == 0:
                continue

            r = rank + dr
            f = file + df

            if 0 <= r <= 7 and 0 <= f <= 7:

                zone.add(
                    chess.square(f, r)
                )

    return zone


# ==========================================
# King Attack
#
# Returns True if the moved piece attacks
# any square surrounding the enemy king.
# ==========================================

def attacks_enemy_king_zone(board, move):

    moving_piece = board.piece_at(move.from_square)

    if moving_piece is None:
        return False

    enemy = not moving_piece.color

    zone = king_zone(board, enemy)

    board.push(move)

    attacks = board.attacks(move.to_square)

    board.pop()

    return len(attacks & zone) > 0


# ==========================================
# Game Phase
# ==========================================

def game_phase(fullmove_number):

    if fullmove_number <= 20:
        return "opening"

    if fullmove_number <= 60:
        return "middlegame"

    return "endgame"