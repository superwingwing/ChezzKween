import chess
import chess.pgn

from aggressive import extract_aggressive_features
from tactical import extract_tactical_features
from positional import extract_positional_features

from helpers import material_difference


def extract_game_features(game):
    """
    Extract every feature from one chess game.
    Returns a single dictionary.
    """

    board = game.board()

    # -------------------------
    # Merge all feature groups
    # -------------------------
    features = {}

    features.update(
        extract_aggressive_features(game)
    )

    features.update(
        extract_tactical_features(game)
    )

    features.update(
        extract_positional_features(game)
    )

    # -------------------------
    # General Features
    # -------------------------

    total_moves = 0

    exchanges = 0

    for move in game.mainline_moves():

        if board.is_capture(move):
            exchanges += 1

        board.push(move)

        total_moves += 1

    features["total_moves"] = total_moves

    features["material_balance"] = material_difference(board)

    features["result"] = game.headers.get("Result", "*")

    features["white_player"] = game.headers.get("White", "")

    features["black_player"] = game.headers.get("Black", "")

    features["white_elo"] = game.headers.get("WhiteElo", "0")

    features["black_elo"] = game.headers.get("BlackElo", "0")

    features["eco"] = game.headers.get("ECO", "")

    return features


def extract_pgn_features(filepath):
    """
    Reads a PGN file containing
    one or many games.
    """

    dataset = []

    with open(filepath, encoding="utf-8", errors="ignore") as pgn:

        while True:

            game = chess.pgn.read_game(pgn)

            if game is None:
                break

            features = extract_game_features(game)

            dataset.append(features)

    return dataset


# ------------------------------------------
# TEST
# ------------------------------------------
if __name__ == "__main__":

    data = extract_pgn_features(
        "../dataset/pgn/sample.pgn"
    )

    print("Games:", len(data))

    print()

    print(data[0])