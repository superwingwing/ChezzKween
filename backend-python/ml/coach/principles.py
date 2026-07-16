"""
Chess Coaching Knowledge Base

Each principle contains:

- title
- lesson
- explanation
- recommendation

The Coach Engine will choose one or more principles
based on the facts returned by analyzer.py.
"""

PRINCIPLES = {

    # ======================================
    # OPENING
    # ======================================

    "EARLY_QUEEN": {

        "title":
            "Early Queen Development",

        "lesson":
            "Develop your minor pieces before moving the queen.",

        "explanation":
            "Bringing the queen out too early often allows your opponent to attack it while improving their own development.",

        "recommendation":
            "Develop your knights and bishops first before starting an attack."

    },

    "KNIGHT_DEVELOPMENT": {

        "title":
            "Knight Development",

        "lesson":
            "Develop knights toward the center.",

        "explanation":
            "Knights are most effective when placed on active central squares where they influence many important positions.",

        "recommendation":
            "Continue developing your remaining pieces before launching an attack."

    },

    "BISHOP_DEVELOPMENT": {

        "title":
            "Bishop Development",

        "lesson":
            "Activate bishops early.",

        "explanation":
            "Developed bishops control long diagonals and support both attack and defense.",

        "recommendation":
            "Look for opportunities to complete development and prepare castling."

    },

    "CASTLING": {

        "title":
            "King Safety",

        "lesson":
            "Castle early whenever possible.",

        "explanation":
            "Castling protects your king while connecting your rooks for future activity.",

        "recommendation":
            "After castling, continue activating your remaining pieces."

    },

    # ======================================
    # CENTER
    # ======================================

    "CENTER_CONTROL": {

        "title":
            "Center Control",

        "lesson":
            "Control the center.",

        "explanation":
            "Pieces placed near the center have greater mobility and influence over the board.",

        "recommendation":
            "Use your pawns and minor pieces to strengthen your central presence."

    },

    # ======================================
    # PIECE ACTIVITY
    # ======================================

    "PIECE_ACTIVITY": {

        "title":
            "Piece Activity",

        "lesson":
            "Keep your pieces active.",

        "explanation":
            "Active pieces create threats, support each other, and give you more tactical opportunities.",

        "recommendation":
            "Avoid leaving pieces undeveloped or trapped."

    },

    # ======================================
    # CAPTURES
    # ======================================

    "GOOD_CAPTURE": {

        "title":
            "Winning Material",

        "lesson":
            "Capture only when it improves your position.",

        "explanation":
            "Winning material is valuable when it does not weaken your position or lose the initiative.",

        "recommendation":
            "Before capturing, always check for tactical responses."

    },

    # ======================================
    # CHECK
    # ======================================

    "CHECK": {

        "title":
            "Checking the King",

        "lesson":
            "Checks should improve your position.",

        "explanation":
            "A check is strongest when it develops your attack or wins material, not simply because it is available.",

        "recommendation":
            "Always consider what happens after the opponent responds."

    },

    # ======================================
    # BLUNDER
    # ======================================

    "BLUNDER": {

        "title":
            "Large Evaluation Loss",

        "lesson":
            "Always check for threats before moving.",

        "explanation":
            "The move significantly worsened the position, suggesting that an important tactical or positional idea was overlooked.",

        "recommendation":
            "Slow down and examine your opponent's threats before making your decision."

    },

    "MISTAKE": {

        "title":
            "Missed Opportunity",

        "lesson":
            "Look for stronger candidate moves.",

        "explanation":
            "The move was playable but allowed a stronger continuation to be missed.",

        "recommendation":
            "Compare several candidate moves before choosing one."

    }

}