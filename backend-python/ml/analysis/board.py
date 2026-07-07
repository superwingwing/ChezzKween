import chess

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

# Open File
def is_open_file(board, file_index):
    """
    No pawns on file.
    """
    for rank in range(8):
        piece = board.piece_at(
            chess.square(file_index, rank)
        )
        if piece and piece.piece_type == chess.PAWN:
            return False
    return True

# Semi Open Fil
def is_semi_open_file(
    board,
    file_index,
    color
):

    """
    No friendly pawns
    but enemy pawn exists.
    """
    friendly = False
    enemy = False
    for rank in range(8):
        piece = board.piece_at(
            chess.square(file_index, rank)
        )
        if piece is None:
            continue
        if piece.piece_type != chess.PAWN:
            continue
        if piece.color == color:
            friendly = True
        else:
            enemy = True
    return (not friendly) and enemy

# Open Files Toward King
def open_files_to_king(
    board,
    color
):

    """
    Counts open/semi-open files
    adjacent to the king.
    """

    king = board.king(color)

    if king is None:
        return 0

    file = chess.square_file(king)

    total = 0

    for f in [

        file - 1,

        file,

        file + 1

    ]:

        if not (0 <= f <= 7):
            continue

        if is_open_file(board, f):

            total += 1

    return total


# ==========================================
# Center Control
# ==========================================

def center_control(
    board,
    color
):

    """
    Number of center squares
    attacked by player.
    """

    score = 0

    for square in CENTER:

        if board.is_attacked_by(
            color,
            square
        ):

            score += 1

    return score

# Extended Center
def extended_center_control(
    board,
    color
):

    score = 0

    for square in EXTENDED_CENTER:

        if board.is_attacked_by(
            color,
            square
        ):

            score += 1

    return score


# ==========================================
# Space Advantage
# ==========================================

def space_advantage(
    board,
    color
):

    """
    Number of controlled squares
    inside enemy territory.
    """

    total = 0

    for square in chess.SQUARES:

        rank = chess.square_rank(square)

        if color == chess.WHITE:

            if rank < 4:
                continue

        else:

            if rank > 3:
                continue

        if board.is_attacked_by(
            color,
            square
        ):

            total += 1

    return total


# ==========================================
# Occupied Open Files
# ==========================================

def rook_on_open_file(
    board,
    color
):

    """
    Counts rooks occupying
    open files.
    """

    total = 0

    for rook in board.pieces(
        chess.ROOK,
        color
    ):

        file = chess.square_file(
            rook
        )

        if is_open_file(
            board,
            file
        ):

            total += 1

    return total


# ==========================================
# Queen on Open File
# ==========================================

def queen_on_open_file(
    board,
    color
):

    queens = board.pieces(
        chess.QUEEN,
        color
    )

    total = 0

    for queen in queens:

        file = chess.square_file(
            queen
        )

        if is_open_file(
            board,
            file
        ):

            total += 1

    return total


# ==========================================
# Testing
# ==========================================

if __name__ == "__main__":

    board = chess.Board()

    print(center_control(board, chess.WHITE))

    print(space_advantage(board, chess.WHITE))

    print(open_files_to_king(board, chess.BLACK))


# ==========================================
# Open / Semi-open Files Toward Enemy King
# ==========================================

def count_open_files_to_enemy_king(board):
    """
    Counts the number of open or semi-open
    files around BOTH kings.

    Used as an aggressive feature.

    Returns
    -------
    int
    """

    total = 0

    for color in (chess.WHITE, chess.BLACK):

        king_square = board.king(color)

        if king_square is None:
            continue

        king_file = chess.square_file(
            king_square
        )

        attacker = not color

        for file in [

            king_file - 1,

            king_file,

            king_file + 1

        ]:

            if file < 0 or file > 7:
                continue

            if is_open_file(board, file):

                total += 1

            elif is_semi_open_file(

                board,

                file,

                attacker

            ):

                total += 1

    return total