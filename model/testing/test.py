import chess.pgn
import joblib

from model.utils.feature_extractor import extract_features_from_game


def predict_pgn(pgn_path):
    # Load model
    model = joblib.load("model/saved/model.pkl")

    with open(pgn_path) as pgn:
        game = chess.pgn.read_game(pgn)

        if game is None:
            print("❌ No game found")
            return

        # Extract features
        features = extract_features_from_game(game)

        # Remove label if exists
        if "label" in features:
            features.pop("label")

        # Convert to list
        feature_values = list(features.values())

        # Predict
        prediction = model.predict([feature_values])[0]

        print("🎯 Prediction:", prediction)
        print("📊 Features:", features)


# 👉 CHANGE THIS TO YOUR TEST FILE
predict_pgn("model/test_data/test1.pgn")