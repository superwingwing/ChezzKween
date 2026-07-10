import os
import csv
from feature_extractor import extract_games_from_pgn
from scoring import compute_scores
from labeling import build_result

PGN_FOLDER = "dataset/pgn"
OUTPUT_FILE = "dataset/chess_dataset.csv"

def process_pgn(path):
    print(f"Reading {os.path.basename(path)}")
    rows = []
    games = extract_games_from_pgn(path)
    for features in games:
        scores = compute_scores(features)
        result = build_result(scores)
        row = {}
        row.update(features)
        row.update(result)
        rows.append(row)
    return rows

# Collect Dataset
def collect_dataset():
    dataset = []
    for filename in os.listdir(PGN_FOLDER):
        if filename.lower().endswith(".pgn"):
            path = os.path.join(
                PGN_FOLDER,
                filename
            )
            rows = process_pgn(path)
            dataset.extend(rows)
    return dataset

# Save CSV
def save_dataset(dataset):
    if len(dataset) == 0:
        print("No games found.")
        return
    columns = list(dataset[0].keys())
    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=columns
        )
        writer.writeheader()
        writer.writerows(dataset)

    print()
    print("------------------------------------")
    print("Dataset Created Successfully")
    print("------------------------------------")
    print(f"Games : {len(dataset)}")
    print(f"Saved : {OUTPUT_FILE}")
    print("------------------------------------")

# Main
def main():
    dataset = collect_dataset()
    save_dataset(dataset)

if __name__ == "__main__":
    main()