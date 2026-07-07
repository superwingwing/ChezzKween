# ==========================================
# material.py
#
# Material Analysis
#
# Thesis:
# Chess Playing Style Classification
#
# Provides reusable material evaluation
# functions for all feature extractors.
#
# FINAL VERSION (Streaming Architecture)
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
# Piece Value
# ==========================================

def piece_value(piece_type: int) -> int:
    """
    Returns the standard material value.
    """
    return PIECE_VALUES.get(piece_type, 0)


# ==========================================
# Material Count
# ==========================================

def material_count(board: chess.Board, color: chess.Color) -> int:
    """
    Total material owned by one player.
    """

    total = 0

    for piece_type, value in PIECE_VALUES.items():

        total += len(board.pieces(piece_type, color)) * value

    return total


# ==========================================
# Material Balance
# ==========================================

def material_balance(board: chess.Board) -> int:
    """
    Positive = White ahead

    Negative = Black ahead
    """

    return (
        material_count(board, chess.WHITE)
        -
        material_count(board, chess.BLACK)
    )


# ==========================================
# Material Difference
# ==========================================

def material_difference(
    before: chess.Board,
    after: chess.Board,
    color: chess.Color
) -> int:
    """
    Material difference after a move.
    """

    return (
        material_count(after, color)
        -
        material_count(before, color)
    )


# ==========================================
# Bishop Pair
# ==========================================

def has_bishop_pair(
    board: chess.Board,
    color: chess.Color
) -> bool:

    return len(board.pieces(chess.BISHOP, color)) >= 2


# ==========================================
# Major Pieces
# ==========================================

def major_piece_count(
    board: chess.Board,
    color: chess.Color
) -> int:

    return (

        len(board.pieces(chess.ROOK, color))

        +

        len(board.pieces(chess.QUEEN, color))

    )


# ==========================================
# Minor Pieces
# ==========================================

def minor_piece_count(
    board: chess.Board,
    color: chess.Color
) -> int:

    return (

        len(board.pieces(chess.KNIGHT, color))

        +

        len(board.pieces(chess.BISHOP, color))

    )


# ==========================================
# Sacrifice Detection
# ==========================================

def is_sacrifice(
    board: chess.Board,
    move: chess.Move
) -> bool:
    """
    Streaming sacrifice detection.

    Returns True if the player gives away
    material worth at least 3 points.

    This function is called BEFORE board.push(move).
    """

    piece = board.piece_at(move.from_square)

    if piece is None:
        return False

    # Ignore captures.
    # Captures are usually exchanges,
    # not sacrifices.

    if board.is_capture(move):
        return False

    before = material_count(
        board,
        piece.color
    )

    temp = board.copy()

    temp.push(move)

    after = material_count(
        temp,
        piece.color
    )

    material_loss = before - after

    return material_loss >= 3


# ==========================================
# Testing
# ==========================================

if __name__ == "__main__":

    board = chess.Board()

    print("White Material:", material_count(board, chess.WHITE))
    print("Black Material:", material_count(board, chess.BLACK))
    print("Balance:", material_balance(board))
    print("White Bishop Pair:", has_bishop_pair(board, chess.WHITE))