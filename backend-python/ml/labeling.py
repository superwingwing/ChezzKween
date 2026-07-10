# labeling.py
def build_result(scores):
    aggressive = scores["Aggressive"]
    positional = scores["Positional"]

    dominant = max(   # Determine dominant style
        scores,
        key=scores.get
    )

    return {
        "AggressiveScore": aggressive,
        "PositionalScore": positional,
        "Label": dominant
    }

# Testing
if __name__ == "__main__":
    sample = {
        "Aggressive": 62.8,
        "Positional": 37.2
    }
    print(build_result(sample))