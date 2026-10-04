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


# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv(DATASET)

print()
print("Dataset Loaded")
print("Dataset Shape:", df.shape)


# ==========================================
# Features
# ==========================================

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


# ==========================================
# Encode Labels
# ==========================================

encoder = LabelEncoder()
y = encoder.fit_transform(y)


# ==========================================
# Dataset Split
# 70% Training
# 15% Validation
# 15% Testing
# ==========================================

# First split:
# 70% Training
# 30% Temporary
X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

# Second split:
# 15% Validation
# 15% Testing
X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)


# ==========================================
# Display Dataset Split
# ==========================================

print()
print("--------------------------------")
print("Dataset Split")
print("--------------------------------")
print("Training   :", len(X_train))
print("Validation :", len(X_val))
print("Testing    :", len(X_test))
print("Total      :", len(X_train) + len(X_val) + len(X_test))


# ==========================================
# Train Random Forest Model
# ==========================================

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)


# ==========================================
# Validation Evaluation
# ==========================================

validation_prediction = model.predict(X_val)

validation_accuracy = accuracy_score(
    y_val,
    validation_prediction
)

print()
print("--------------------------------")
print("Validation Results")
print("--------------------------------")
print("Validation Accuracy:")
print(validation_accuracy)

print()
print("Validation Classification Report")
print(
    classification_report(
        y_val,
        validation_prediction,
        target_names=encoder.classes_
    )
)


# ==========================================
# Final Testing
# ==========================================

test_prediction = model.predict(X_test)


# ==========================================
# Final Evaluation
# ==========================================

test_accuracy = accuracy_score(
    y_test,
    test_prediction
)

print()
print("--------------------------------")
print("Final Test Results")
print("--------------------------------")

print()
print("Test Accuracy:")
print(test_accuracy)

print()
print("Test Classification Report")
print(
    classification_report(
        y_test,
        test_prediction,
        target_names=encoder.classes_
    )
)

print()
print("Test Confusion Matrix")
print(
    confusion_matrix(
        y_test,
        test_prediction
    )
)


# ==========================================
# Save Model
# ==========================================

joblib.dump(
    model,
    MODEL
)

joblib.dump(
    encoder,
    ENCODER
)

print()
print("--------------------------------")
print("Model Saved")
print("--------------------------------")
print("Model:", MODEL)
print("Encoder:", ENCODER)

print()
print("Feature Columns:")
print(X.columns.tolist())