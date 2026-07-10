import chess.pgn
from extractors import aggressive
from extractors import positional
from extractors import tactical

# Extract One Game
def extract_features(game):
    board = game.board()
    features = {}
    features["event"] = game.headers.get("Event", "")
    features["site"] = game.headers.get("Site", "")
    features["date"] = game.headers.get("Date", "")
    features["white"] = game.headers.get("White", "")
    features["black"] = game.headers.get("Black", "")
    features["result"] = game.headers.get("Result", "")
    features["eco"] = game.headers.get("ECO", "")
    features["total_moves"] = 0

    # Initialize Extractors
    aggressive.initialize(features)
    positional.initialize(features)
    tactical.initialize(features)

    # Process Every Move
    for move in game.mainline_moves():
        aggressive.update(
            board,
            move,
            features
        )
        positional.update(
            board,
            move,
            features
        )
        tactical.update(
            board,
            move,
            features
        )
        board.push(move)
        features["total_moves"] += 1

    # Finalize Extractors
    aggressive.finalize(features)
    positional.finalize(
        board,
        features
    )
    tactical.finalize(features)

    return features

# Read Entire PGN File
# Supports multiple games

def extract_games_from_pgn(path):
    games = []
    with open(
        path,
        encoding="utf-8",
        errors="ignore"
    ) as f:

        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            try:
                features = extract_features(game)
                games.append(features)
            except Exception as e:
                print(
                    "Skipped game:",
                    e
                )
    return games

# Testing
if __name__ == "__main__":
    games = extract_games_from_pgn(
        "dataset/pgn/sample.pgn"
    )
    print()
    print("Games:", len(games))
    print()

    if games:
        for k, v in games[0].items():
            print(f"{k:25} {v}")