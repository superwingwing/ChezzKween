# ml/scoring.py

# ----------------------------------------------------------
# RULE-BASED STYLE SCORING
#
# Weights are based on the heuristic rules
# described in the thesis.
# ----------------------------------------------------------

AGGRESSIVE_WEIGHTS = {
    "captures": 0.40,
    "sacrifices": 0.30,
    "king_attacks": 0.20,
    "forks": 0.10,
    "pawn_structure": 0.00,
    "piece_development": 0.00,
    "pins": 0.00
}

POSITIONAL_WEIGHTS = {
    "captures": 0.10,
    "sacrifices": 0.00,
    "king_attacks": 0.10,
    "forks": 0.00,
    "pawn_structure": 0.50,
    "piece_development": 0.30,
    "pins": 0.00
}

TACTICAL_WEIGHTS = {
    "captures": 0.20,
    "sacrifices": 0.30,
    "king_attacks": 0.20,
    "forks": 0.30,
    "pawn_structure": 0.00,
    "piece_development": 0.00,
    "pins": 0.30
}


def compute_scores(features):
    """
    Computes Aggressive, Positional,
    and Tactical scores from extracted features.

    Parameters
    ----------
    features : dict

    Returns
    -------
    dict
    """

    aggressive = 0
    positional = 0
    tactical = 0

    for feature, value in features.items():

        aggressive += (
            value *
            AGGRESSIVE_WEIGHTS.get(feature, 0)
        )

        positional += (
            value *
            POSITIONAL_WEIGHTS.get(feature, 0)
        )

        tactical += (
            value *
            TACTICAL_WEIGHTS.get(feature, 0)
        )

    return {
        "aggressive_score": round(aggressive, 2),
        "positional_score": round(positional, 2),
        "tactical_score": round(tactical, 2)
    }


# ----------------------------------------------------------
# Example
# ----------------------------------------------------------

if __name__ == "__main__":

    sample_features = {
        "captures": 6,
        "sacrifices": 2,
        "king_attacks": 5,
        "forks": 3,
        "pawn_structure": 2,
        "piece_development": 3,
        "pins": 1
    }

    scores = compute_style_scores(sample_features)

    print(scores)