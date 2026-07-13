import chess
from ml.analysis import board
from ml.analysis import piece

def initialize(features):
    features["center_control"] = 0
    features["extended_center_control"] = 0
    features["space_advantage"] = 0
    features["piece_activity"] = 0
    features["coordination"] = 0
    features["outposts"] = 0
    features["protected_pieces"] = 0
    features["rook_on_open_file"] = 0
    features["queen_on_open_file"] = 0
    features["_positions"] = 0


def update(
    board_state: chess.Board,
    move: chess.Move,
    features
):
    """
    Called BEFORE board.push(move).
    """
    color = board_state.turn

    features["center_control"] += (
        board.center_control(
            board_state,
            color
        )
    )

    features["extended_center_control"] += (
        board.extended_center_control(
            board_state,
            color
        )
    )

    features["space_advantage"] += (
        board.space_advantage(
            board_state,
            color
        )
    )

    features["piece_activity"] += (
        piece.activity_score(
            board_state,
            color
        )
    )

    features["coordination"] += (
        piece.coordination_score(
            board_state,
            color
        )
    )

    features["outposts"] += (
        piece.outposts(
            board_state,
            color
        )
    )

    features["protected_pieces"] += (
        piece.protected_pieces(
            board_state,
            color
        )
    )

    features["rook_on_open_file"] += (
        board.rook_on_open_file(
            board_state,
            color
        )
    )

    features["queen_on_open_file"] += (
        board.queen_on_open_file(
            board_state,
            color
        )
    )

    features["_positions"] += 1

def finalize(
    board_state,
    features
):

    total = max(features["_positions"], 1)

    positional_features = [
        "center_control",
        "extended_center_control",
        "space_advantage",
        "piece_activity",
        "coordination",
        "outposts",
        "protected_pieces",
        "rook_on_open_file",
        "queen_on_open_file"
    ]

    for feature in positional_features:
        features[feature] /= total
    del features["_positions"]