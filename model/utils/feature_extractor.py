import chess.pgn

def extract_features_from_game(game):
    board = game.board()

    features = {
        "captures": 0,
        "checks": 0,
        "moves": 0,
        "pawn_moves": 0,
        "early_development": 0
    }

    move_count = 0

    for move in game.mainline_moves():
        move_count += 1

        # Count captures
        if board.is_capture(move):
            features["captures"] += 1

        # Count checks
        if board.gives_check(move):
            features["checks"] += 1

        # Pawn movement
        piece = board.piece_at(move.from_square)
        if piece and piece.piece_type == chess.PAWN:
            features["pawn_moves"] += 1

        # Early development (first 10 moves)
        if move_count <= 10:
            if piece and piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
                features["early_development"] += 1

        board.push(move)

    features["moves"] = move_count

    return features


def parse_pgn(file_path):
    games_data = []

    with open(file_path) as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break

            features = extract_features_from_game(game)

            # Heuristic labeling
            if features["captures"] > 10 and features["checks"] > 5:
                label = "aggressive"
            else:
                label = "positional"

            features["label"] = label
            games_data.append(features)

    return games_data