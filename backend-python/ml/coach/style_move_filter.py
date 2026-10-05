import chess
import chess.pgn
import io

from ml.feature_extractor import extract_features
from ml.scoring import compute_scores


# Maximum Stockfish evaluation loss allowed for a
# move to still be considered playable.
STYLE_MOVE_TOLERANCE = 0.50


def calculate_engine_loss(
    candidate_eval,
    best_eval,
    board
):
    """
    Calculate how much evaluation is lost compared
    with Stockfish's best candidate.

    Positive value = evaluation loss.

    The evaluation values are already expressed from
    White's perspective.
    """

    if board.turn == chess.WHITE:
        loss = best_eval - candidate_eval
    else:
        loss = candidate_eval - best_eval

    return max(0.0, round(loss, 2))


def is_playable(
    candidate_eval,
    best_eval,
    board
):
    """
    Determine whether a candidate is close enough
    to Stockfish's best move to remain playable.
    """

    engine_loss = calculate_engine_loss(
        candidate_eval,
        best_eval,
        board
    )

    return engine_loss <= STYLE_MOVE_TOLERANCE


def calculate_style_compatibility(
    candidate_style,
    player_aggressive,
    player_positional
):
    """
    Compare a candidate move's style profile with
    the player's overall style profile.

    Example:

        Player:
            Aggressive = 70
            Positional = 30

        Candidate:
            Aggressive = 80
            Positional = 20

    The candidate receives a higher compatibility
    score because it is more aligned with the
    player's aggressive style.
    """

    try:
        player_aggressive = float(
            player_aggressive
        )

        player_positional = float(
            player_positional
        )
    except (TypeError, ValueError):
        player_aggressive = 50.0
        player_positional = 50.0

    total_player_style = (
        player_aggressive +
        player_positional
    )

    if total_player_style <= 0:
        player_aggressive = 50.0
        player_positional = 50.0
    else:
        player_aggressive = (
            player_aggressive /
            total_player_style
        )

        player_positional = (
            player_positional /
            total_player_style
        )

    candidate_aggressive = float(
        candidate_style.get(
            "Aggressive",
            0
        )
    ) / 100.0

    candidate_positional = float(
        candidate_style.get(
            "Positional",
            0
        )
    ) / 100.0

    compatibility = (
        player_aggressive *
        candidate_aggressive
        +
        player_positional *
        candidate_positional
    )

    return round(
        compatibility,
        4
    )


def create_candidate_game(
    board,
    move
):
    """
    Create a temporary PGN game containing the
    current position and the candidate move.

    The existing feature extractor expects
    a chess.pgn.Game, so this function adapts
    the current board position to that format.
    """

    game = chess.pgn.Game()

    # Preserve the current position.
    game.setup(board)

    # Add the candidate move.
    game.add_variation(move)

    return game


def analyze_candidate_style(
    board,
    move_uci
):
    """
    Run the EXISTING feature extraction pipeline
    for one candidate move.

    No new chess features are created here.
    """

    try:
        move = chess.Move.from_uci(
            move_uci
        )
    except ValueError:
        return None

    if move not in board.legal_moves:
        return None

    try:
        candidate_game = create_candidate_game(
            board,
            move
        )

        features = extract_features(
            candidate_game
        )

        candidate_style = compute_scores(
            features
        )

        return {
            "features": features,
            "style": candidate_style
        }

    except Exception as error:
        print(
            "Candidate style analysis failed:",
            move_uci,
            error
        )

        return None


def filter_candidates_by_style(
    board,
    candidates,
    player_aggressive,
    player_positional
):
    """
    Select the Stockfish candidate that best matches
    the player's playing style while remaining playable.

    Pipeline:

        Stockfish candidates
            ↓
        Playability check
            ↓
        Existing feature extraction
            ↓
        Existing scoring.py
            ↓
        Style compatibility
            ↓
        Style-aware recommendation
    """

    if not candidates:
        return {
            "stockfish_best": None,
            "style_recommended": None,
            "playable_alternatives": []
        }

    # -----------------------------------------
    # PLAYER STYLE
    # -----------------------------------------

    try:
        player_aggressive = float(
            player_aggressive
        )

        player_positional = float(
            player_positional
        )

    except (TypeError, ValueError):
        player_aggressive = 50.0
        player_positional = 50.0

    total_style = (
        player_aggressive +
        player_positional
    )

    if total_style <= 0:
        player_aggressive = 50.0
        player_positional = 50.0

    else:
        player_aggressive = (
            player_aggressive /
            total_style
        ) * 100.0

        player_positional = (
            player_positional /
            total_style
        ) * 100.0

    # -----------------------------------------
    # STOCKFISH BEST
    # -----------------------------------------

    stockfish_best = candidates[0]

    best_eval = stockfish_best.get(
        "evaluation",
        0.0
    )

    playable_candidates = []

    # -----------------------------------------
    # CHECK EACH STOCKFISH CANDIDATE
    # -----------------------------------------

    for candidate in candidates:

        move_uci = candidate.get(
            "best_move"
        )

        candidate_eval = candidate.get(
            "evaluation"
        )

        if not move_uci:
            continue

        if candidate_eval is None:
            continue

        # -------------------------------------
        # ENGINE PLAYABILITY
        # -------------------------------------

        engine_loss = calculate_engine_loss(
            candidate_eval,
            best_eval,
            board
        )

        if not is_playable(
            candidate_eval,
            best_eval,
            board
        ):
            continue

        # -------------------------------------
        # EXISTING STYLE EXTRACTION
        # -------------------------------------

        candidate_analysis = analyze_candidate_style(
            board=board,
            move_uci=move_uci
        )

        if candidate_analysis is None:
            continue

        candidate_style = (
            candidate_analysis["style"]
        )

        candidate_features = (
            candidate_analysis["features"]
        )

        # -------------------------------------
        # STYLE COMPATIBILITY
        # -------------------------------------

        style_score = calculate_style_compatibility(
            candidate_style=candidate_style,
            player_aggressive=player_aggressive,
            player_positional=player_positional
        )

        # -------------------------------------
        # STORE CANDIDATE
        # -------------------------------------

        playable_candidates.append({
            "move": move_uci,

            "evaluation": candidate_eval,

            "engine_loss": engine_loss,

            "pv": candidate.get(
                "pv",
                []
            ),

            "aggressive_score": candidate_style.get(
                "Aggressive",
                0
            ),

            "positional_score": candidate_style.get(
                "Positional",
                0
            ),

            "style_score": style_score,

            "features": candidate_features,

            "fallback": False
        })

    # -----------------------------------------
    # FALLBACK
    # -----------------------------------------

    if not playable_candidates:

        return {
            "stockfish_best": stockfish_best,

            "style_recommended": {
                "move": stockfish_best.get(
                    "best_move"
                ),

                "evaluation": stockfish_best.get(
                    "evaluation"
                ),

                "engine_loss": 0.0,

                "pv": stockfish_best.get(
                    "pv",
                    []
                ),

                "aggressive_score": None,

                "positional_score": None,

                "style_score": None,

                "features": None,

                "fallback": True
            },

            "playable_alternatives": []
        }

    # -----------------------------------------
    # RANK BY STYLE COMPATIBILITY
    # -----------------------------------------

    playable_candidates.sort(
        key=lambda candidate:
            candidate["style_score"],
        reverse=True
    )

    style_recommended = (
        playable_candidates[0]
    )

    # -----------------------------------------
    # ALTERNATIVES
    # -----------------------------------------

    playable_alternatives = [
        candidate
        for candidate in playable_candidates
        if candidate["move"]
        != style_recommended["move"]
    ]

    return {
        "stockfish_best": stockfish_best,

        "style_recommended": style_recommended,

        "playable_alternatives":
            playable_alternatives
    }