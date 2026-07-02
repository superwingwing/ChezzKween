import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# ------------------------------------------
# Load Dataset
# ------------------------------------------

df = pd.read_csv("dataset/dataset.csv")

# ------------------------------------------
# Drop non-feature columns
# ------------------------------------------

X = df.drop(
    columns=[
        "white",
        "black",
        "event",
        "label"
    ]
)

y = df["label"]

# ------------------------------------------
# 70 / 15 / 15 Split
# ------------------------------------------

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

X_validation, X_test, y_validation, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)

print()

print("Training:", len(X_train))
print("Validation:", len(X_validation))
print("Testing:", len(X_test))

# ------------------------------------------
# Train Random Forest
# ------------------------------------------

model = RandomForestClassifier(

    n_estimators=300,

    max_depth=15,

    random_state=42

)

model.fit(X_train, y_train)

# ------------------------------------------
# Validation Accuracy
# ------------------------------------------

validation_prediction = model.predict(X_validation)

print()

print("Validation Accuracy")

print(
    accuracy_score(
        y_validation,
        validation_prediction
    )
)

# ------------------------------------------
# Final Test Accuracy
# ------------------------------------------

prediction = model.predict(X_test)

print()

print("Final Accuracy")

print(
    accuracy_score(
        y_test,
        prediction
    )
)

print()

print(

    classification_report(

        y_test,

        prediction

    )

)

print()

print(

    confusion_matrix(

        y_test,

        prediction

    )

)

# ------------------------------------------
# Save Model
# ------------------------------------------

joblib.dump(

    model,

    "style_classifier.pkl"

)

print()

print("Model Saved!")