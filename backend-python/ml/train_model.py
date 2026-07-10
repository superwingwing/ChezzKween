import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.preprocessing import LabelEncoder

DATASET = "dataset/chess_dataset.csv"
MODEL = "model/style_classifier.pkl"
ENCODER = "model/label_encoder.pkl"


# Load Dataset
df = pd.read_csv(DATASET)
print()
print("Dataset Loaded")
print(df.shape)


# Features

DROP_COLUMNS = [
    "event",
    "site",
    "date",
    "white",
    "black",
    "result",
    "eco",
    "AggressiveScore",
    "PositionalScore",
    "Label"
]

X = df.drop(columns=DROP_COLUMNS)
y = df["Label"]

# Encode Labels
encoder = LabelEncoder()
y = encoder.fit_transform(y)

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Train Model
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)

# Prediction
prediction = model.predict(X_test)

# Evaluation
print()
print("--------------------------------")
print("Accuracy")
print(
    accuracy_score(
        y_test,
        prediction
    )
)

print()
print("Classification Report")
print(
    classification_report(
        y_test,
        prediction,
        target_names=encoder.classes_
    )
)

print()
print("Confusion Matrix")
print(
    confusion_matrix(
        y_test,
        prediction
    )
)

# Save Model
joblib.dump(
    model,
    MODEL
)

joblib.dump(
    encoder,
    ENCODER
)

print()
print("Model Saved")
print(X.columns.tolist())