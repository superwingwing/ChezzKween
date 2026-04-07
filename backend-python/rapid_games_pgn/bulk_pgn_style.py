# Step 1 – Bulk PGN for Player Style
import chess.pgn
import os
import json

# ------------------------
# Helper functions
# ------------------------
def is_attacking_move(board, move):
    """Check if the move captures a piece"""
    return board.is_capture(move)

def is_tactical_move(board, move, engine=None):
    """Check if the move creates a sharp swing (simplified)"""
    # If you integrate Stockfish, can check evaluation swing
    # For now, simple heuristic: capture + attacking move
    return board.is_capture(move) or board.gives_check(move)

def is_positional_move(board, move):
    """Simplified: moves to central squares are positional"""
    central_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    return move.to_square in central_squares

def is_risky_move(board, move):
    """Simplified: moving a piece leaving it undefended"""
    board.push(move)
    attackers = board.attackers(not board.turn, move.to_square)
    board.pop()
    return len(attackers) > 0

def is_defensive_move(board, move):
    """Move that protects own pieces"""
    return False  # Simplified placeholder

# ------------------------
# Parse PGN files
# ------------------------
def parse_user_games(pgn_folder, user_name):
    games = []
    for file in os.listdir(pgn_folder):
        if not file.endswith(".pgn"):
            continue
        path = os.path.join(pgn_folder, file)
        with open(path) as pgn:
            while True:
                game = chess.pgn.read_game(pgn)
                if game is None:
                    break
                user_moves = []
                node = game
                move_number = 0
                board = game.board()
                while not node.is_end():
                    next_node = node.variation(0)
                    move = next_node.move
                    # Determine if it's user's turn
                    if (move_number % 2 == 0 and game.headers['White'] == user_name) or \
                       (move_number % 2 == 1 and game.headers['Black'] == user_name):
                        user_moves.append((board.copy(), move))
                    board.push(move)
                    node = next_node
                    move_number += 1
                if user_moves:
                    games.append(user_moves)
    return games

# ------------------------
# Compute Style Vector
# ------------------------
def compute_style_vector(games):
    metrics = {
        "aggression": 0,
        "tactics": 0,
        "positional": 0,
        "risk": 0,
        "defense": 0
    }
    total_moves = 0
    for game in games:
        for board, move in game:
            total_moves += 1
            if is_attacking_move(board, move):
                metrics["aggression"] += 1
            if is_tactical_move(board, move):
                metrics["tactics"] += 1
            if is_positional_move(board, move):
                metrics["positional"] += 1
            if is_risky_move(board, move):
                metrics["risk"] += 1
            if is_defensive_move(board, move):
                metrics["defense"] += 1
    # Normalize to 0-1
    style_vector = {k: v/total_moves for k,v in metrics.items()}
    return style_vector

# ------------------------
# Rule-based Style Classification
# ------------------------
def classify_style(vector):
    if vector['aggression'] > 0.6 and vector['tactics'] > 0.6 and vector['risk'] > 0.5:
        return "Tactical Aggressor"
    elif vector['positional'] > 0.6 and vector['risk'] < 0.4:
        return "Positional Strategist"
    elif vector['defense'] > 0.6 and vector['aggression'] < 0.4:
        return "Defensive Player"
    else:
        return "Balanced Player"

# ------------------------
# Main Execution
# ------------------------
if __name__ == "__main__":
    # Folder where multiple PGNs are stored
    pgn_folder = "pgn_games/"
    user_name = "John Doe"

    # 1. Parse PGN
    games = parse_user_games(pgn_folder, user_name)
    print(f"Loaded {len(games)} games for {user_name}")

    # 2. Compute Style Vector
    style_vector = compute_style_vector(games)
    print("Style Vector:", style_vector)

    # 3. Classify Style
    player_style = classify_style(style_vector)
    print("Player Style:", player_style)

    # 4. Save to JSON
    output = {
        "player_name": user_name,
        "style_vector": style_vector,
        "player_style": player_style
    }

    with open(f"{user_name}_style.json", "w") as f:
        json.dump(output, f, indent=4)

    print("Saved player style JSON.")