import chess

def is_passed_pawn(
    board: chess.Board,
    square: chess.Square,
    color: chess.Color
):
    """
    Standard chess definition.

    A pawn is passed if no enemy pawn
    exists on the same file or adjacent
    files ahead of it.
    """

    piece = board.piece_at(square)

    if piece is None:
        return False
    if piece.piece_type != chess.PAWN:
        return False
    if piece.color != color:
        return False
    
    file = chess.square_file(square)
    rank = chess.square_rank(square)
    enemy = not color
    files = []

    if file > 0:
        files.append(file - 1)

    files.append(file)

    if file < 7:
        files.append(file + 1)

    for f in files:
        if color == chess.WHITE:
            ranks = range(rank + 1, 8)
        else:
            ranks = range(rank - 1, -1, -1)
        for r in ranks:
            sq = chess.square(f, r)
            p = board.piece_at(sq)
            if (
                p is not None
                and
                p.color == enemy
                and
                p.piece_type == chess.PAWN
            ):
                return False
    return True

# Count Passed Pawns

def passed_pawns(
    board: chess.Board,
    color: chess.Color
):

    total = 0
    for pawn in board.pieces(
        chess.PAWN,
        color
    ):

        if is_passed_pawn(
            board,
            pawn,
            color
        ):
            total += 1
    return total

# Isolated Pawn
def is_isolated_pawn(
    board: chess.Board,
    square: chess.Square,
    color: chess.Color
):

    """
    Standard definition.

    No friendly pawn exists
    on adjacent files.
    """

    file = chess.square_file(square)

    adjacent = []

    if file > 0:
        adjacent.append(file - 1)
    if file < 7:
        adjacent.append(file + 1)
    for pawn in board.pieces(
        chess.PAWN,
        color
    ):
        if chess.square_file(pawn) in adjacent:
            return False
    return True

# Count Isolated Pawns

def isolated_pawns(
    board: chess.Board,
    color: chess.Color
):
    total = 0
    for pawn in board.pieces(
        chess.PAWN,
        color
    ):

        if is_isolated_pawn(
            board,
            pawn,
            color
        ):
            total += 1
    return total

# Doubled Pawns
def doubled_pawns(
    board: chess.Board,
    color: chess.Color
):

    """
    Counts extra pawns
    sharing a file.
    Example
    2 pawns on file = 1 doubled pawn
    3 pawns = 2 doubled pawns
    """
    total = 0

    for file in range(8):
        count = 0
        for pawn in board.pieces(
            chess.PAWN,
            color
        ):
            if chess.square_file(pawn) == file:
                count += 1
        if count >= 2:
            total += count - 1
    return total

# Pawn Support
def pawn_supporters(
    board: chess.Board,
    square: chess.Square,
    color: chess.Color
):
    """
    Returns the number of friendly pawns
    supporting this pawn.
    White pawn support:
        one rank behind diagonally
    Black pawn support:
        one rank ahead diagonally
    """
    file = chess.square_file(square)
    rank = chess.square_rank(square)

    supporters = 0
    if color == chess.WHITE:
        support_rank = rank - 1
    else:
        support_rank = rank + 1
    if 0 <= support_rank <= 7:
        for df in (-1, 1):
            f = file + df
            if 0 <= f <= 7:
                sq = chess.square(f, support_rank)
                piece = board.piece_at(sq)
                if (
                    piece is not None
                    and piece.color == color
                    and piece.piece_type == chess.PAWN
                ):
                    supporters += 1
    return supporters


# Connected Pawn
def is_connected_pawn(
    board: chess.Board,
    square: chess.Square,
    color: chess.Color
):
    """
    True if this pawn is supported
    by another friendly pawn.
    """

    return pawn_supporters(
        board,
        square,
        color
    ) > 0


# Pawn Chain Count

def pawn_chain_count(
    board: chess.Board,
    color: chess.Color
):
    """
    Counts pawns belonging
    to pawn chains.
    """
    total = 0
    for pawn in board.pieces(
        chess.PAWN,
        color
    ):
        if is_connected_pawn(
            board,
            pawn,
            color
        ):
            total += 1
    return total


# Pawn Structure Score
def pawn_structure_score(
    board: chess.Board,
    color: chess.Color
):
    """
    Overall pawn structure quality.
    Higher is better.
    Formula:
        + Passed pawns
        + Connected pawns
        - Isolated pawns
        - Doubled pawns
    """
    score = 0
    score += (
        passed_pawns(
            board,
            color
        ) * 3
    )

    score += (
        pawn_chain_count(
            board,
            color
        ) * 2
    )

    score -= (
        isolated_pawns(
            board,
            color
        ) * 2
    )

    score -= (
        doubled_pawns(
            board,
            color
        ) * 2
    )

    return score


# Testing

if __name__ == "__main__":
    board = chess.Board()
    print(
        "White Passed:",
        passed_pawns(board, chess.WHITE)
    )
    print(
        "White Isolated:",
        isolated_pawns(board, chess.WHITE)
    )
    print(
        "White Doubled:",
        doubled_pawns(board, chess.WHITE)
    )
    print(
        "White Chains:",
        pawn_chain_count(board, chess.WHITE)
    )

    print(
        "White Pawn Score:",
        pawn_structure_score(board, chess.WHITE)
    )