import chess

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 100
}

# Directions
ROOK_DIRECTIONS = [
    (1,0),(-1,0),(0,1),(0,-1)
]

BISHOP_DIRECTIONS = [
    (1,1),(1,-1),(-1,1),(-1,-1)
]

QUEEN_DIRECTIONS = ROOK_DIRECTIONS + BISHOP_DIRECTIONS

# Board helpers
def inside_board(file, rank):
    return 0 <= file <= 7 and 0 <= rank <= 7

def next_square(square, direction):
    file = chess.square_file(square) + direction[0]
    rank = chess.square_rank(square) + direction[1]
    if not inside_board(file, rank):
        return None
    return chess.square(file, rank)

# Piece directions
def piece_directions(piece_type):
    if piece_type == chess.ROOK:
        return ROOK_DIRECTIONS
    if piece_type == chess.BISHOP:
        return BISHOP_DIRECTIONS
    if piece_type == chess.QUEEN:
        return QUEEN_DIRECTIONS
    return []

# Ray scanning
def scan_ray(board, start_square, direction):
    occupied = []
    square = next_square(start_square, direction)

    while square is not None:
        piece = board.piece_at(square)

        if piece:
            occupied.append((square, piece))

        square = next_square(square, direction)

    return occupied

def scan_piece_rays(board, square):
    piece = board.piece_at(square)

    if piece is None:
        return {}

    result = {}

    for direction in piece_directions(piece.piece_type):
        result[direction] = scan_ray(
            board,
            square,
            direction
        )

    return result

# Piece checks
def enemy_piece(piece, color):
    return piece is not None and piece.color != color

def friendly_piece(piece, color):
    return piece is not None and piece.color == color

def valuable_piece(piece):
    return piece is not None and piece.piece_type != chess.PAWN

def strong_piece(piece):
    return piece is not None and piece.piece_type in (
        chess.ROOK,
        chess.QUEEN,
        chess.KING
    )

def piece_value(piece):
    if piece is None:
        return 0

    return PIECE_VALUES[piece.piece_type]

# Tactical captures
def count_tactical_captures(board, moves):
    total = 0

    for move in moves:
        temp = board.copy()

        if not temp.is_capture(move):
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

    return total

# Hanging captures
def count_hanging_captures(board, moves):
    total = 0

    for move in moves:
        temp = board.copy()

        if not temp.is_capture(move):
            continue

        victim = temp.piece_at(
            move.to_square
        )

        if victim is None:
            continue

        defenders = temp.attackers(
            victim.color,
            move.to_square
        )

        if len(defenders) == 0:
            total += 1

    return total

# Winning exchanges
def count_winning_exchanges(board, moves):
    total = 0

    for move in moves:
        temp = board.copy()

        if not temp.is_capture(move):
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

    return total

# Discovered checks
def count_discovered_checks(board,moves):
    total=0

    for move in moves:
        temp=board.copy()

        if not temp.is_legal(move):
            continue

        mover=temp.piece_at(move.from_square)

        if mover is None:
            continue

        enemy=not mover.color

        temp.push(move)

        if temp.is_check():
            king=temp.king(enemy)

            if king:
                attackers=temp.attackers(
                    mover.color,
                    king
                )

                if len(attackers)>=2:
                    total+=1

    return total


# Double checks
def count_double_checks(board,moves):
    total=0

    for move in moves:
        temp=board.copy()

        if not temp.is_legal(move):
            continue

        mover=temp.piece_at(
            move.from_square
        )

        if mover is None:
            continue

        enemy=not mover.color

        temp.push(move)

        if temp.is_check():

            king=temp.king(enemy)

            if king:

                attackers=temp.attackers(
                    mover.color,
                    king
                )

                if len(attackers)>=2:
                    total+=1

    return total


# Material winning combinations
def count_material_winning_combinations(board,moves):
    total=0

    for move in moves:

        temp=board.copy()

        if not temp.is_legal(move):
            continue

        if not temp.is_capture(move):
            continue

        attacker=temp.piece_at(
            move.from_square
        )

        victim=temp.piece_at(
            move.to_square
        )

        if attacker and victim:

            gain=(
                piece_value(victim)
                -
                piece_value(attacker)
            )

            if gain>=3:
                total+=1

    return total


# Tactical summary
def tactical_summary(board,moves):

    return {

        "tactical_captures":
            count_tactical_captures(
                board,
                moves
            ),

        "hanging_captures":
            count_hanging_captures(
                board,
                moves
            ),

        "winning_exchanges":
            count_winning_exchanges(
                board,
                moves
            ),

        "discovered_checks":
            count_discovered_checks(
                board,
                moves
            ),

        "double_checks":
            count_double_checks(
                board,
                moves
            ),

        "material_winning_combinations":
            count_material_winning_combinations(
                board,
                moves
            )
    }


# Coaching tactical analysis
def analyze_tactical(board,moves):

    summary=tactical_summary(
        board,
        moves
    )

    score=sum(summary.values())

    return {

        **summary,

        "score":score

    }