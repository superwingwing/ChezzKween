# ==========================================
# feature_extractor.py
# ==========================================

import os
import io
import chess
import chess.pgn


# ------------------------------------------
# Detect if move gives check
# ------------------------------------------
def gives_check(board, move):
    board.push(move)
    check = board.is_check()
    board.pop()
    return check


# ------------------------------------------
# Detect development move
# (Knight/Bishop leaves starting square)
# ------------------------------------------
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


# ------------------------------------------
# Pawn advance
# ------------------------------------------
def pawn_advance(board, move):

    piece = board.piece_at(move.from_square)

    if piece and piece.piece_type == chess.PAWN:
        return 1

    return 0


# ------------------------------------------
# Center control
# ------------------------------------------
CENTER = {
    chess.D4,
    chess.D5,
    chess.E4,
    chess.E5
}


def controls_center(move):

    if move.to_square in CENTER:
        return 1

    return 0


# ------------------------------------------
# Extract one game's features
# ------------------------------------------
def extract_features(game):

    board = game.board()

    captures = 0
    checks = 0
    castles = 0
    developments = 0
    pawn_advances = 0
    center_control = 0

    total_moves = 0

    for move in game.mainline_moves():

        if board.is_capture(move):
            captures += 1

        if gives_check(board, move):
            checks += 1

        if board.is_castling(move):
            castles += 1

        if is_development(board, move):
            developments += 1

        pawn_advances += pawn_advance(board, move)

        center_control += controls_center(move)

        board.push(move)

        total_moves += 1

    winner = game.headers.get("Result", "*")

    return {

        "white": game.headers.get("White", ""),

        "black": game.headers.get("Black", ""),

        "result": winner,

        "moves": total_moves,

        "captures": captures,

        "checks": checks,

        "castles": castles,

        "developments": developments,

        "pawn_advances": pawn_advances,

        "center_control": center_control

    }


# ------------------------------------------
# Read one PGN file
# (supports MANY games)
# ------------------------------------------
def read_pgn_file(path):

    games = []

    with open(path, encoding="utf-8", errors="ignore") as f:

        while True:

            game = chess.pgn.read_game(f)

            if game is None:
                break

            features = extract_features(game)

            games.append(features)

    return games


# ------------------------------------------
# Read an entire folder
# ------------------------------------------
def read_dataset(folder):

    dataset = []

    for file in os.listdir(folder):

        if file.lower().endswith(".pgn"):

            full_path = os.path.join(folder, file)

            print("Reading:", file)

            games = read_pgn_file(full_path)

            dataset.extend(games)

    return dataset


# ------------------------------------------
# Testing
# ------------------------------------------
if __name__ == "__main__":

    folder = "dataset/pgn"

    data = read_dataset(folder)

    print()

    print("Games loaded:", len(data))

    print()

    print(data[0])