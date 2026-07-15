import joblib
import pandas as pd
from ml.feature_extractor import extract_games_from_pgn

MODEL = "ml/model/style_classifier.pkl"
ENCODER = "ml/model/label_encoder.pkl"

model = joblib.load(MODEL)
encoder = joblib.load(ENCODER)

FEATURE_COLUMNS = [
    "total_moves",
    "sacrifices",
    "king_attacks",
    "open_files_to_king",
    "queen_attack_participation",
    "rook_attack_participation",
    "attacking_piece_concentration",
    "center_control",
    "extended_center_control",
    "space_advantage",
    "piece_activity",
    "coordination",
    "outposts",
    "protected_pieces",
    "rook_on_open_file",
    "queen_on_open_file",
    "tactical_captures",
    "hanging_captures",
    "winning_exchanges",
    "discovered_checks",
    "double_checks",
    "material_winning_combinations",
    "tactical_capture_rate",
    "hanging_capture_rate",
    "winning_exchange_rate",
    "double_check_rate",
    "discovered_check_rate"
]

# ==========================================
# Predict Using Extracted Features
# Used by FastAPI upload route
# ==========================================

def predict_features(features):
    df = pd.DataFrame([
        {
            column: features[column]
            for column in FEATURE_COLUMNS
        }
    ])

    prediction = model.predict(df)[0]
    probabilities = model.predict_proba(df)[0]
    style = encoder.inverse_transform(
        [prediction]
    )[0]

    confidence = float(
        max(probabilities)
    )

    return {
        "style": style,
        "confidence": confidence,
        "probabilities": {
            encoder.classes_[i]:
            round(probabilities[i] * 100, 2)
            for i in range(len(probabilities))

        }

    }

# ==========================================
# Predict Entire PGN File
# Used for testing
# ==========================================

def predict_style(pgn_path):
    games = extract_games_from_pgn(pgn_path)
    predictions = []
    for game in games:
        prediction = predict_features(game)
        predictions.append(prediction)
    return predictions


# ==========================================
# Testing
# ==========================================

if __name__ == "__main__":
    results = predict_style(
        "dataset/pgn/sample.pgn"
    )

    for index, game in enumerate(results, start=1):

        print("--------------------------------")
        print(f"Game {index}")
        print("--------------------------------")
        print("Predicted Style :", game["style"])
        print("Confidence      :", round(game["confidence"] * 100, 2), "%")
        print()

        for style, probability in game["probabilities"].items():

            print(f"{style:15}: {probability}%")

        print("--------------------------------")