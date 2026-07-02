"""
labeling.py

Assign the final chess playing style based on
the highest heuristic score.
"""


def assign_label(aggressive_score, positional_score, tactical_score):
    """
    Returns the style with the highest score.

    Parameters
    ----------
    aggressive_score : float
    positional_score : float
    tactical_score : float

    Returns
    -------
    str
        "Aggressive"
        "Positional"
        "Tactical"
    """

    scores = {
        "Aggressive": aggressive_score,
        "Positional": positional_score,
        "Tactical": tactical_score
    }

    return max(scores, key=scores.get)


if __name__ == "__main__":

    label = assign_label(
        aggressive_score=4.3,
        positional_score=3.0,
        tactical_score=4.0
    )

    print(label)