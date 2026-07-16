from ml.coach.principles import PRINCIPLES


class ExplanationEngine:

    def __init__(self):
        pass

    def generate(self, facts):

        explanation = {
            "title": "",
            "quality": "",
            "lesson": "",
            "what_happened": "",
            "why": "",
            "recommendation": ""
        }

        loss = facts["evaluation_loss"]

        # =====================================
        # Move Quality
        # =====================================

        if loss < 0.30:
            explanation["quality"] = "Best"

        elif loss < 0.70:
            explanation["quality"] = "Good"

        elif loss < 1.50:
            explanation["quality"] = "Inaccuracy"

        elif loss < 3.00:
            explanation["quality"] = "Mistake"

        else:
            explanation["quality"] = "Blunder"

        # =====================================
        # Castling
        # =====================================

        if facts["is_castle"]:

            p = PRINCIPLES["CASTLING"]

            explanation["title"] = p["title"]
            explanation["lesson"] = p["lesson"]
            explanation["what_happened"] = (
                "You castled your king."
            )
            explanation["why"] = p["explanation"]
            explanation["recommendation"] = p["recommendation"]

            return explanation

        # =====================================
        # Knight
        # =====================================

        if facts["piece"] == "knight":

            p = PRINCIPLES["KNIGHT_DEVELOPMENT"]

            explanation["title"] = p["title"]
            explanation["lesson"] = p["lesson"]
            explanation["what_happened"] = (
                "You developed a knight."
            )
            explanation["why"] = p["explanation"]
            explanation["recommendation"] = p["recommendation"]

            return explanation

        # =====================================
        # Bishop
        # =====================================

        if facts["piece"] == "bishop":

            p = PRINCIPLES["BISHOP_DEVELOPMENT"]

            explanation["title"] = p["title"]
            explanation["lesson"] = p["lesson"]
            explanation["what_happened"] = (
                "You developed a bishop."
            )
            explanation["why"] = p["explanation"]
            explanation["recommendation"] = p["recommendation"]

            return explanation

        # =====================================
        # Queen
        # =====================================

        if facts["piece"] == "queen":

            p = PRINCIPLES["EARLY_QUEEN"]

            explanation["title"] = p["title"]
            explanation["lesson"] = p["lesson"]
            explanation["what_happened"] = (
                "You chose to move your queen."
            )
            explanation["why"] = p["explanation"]
            explanation["recommendation"] = p["recommendation"]

            return explanation

        # =====================================
        # Capture
        # =====================================

        if facts["is_capture"]:

            p = PRINCIPLES["GOOD_CAPTURE"]

            explanation["title"] = p["title"]
            explanation["lesson"] = p["lesson"]
            explanation["what_happened"] = (
                "You captured an opponent's piece."
            )
            explanation["why"] = p["explanation"]
            explanation["recommendation"] = p["recommendation"]

            return explanation

        # =====================================
        # Check
        # =====================================

        if facts["gives_check"]:

            p = PRINCIPLES["CHECK"]

            explanation["title"] = p["title"]
            explanation["lesson"] = p["lesson"]
            explanation["what_happened"] = (
                "Your move gave check."
            )
            explanation["why"] = p["explanation"]
            explanation["recommendation"] = p["recommendation"]

            return explanation

        # =====================================
        # Evaluation Based
        # =====================================

        if explanation["quality"] == "Blunder":

            p = PRINCIPLES["BLUNDER"]

        elif explanation["quality"] == "Mistake":

            p = PRINCIPLES["MISTAKE"]

        else:

            explanation["title"] = "Solid Move"

            explanation["lesson"] = (
                "Continue looking for active moves."
            )

            explanation["what_happened"] = (
                "The move maintained a playable position."
            )

            explanation["why"] = (
                "It neither created major problems nor produced a decisive advantage."
            )

            explanation["recommendation"] = (
                "Keep improving your pieces while watching for tactical opportunities."
            )

            return explanation

        explanation["title"] = p["title"]

        explanation["lesson"] = p["lesson"]

        explanation["what_happened"] = (
            "The move caused a significant deterioration in the position."
        )

        explanation["why"] = p["explanation"]

        explanation["recommendation"] = p["recommendation"]

        return explanation