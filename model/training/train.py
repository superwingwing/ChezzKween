import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

from model.utils.feature_extractor import parse_pgn

data = []

pgn_folder = "model/raw_data"

# Loop through all PGN files
for file in os.listdir(pgn_folder):
    if file.endswith(".pgn"):
        file_path = os.path.join(pgn_folder, file)
        print(f"Processing {file_path}...")

        games = parse_pgn(file_path)
        data.extend(games)

# Convert to DataFrame
df = pd.DataFrame(data)

# Split features and labels
X = df.drop("label", axis=1)
y = df["label"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "model/saved/model.pkl")

print("✅ Model trained using multiple PGN files!")