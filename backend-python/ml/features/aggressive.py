import chess

from helpers import (
    is_capture,
    gives_check,
    queen_move,
    rook_move,
    attacks_king_zone,
    material_difference
)


def extract_aggressive_features(game):
    """
    Extract aggressive-style features from one chess game.
    """

    board = game.board()

    captures = 0
    sacrifices = 0
    checks = 0
    king_attacks = 0
    queen_activity = 0
    rook_activity = 0
    attack_moves = 0

    previous_material = material_difference(board)

    for move in game.mainline_moves():

        # -----------------------------
        # Capture
        # -----------------------------
        if is_capture(board, move):
            captures += 1

        # -----------------------------
        # Check
        # -----------------------------
        if gives_check(board, move):
            checks += 1

        # -----------------------------
        # Queen Activity
        # -----------------------------
        if queen_move(board, move):
            queen_activity += 1

        # -----------------------------
        # Rook Activity
        # -----------------------------
        if rook_move(board, move):
            rook_activity += 1

        # -----------------------------
        # Attack near enemy king
        # -----------------------------
        if attacks_king_zone(board, move):
            king_attacks += 1

        # -----------------------------
        # Attack Move
        #
        # White entering ranks 5-8
        # Black entering ranks 1-4
        # -----------------------------
        piece = board.piece_at(move.from_square)

        if piece:

            rank = chess.square_rank(move.to_square)

            if piece.color == chess.WHITE:

                if rank >= 4:
                    attack_moves += 1

            else:

                if rank <= 3:
                    attack_moves += 1

        # -----------------------------
        # Sacrifice Detection
        #
        # Material decreases after move.
        # This is a heuristic.
        # -----------------------------
        board.push(move)

        current_material = material_difference(board)

        if current_material > previous_material:
            sacrifices += 1

        previous_material = current_material

    return {

        "captures": captures,

        "sacrifices": sacrifices,

        "checks": checks,

        "king_attacks": king_attacks,

        "queen_activity": queen_activity,

        "rook_activity": rook_activity,

        "attack_moves": attack_moves

    }


# --------------------------------------------
# Testing
# --------------------------------------------
if __name__ == "__main__":

    import chess.pgn

    with open("sample.pgn") as f:

        game = chess.pgn.read_game(f)

    print(extract_aggressive_features(game))