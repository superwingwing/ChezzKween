# ==========================================
# scoring.py
#
# Rule-Based Style Scoring
#
# Thesis:
# Chess Playing Style Classification
#
# Styles:
#   • Aggressive
#   • Positional
#
# Tactical features contribute to Aggressive
# ==========================================


# ==========================================
# Style Weights
# ==========================================

STYLE_WEIGHTS = {


    # --------------------------------------
    # Aggressive Features
    # --------------------------------------

    "Aggressive": {

        "sacrifices": 0.25,

        "king_attacks": 0.25,

        "queen_attack_participation": 0.20,

        "rook_attack_participation": 0.15,

        "attacking_piece_concentration": 0.15

    },


    # --------------------------------------
    # Positional Features
    # --------------------------------------

    "Positional": {

        "center_control": 0.15,

        "extended_center_control": 0.15,

        "space_advantage": 0.15,

        "piece_activity": 0.15,

        "coordination": 0.10,

        "outposts": 0.10,

        "protected_pieces": 0.10,

        "rook_on_open_file": 0.05,

        "queen_on_open_file": 0.05

    },


    # --------------------------------------
    # Tactical Features
    #
    # Tactical is not a separate style.
    # These features are merged into
    # Aggressive scoring.
    # --------------------------------------

    "Tactical": {

        "tactical_captures": 0.25,

        "hanging_captures": 0.15,

        "winning_exchanges": 0.20,

        "discovered_checks": 0.15,

        "double_checks": 0.15,

        "material_winning_combinations": 0.10

    }

}



# ==========================================
# Compute One Style
# ==========================================

def compute_style(features, weights):

    score = 0.0


    for feature, weight in weights.items():

        value = features.get(feature, 0)


        if isinstance(value, bool):

            value = int(value)


        score += value * weight


    return score



# ==========================================
# Normalize Scores
# ==========================================

def normalize(scores):

    total = sum(scores.values())


    if total == 0:

        return {

            "Aggressive": 50.0,

            "Positional": 50.0

        }


    normalized = {}


    for style, value in scores.items():

        normalized[style] = round(

            (value / total) * 100,

            2

        )


    return normalized



# ==========================================
# Compute Scores
# ==========================================

def compute_scores(features):


    aggressive_weights = {

        **STYLE_WEIGHTS["Aggressive"],

        **STYLE_WEIGHTS["Tactical"]

    }


    scores = {


        # Aggressive =
        # attacking features + tactical features

        "Aggressive": compute_style(

            features,

            aggressive_weights

        ),



        # Positional =
        # positional features only

        "Positional": compute_style(

            features,

            STYLE_WEIGHTS["Positional"]

        )

    }


    return normalize(scores)



# ==========================================
# Testing
# ==========================================

if __name__ == "__main__":


    sample = {


        # ------------------------------
        # Aggressive
        # ------------------------------

        "sacrifices": 4,

        "king_attacks": 18,

        "queen_attack_participation": 10,

        "rook_attack_participation": 8,

        "attacking_piece_concentration": 6,



        # ------------------------------
        # Tactical
        # ------------------------------

        "tactical_captures": 12,

        "hanging_captures": 5,

        "winning_exchanges": 7,

        "discovered_checks": 2,

        "double_checks": 1,

        "material_winning_combinations": 4,



        # ------------------------------
        # Positional
        # ------------------------------

        "center_control": 16,

        "extended_center_control": 24,

        "space_advantage": 18,

        "piece_activity": 12,

        "coordination": 10,

        "outposts": 3,

        "protected_pieces": 18,

        "rook_on_open_file": 2,

        "queen_on_open_file": 1

    }



    result = compute_scores(sample)


    print(result)