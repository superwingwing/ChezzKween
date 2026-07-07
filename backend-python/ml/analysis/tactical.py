import chess

# Piece Values
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 100
}

# Sliding Directions
ROOK_DIRECTIONS = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
]

BISHOP_DIRECTIONS = [
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1)
]

QUEEN_DIRECTIONS = (
    ROOK_DIRECTIONS +
    BISHOP_DIRECTIONS
)

# Board Helpers
def inside_board(file, rank):
    """
    True if coordinates
    are inside chess board.
    """

    return (
        0 <= file <= 7
        and
        0 <= rank <= 7
    )


def next_square(square, direction):
    """
    Returns next square
    in given direction.

    Returns None if outside board.
    """

    file = chess.square_file(square)
    rank = chess.square_rank(square)

    file += direction[0]
    rank += direction[1]

    if not inside_board(file, rank):
        return None

    return chess.square(file, rank)

# ==========================================
# Piece Direction
# ==========================================

def piece_directions(piece_type):
    """
    Sliding directions
    for piece.
    """

    if piece_type == chess.ROOK:
        return ROOK_DIRECTIONS

    if piece_type == chess.BISHOP:
        return BISHOP_DIRECTIONS

    if piece_type == chess.QUEEN:
        return QUEEN_DIRECTIONS

    return []

# ==========================================
# Ray Scanner
# ==========================================

def scan_ray(
    board,
    start_square,
    direction
):
    """
    Walks one ray.

    Returns every occupied
    square encountered
    in order.

    This is the heart of
    tactical detection.
    """

    occupied = []

    square = next_square(
        start_square,
        direction
    )

    while square is not None:

        piece = board.piece_at(square)

        if piece is not None:

            occupied.append(
                (
                    square,
                    piece
                )
            )

        square = next_square(
            square,
            direction
        )

    return occupied

# ==========================================
# Scan All Rays
# ==========================================

def scan_piece_rays(
    board,
    square
):
    """
    Scans every legal ray
    of rook, bishop,
    queen.

    Returns dictionary

    direction ->
    occupied pieces
    """

    piece = board.piece_at(square)

    if piece is None:
        return {}

    directions = piece_directions(
        piece.piece_type
    )

    result = {}

    for direction in directions:

        result[direction] = scan_ray(
            board,
            square,
            direction
        )

    return result

# ==========================================
# Enemy Pieces
# ==========================================

def enemy_piece(piece, color):

    return (
        piece is not None
        and
        piece.color != color
    )

# ==========================================
# Friendly Pieces
# ==========================================

def friendly_piece(piece, color):

    return (
        piece is not None
        and
        piece.color == color
    )

# ==========================================
# Valuable Piece
# ==========================================

def valuable_piece(piece):

    if piece is None:
        return False

    return (
        piece.piece_type
        != chess.PAWN
    )

# ==========================================
# Strong Piece
# ==========================================

def strong_piece(piece):

    if piece is None:
        return False

    return piece.piece_type in (

        chess.ROOK,

        chess.QUEEN,

        chess.KING

    )

# ==========================================
# Piece Value
# ==========================================

def piece_value(piece):

    if piece is None:
        return 0

    return PIECE_VALUES[
        piece.piece_type
    ]

# ==========================================
# Tactical Captures
# ==========================================

def count_tactical_captures(board, moves):
    """
    Counts captures that win
    at least equal material.

    Returns
    -------
    int
    """

    total = 0

    temp = board.copy()

    for move in moves:

        if not temp.is_capture(move):

            temp.push(move)
            continue

        attacker = temp.piece_at(
            move.from_square
        )

        victim = temp.piece_at(
            move.to_square
        )

        if attacker and victim:

            if piece_value(victim) >= piece_value(attacker):

                total += 1

        temp.push(move)

    return total


# ==========================================
# Hanging Piece Captures
# ==========================================

def count_hanging_captures(board, moves):
    """
    Counts captures of
    undefended pieces.
    """

    total = 0

    temp = board.copy()

    for move in moves:

        if not temp.is_capture(move):

            temp.push(move)
            continue

        victim = temp.piece_at(
            move.to_square
        )

        if victim is None:

            temp.push(move)
            continue

        defenders = temp.attackers(

            victim.color,

            move.to_square

        )

        if len(defenders) == 0:

            total += 1

        temp.push(move)

    return total


# ==========================================
# Winning Exchanges
# ==========================================

def count_winning_exchanges(board, moves):
    """
    Counts exchanges where
    lower value captures
    higher value.

    Example

    Knight takes Queen
    """

    total = 0

    temp = board.copy()

    for move in moves:

        if not temp.is_capture(move):

            temp.push(move)
            continue

        attacker = temp.piece_at(
            move.from_square
        )

        victim = temp.piece_at(
            move.to_square
        )

        if attacker and victim:

            if piece_value(victim) > piece_value(attacker):

                total += 1

        temp.push(move)

    return total

# ==========================================
# Discovered Checks
# ==========================================

def count_discovered_checks(board, moves):
    """
    Counts discovered checks.

    A discovered check occurs when
    a move uncovers an attack on
    the enemy king by another piece.
    """

    total = 0

    temp = board.copy()

    for move in moves:

        mover = temp.piece_at(move.from_square)

        if mover is None:
            temp.push(move)
            continue

        enemy = not mover.color

        temp.push(move)

        if temp.is_check():

            king = temp.king(enemy)

            attackers = temp.attackers(
                mover.color,
                king
            )

            if len(attackers) >= 2:
                total += 1

        temp.pop()
        temp.push(move)

    return total


# ==========================================
# Double Checks
# ==========================================

def count_double_checks(board, moves):
    """
    Counts double checks.

    A double check happens when
    two different pieces attack
    the enemy king after one move.
    """

    total = 0

    temp = board.copy()

    for move in moves:

        mover = temp.piece_at(move.from_square)

        if mover is None:
            temp.push(move)
            continue

        enemy = not mover.color

        temp.push(move)

        if temp.is_check():

            king = temp.king(enemy)

            attackers = temp.attackers(
                mover.color,
                king
            )

            if len(attackers) >= 2:

                total += 1

        temp.pop()
        temp.push(move)

    return total


# ==========================================
# Material Winning Combinations
# ==========================================

def count_material_winning_combinations(board, moves):
    """
    Counts moves that immediately
    gain significant material.

    Threshold:
        Gain of 3 or more points.
    """

    total = 0

    temp = board.copy()

    for move in moves:

        if not temp.is_capture(move):

            temp.push(move)
            continue

        attacker = temp.piece_at(
            move.from_square
        )

        victim = temp.piece_at(
            move.to_square
        )

        if attacker and victim:

            gain = (

                piece_value(victim)

                -

                piece_value(attacker)

            )

            if gain >= 3:

                total += 1

        temp.push(move)

    return total


# ==========================================
# Tactical Summary
# ==========================================

def tactical_summary(board, moves):
    """
    Returns all tactical
    features in one dictionary.
    """

    return {

        "tactical_captures":
            count_tactical_captures(board, moves),

        "hanging_captures":
            count_hanging_captures(board, moves),

        "winning_exchanges":
            count_winning_exchanges(board, moves),

        "discovered_checks":
            count_discovered_checks(board, moves),

        "double_checks":
            count_double_checks(board, moves),

        "material_winning_combinations":
            count_material_winning_combinations(
                board,
                moves
            )

    }