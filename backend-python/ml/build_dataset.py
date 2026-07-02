import os
import csv
import io
import chess.pgn

from feature_extractor import extract_features
from scoring import compute_scores
from labeling import assign_label

# Folder containing PGN files
PGN_FOLDER = "dataset/pgn"

# Output CSV
OUTPUT_FILE = "dataset/dataset.csv"


FIELDNAMES = [
    "white",
    "black",
    "event",

    # Features
    "captures",
    "checks",
    "castles",
    "queen_moves",
    "rook_moves",
    "bishop_moves",
    "knight_moves",
    "pawn_moves",
    "king_moves",
    "center_moves",
    "promotion",
    "piece_development",

    # Scores
    "aggressive_score",
    "positional_score",
    "tactical_score",

    # Final label
    "label"
]


def process_game(game):

    features = extract_features(game)

    aggressive, positional, tactical = compute_scores(features)

    label = assign_label(
        aggressive,
        positional,
        tactical
    )

    row = {
        "white": game.headers.get("White", ""),
        "black": game.headers.get("Black", ""),
        "event": game.headers.get("Event", ""),

        **features,

        "aggressive_score": aggressive,
        "positional_score": positional,
        "tactical_score": tactical,

        "label": label
    }

    return row


def process_pgn(filepath, writer):

    print(f"Reading {filepath}")

    with open(filepath, encoding="utf-8", errors="ignore") as f:

        while True:

            game = chess.pgn.read_game(f)

            if game is None:
                break

            row = process_game(game)

            writer.writerow(row)


def main():

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=FIELDNAMES
        )

        writer.writeheader()

        for filename in os.listdir(PGN_FOLDER):

            if filename.endswith(".pgn"):

                process_pgn(
                    os.path.join(PGN_FOLDER, filename),
                    writer
                )

    print("Dataset created!")
    print("Saved as:", OUTPUT_FILE)


if __name__ == "__main__":
    main()