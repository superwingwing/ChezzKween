import chess

def king_square(board: chess.Board, color: chess.Color):
    """
    Returns the square occupied
    by the specified king.
    """
    return board.king(color)


# King Zone

def king_zone(board: chess.Board, color: chess.Color):
    """
    Returns all squares surrounding
    the king including the king square.
    Used for king attack analysis.
    """
    king = board.king(color)
    if king is None:
        return set()
    zone = {king}
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


# Count Attackers

def count_attackers(
    board: chess.Board,
    color: chess.Color,
    square: chess.Square
):
    """
    Number of pieces of 'color'
    attacking the square.
    """
    return len(
        board.attackers(
            color,
            square
        )
    )

# Count Defenders
def count_defenders(
    board: chess.Board,
    color: chess.Color,
    square: chess.Square
):

    """
    Alias for readability.
    Number of defending pieces.
    """
    return count_attackers(
        board,
        color,
        square
    )

# Total King Attackers
def king_attackers(
    board: chess.Board,
    attacking_color: chess.Color
):

    """
    Counts how many DISTINCT attacking pieces
    attack any square in the enemy king zone.
    """
    enemy = not attacking_color
    zone = king_zone(board, enemy)
    attackers = set()
    for square in zone:
        attackers.update(
            board.attackers(
                attacking_color,
                square
            )
        )
    return len(attackers)

# Total King Defenders
def king_defenders(
    board: chess.Board,
    defending_color: chess.Color
):
    """
    Counts defending pieces around
    their own king.
    """
    zone = king_zone(
        board,
        defending_color
    )
    defenders = set()
    for square in zone:
        defenders.update(
            board.attackers(
                defending_color,
                square
            )
        )
    return len(defenders)

# Attack Pressure

def attack_pressure(
    board: chess.Board,
    attacking_color: chess.Color
):
    """
    Attack Pressure
    =
    attackers
    -
    defenders

    Positive:
        Strong attack

    Negative:
        Well defended
    """
    enemy = not attacking_color

    attackers = king_attackers(
        board,
        attacking_color
    )

    defenders = king_defenders(
        board,
        enemy
    )
    return attackers - defenders

# Queen Participation
def queen_participates(
    board: chess.Board,
    color: chess.Color
):

    """
    Returns True if the queen attacks
    the enemy king zone.
    """
    \
    queens = board.pieces(
        chess.QUEEN,
        color
    )

    if not queens:
        return False

    enemy = not color

    zone = king_zone(
        board,
        enemy
    )

    for queen in queens:
        attacks = board.attacks(
            queen
        )
        if attacks & zone:
            return True
    return False

# Rook Participation
def rook_participation(
    board: chess.Board,
    color: chess.Color
):

    """
    Number of rooks attacking
    enemy king zone.
    """

    enemy = not color

    zone = king_zone(
        board,
        enemy
    )

    total = 0

    for rook in board.pieces(
        chess.ROOK,
        color
    ):
        attacks = board.attacks(
            rook
        )
        if attacks & zone:
            total += 1
    return total

# King Safety
def king_safety(
    board: chess.Board,
    color: chess.Color
):

    """
    Higher value means
    safer king.
    Simple heuristic:
    defenders
    -
    attackers
    """

    defenders = king_defenders(
        board,
        color
    )

    attackers = king_attackers(
        board,
        not color
    )

    return defenders - attackers


# Testing
if __name__ == "__main__":

    board = chess.Board()
    print("White Attackers:",
          king_attackers(board, chess.WHITE))
    print("Black Attackers:",
          king_attackers(board, chess.BLACK))
    print("Attack Pressure:",
          attack_pressure(board, chess.WHITE))
    print("White King Safety:",
          king_safety(board, chess.WHITE))
    
    
 # ==========================================
# Coaching Analysis
# ==========================================

def analyze_king(board: chess.Board, color: chess.Color):
    """
    Rich king analysis for the coaching system.
    Uses existing functions without affecting
    the style-classification pipeline.
    """

    king = king_square(board, color)

    if king is None:
        return None

    # ----------------------------
    # Castled?
    # ----------------------------

    if color == chess.WHITE:
        castled = king in (chess.G1, chess.C1)
    else:
        castled = king in (chess.G8, chess.C8)

    # ----------------------------
    # Existing metrics
    # ----------------------------

    attackers = king_attackers(
        board,
        not color
    )

    defenders = king_defenders(
        board,
        color
    )

    pressure = attack_pressure(
        board,
        not color
    )

    safety = king_safety(
        board,
        color
    )

    queen_attack = queen_participates(
        board,
        not color
    )

    rook_attackers = rook_participation(
        board,
        not color
    )

    # ----------------------------
    # Open file?
    # ----------------------------

    file = chess.square_file(king)

    open_file = True

    for rank in range(8):

        square = chess.square(file, rank)

        piece = board.piece_at(square)

        if piece and piece.piece_type == chess.PAWN:

            open_file = False

            break

    return {

        "castled": castled,

        "attackers": attackers,

        "defenders": defenders,

        "pressure": pressure,

        "safety": safety,

        "queen_attack": queen_attack,

        "rook_attackers": rook_attackers,

        "open_file": open_file

    }