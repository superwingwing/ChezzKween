import chess

from helpers import (
    controls_center,
    is_development,
    is_castle
)


# ------------------------------------------
# Count doubled pawns
# ------------------------------------------
def doubled_pawns(board, color):

    count = 0

    for file in range(8):

        pawns = 0

        for rank in range(8):

            square = chess.square(file, rank)

            piece = board.piece_at(square)

            if (
                piece
                and piece.color == color
                and piece.piece_type == chess.PAWN
            ):
                pawns += 1

        if pawns > 1:
            count += pawns - 1

    return count


# ------------------------------------------
# Count isolated pawns
# ------------------------------------------
def isolated_pawns(board, color):

    pawns = board.pieces(chess.PAWN, color)

    isolated = 0

    for pawn in pawns:

        file = chess.square_file(pawn)

        neighbour = False

        for other in pawns:

            if other == pawn:
                continue

            if abs(chess.square_file(other) - file) == 1:
                neighbour = True
                break

        if not neighbour:
            isolated += 1

    return isolated


# ------------------------------------------
# Count passed pawns
# ------------------------------------------
def passed_pawns(board, color):

    passed = 0

    my_pawns = board.pieces(chess.PAWN, color)
    enemy_pawns = board.pieces(chess.PAWN, not color)

    for pawn in my_pawns:

        file = chess.square_file(pawn)
        rank = chess.square_rank(pawn)

        blocked = False

        for enemy in enemy_pawns:

            ef = chess.square_file(enemy)
            er = chess.square_rank(enemy)

            if abs(file - ef) <= 1:

                if color == chess.WHITE:

                    if er > rank:
                        blocked = True

                else:

                    if er < rank:
                        blocked = True

        if not blocked:
            passed += 1

    return passed


# ------------------------------------------
# Bishop Pair
# ------------------------------------------
def bishop_pair(board, color):

    bishops = board.pieces(chess.BISHOP, color)

    return 1 if len(bishops) >= 2 else 0


# ------------------------------------------
# Extract positional features
# ------------------------------------------
def extract_positional_features(game):

    board = game.board()

    development = 0
    center_control = 0
    castles = 0

    for move in game.mainline_moves():

        if is_development(board, move):
            development += 1

        if controls_center(move):
            center_control += 1

        if is_castle(board, move):
            castles += 1

        board.push(move)

    white_doubled = doubled_pawns(board, chess.WHITE)
    black_doubled = doubled_pawns(board, chess.BLACK)

    white_isolated = isolated_pawns(board, chess.WHITE)
    black_isolated = isolated_pawns(board, chess.BLACK)

    white_passed = passed_pawns(board, chess.WHITE)
    black_passed = passed_pawns(board, chess.BLACK)

    white_bishop = bishop_pair(board, chess.WHITE)
    black_bishop = bishop_pair(board, chess.BLACK)

    return {

        "piece_development": development,

        "center_control": center_control,

        "castles": castles,

        "pawn_structure":
            (
                white_passed
                + black_passed
                - white_doubled
                - black_doubled
                - white_isolated
                - black_isolated
            ),

        "passed_pawns":
            white_passed + black_passed,

        "isolated_pawns":
            white_isolated + black_isolated,

        "doubled_pawns":
            white_doubled + black_doubled,

        "bishop_pair":
            white_bishop + black_bishop
    }


# ------------------------------------------
# Testing
# ------------------------------------------
if __name__ == "__main__":

    import chess.pgn

    with open("sample.pgn") as f:

        game = chess.pgn.read_game(f)

    print(extract_positional_features(game))