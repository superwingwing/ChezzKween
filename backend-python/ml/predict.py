# ==========================================
# predict_style.py
#
# Chess Playing Style Classification
#
# Predict Player Style
#
# Thesis:
# Chess Playing Style Classification
# ==========================================

import joblib
import pandas as pd

from feature_extractor import extract_games_from_pgn


# ==========================================
# Load Model
# ==========================================

MODEL = "models/style_classifier.pkl"
ENCODER = "models/label_encoder.pkl"

model = joblib.load(MODEL)
encoder = joblib.load(ENCODER)


# ==========================================
# Columns NOT used for prediction
# ==========================================

DROP_COLUMNS = [

    "event",
    "site",
    "date",
    "white",
    "black",
    "result",
    "eco"

]


# ==========================================
# Predict One PGN
# ==========================================

def predict_style(pgn_path):

    games = extract_games_from_pgn(pgn_path)

    if len(games) == 0:

        return []

    predictions = []

    for game in games:

        features = game.copy()

        for col in DROP_COLUMNS:

            features.pop(col, None)

        df = pd.DataFrame([features])

        prediction = model.predict(df)[0]

        probabilities = model.predict_proba(df)[0]

        style = encoder.inverse_transform([prediction])[0]

        predictions.append({

            "style": style,

            "probabilities": {

                encoder.classes_[i]: round(probabilities[i] * 100, 2)

                for i in range(len(probabilities))

            }

        })

    return predictions


# ==========================================
# Example
# ==========================================

if __name__ == "__main__":

    result = predict_style(

        "dataset/pgn/sample.pgn"

    )

    for game in result:

        print("--------------------------------")

        print("Predicted Style :", game["style"])

        print()

        for k, v in game["probabilities"].items():

            print(f"{k:15}: {v}%")

        print("--------------------------------")