# ==========================================
# labeling.py
#
# Chess Style Labeling
#
# Thesis:
# Chess Playing Style Classification
#
# Converts normalized style scores
# into the final ML label.
#
# FINAL VERSION
# ==========================================


# ==========================================
# Main Label Builder
# ==========================================

def build_result(scores):

    aggressive = scores["Aggressive"]
    positional = scores["Positional"]

    # -------------------------
    # Determine dominant style
    # -------------------------

    dominant = max(
        scores,
        key=scores.get
    )

    return {

        "AggressiveScore": aggressive,

        "PositionalScore": positional,

        "Label": dominant

    }


# ==========================================
# Testing
# ==========================================

if __name__ == "__main__":

    sample = {

        "Aggressive": 62.8,

        "Positional": 37.2

    }

    print(build_result(sample))