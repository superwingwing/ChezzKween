from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Evaluate Model
def evaluate_model(true_labels, predicted_labels):
    accuracy = accuracy_score(
        true_labels,
        predicted_labels
    )
    precision = precision_score(
        true_labels,
        predicted_labels,
        average="weighted"
    )
    recall = recall_score(
        true_labels,
        predicted_labels,
        average="weighted"
    )
    f1 = f1_score(
        true_labels,
        predicted_labels,
        average="weighted"
    )
    matrix = confusion_matrix(
        true_labels,
        predicted_labels
    )
    report = classification_report(
        true_labels,
        predicted_labels
    )


    results = {
        "Accuracy": round(
            accuracy * 100,
            2
        ),
        "Precision": round(
            precision * 100,
            2
        ),
        "Recall": round(
            recall * 100,
            2
        ),
        "F1 Score": round(
            f1 * 100,
            2
        ),
        "Confusion Matrix": matrix,
        "Classification Report": report
    }
    return results

# Testing
if __name__ == "__main__":


    # Ground truth labels
    # Manually assigned by chess experts
    # or based on player analysis
    true_labels = [
        "Aggressive",
        "Aggressive",
        "Positional",
        "Positional",
        "Aggressive",
        "Positional"
    ]

    # Output from your scoring.py

    predicted_labels = [
        "Aggressive",
        "Positional",
        "Positional",
        "Positional",
        "Aggressive",
        "Aggressive"
    ]

    results = evaluate_model(
        true_labels,
        predicted_labels
    )

    print("\nEvaluation Results")
    print("===================")
    for key, value in results.items():
        print(f"\n{key}:")
        print(value)