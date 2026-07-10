import chess
from analysis import board
from analysis import king
from analysis import piece
from analysis import material

def initialize(features):
    features["sacrifices"] = 0
    features["king_attacks"] = 0
    features["open_files_to_king"] = 0
    features["queen_attack_participation"] = 0
    features["rook_attack_participation"] = 0
    features["attacking_piece_concentration"] = 0

# Update
def update(
    board_state: chess.Board,
    move: chess.Move,
    features
):
    """
    Called BEFORE board.push(move)
    """
    piece_moved = board_state.piece_at(
        move.from_square
    )
    if piece_moved is None:
        return
    color = piece_moved.color

    # Sacrifice
    if material.is_sacrifice(
        board_state,
        move
    ):
        features["sacrifices"] += 1

    # King Attackers
    features["king_attacks"] += (
        king.king_attackers(
            board_state,
            color
        )
    )
    # Open Files Toward Enemy King
    features["open_files_to_king"] += (
        board.open_files_to_king(
            board_state,
            not color
        )
    )
    # Queen Participation
    features["queen_attack_participation"] += (
        piece.queen_attack_participation(
            board_state,
            color
        )
    )
    # Rook Participation
    features["rook_attack_participation"] += (
        piece.rook_attack_participation(
            board_state,
            color
        )
    )
    # Attacking Piece Concentration
    features["attacking_piece_concentration"] += (
        piece.attacking_piece_concentration(
            board_state,
            color
        )
    )

# Finalize
def finalize(features):
    total_moves = max(
        features["total_moves"],
        1
    )

    features["sacrifices"] /= total_moves
    features["king_attacks"] /= total_moves
    features["open_files_to_king"] /= total_moves
    features["queen_attack_participation"] /= total_moves
    features["rook_attack_participation"] /= total_moves
    features["attacking_piece_concentration"] /= total_moves

