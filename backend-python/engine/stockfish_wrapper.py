import chess.engine

def evaluate_move(board, move, idx):
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")  # adjust path
    info = engine.analyse(board, chess.engine.Limit(depth=12))
    score = info['score'].white().score(mate_score=10000)
    engine.quit()
    comment = f"Move {idx+1}: {board.san(move)}"
    if score is not None:
        if score > 50:
            comment += " is strong for White."
        elif score < -50:
            comment += " is strong for Black."
        else:
            comment += " is balanced."
    return comment
