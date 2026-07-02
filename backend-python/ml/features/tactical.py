import chess


# -------------------------------------------------
# Detect Pins
# -------------------------------------------------
def count_pins(board):

    pins = 0

    for color in [chess.WHITE, chess.BLACK]:

        king = board.king(color)

        if king is None:
            continue

        for square in chess.SQUARES:

            piece = board.piece_at(square)

            if piece is None:
                continue

            if piece.color != color:
                continue

            if board.is_pinned(color, square):
                pins += 1

    return pins


# -------------------------------------------------
# Detect Forks
#
# Simple heuristic:
# after moving, piece attacks at least
# TWO enemy pieces.
# -------------------------------------------------
def is_fork(board, move):

    board.push(move)

    attacker_square = move.to_square

    piece = board.piece_at(attacker_square)

    if piece is None:
        board.pop()
        return False

    enemy = not piece.color

    attacks = board.attacks(attacker_square)

    targets = 0

    for sq in attacks:

        p = board.piece_at(sq)

        if p and p.color == enemy:

            targets += 1

    board.pop()

    return targets >= 2


# -------------------------------------------------
# Detect Skewers
#
# Simple heuristic:
# sliding piece attacks king and another
# valuable piece behind.
# -------------------------------------------------
def is_skewer(board, move):

    board.push(move)

    piece = board.piece_at(move.to_square)

    if piece is None:

        board.pop()
        return False

    if piece.piece_type not in (
        chess.BISHOP,
        chess.ROOK,
        chess.QUEEN
    ):
        board.pop()
        return False

    enemy = not piece.color

    king_square = board.king(enemy)

    if king_square is None:
        board.pop()
        return False

    attacks = board.attacks(move.to_square)

    result = king_square in attacks

    board.pop()

    return result


# -------------------------------------------------
# Detect Discovered Attack
#
# Simple heuristic:
# moved piece was blocking another piece.
# -------------------------------------------------
def discovered_attack(board, move):

    piece = board.piece_at(move.from_square)

    if piece is None:
        return False

    board.push(move)

    enemy = board.turn

    discovered = False

    for sq in chess.SQUARES:

        p = board.piece_at(sq)

        if p is None:
            continue

        if p.color != piece.color:
            continue

        attacks = board.attacks(sq)

        for target in attacks:

            tp = board.piece_at(target)

            if tp and tp.color == enemy:

                discovered = True
                break

        if discovered:
            break

    board.pop()

    return discovered


# -------------------------------------------------
# Extract Tactical Features
# -------------------------------------------------
def extract_tactical_features(game):

    board = game.board()

    forks = 0
    pins = 0
    skewers = 0
    discovered = 0
    tactical_captures = 0

    for move in game.mainline_moves():

        if is_fork(board, move):
            forks += 1

        if is_skewer(board, move):
            skewers += 1

        if discovered_attack(board, move):
            discovered += 1

        if board.is_capture(move):

            if (
                is_fork(board, move)
                or is_skewer(board, move)
            ):
                tactical_captures += 1

        board.push(move)

    pins = count_pins(board)

    return {

        "forks": forks,

        "pins": pins,

        "skewers": skewers,

        "discovered_attacks": discovered,

        "tactical_captures": tactical_captures

    }


# -------------------------------------------------
# Testing
# -------------------------------------------------
if __name__ == "__main__":

    import chess.pgn

    with open("sample.pgn") as f:

        game = chess.pgn.read_game(f)

    print(extract_tactical_features(game))