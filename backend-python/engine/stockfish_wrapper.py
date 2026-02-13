import chess.engine

ENGINE_PATH = "stockfish"   # or "stockfish.exe" if needed

# Create ONE global engine instance
engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)


def evaluate_move(board, move, idx):

    # Push move first so evaluation matches move played
    board.push(move)

    info = engine.analyse(
        board,
        chess.engine.Limit(depth=12)
    )

    score = info['score'].white().score(mate_score=10000)

    comment = f"Move {idx+1}: {board.san(move)}"

    if score is not None:
        if score > 50:
            comment += " is strong for White."
        elif score < -50:
            comment += " is strong for Black."
        else:
            comment += " is balanced."

    return comment


def close_engine():
    engine.quit()
