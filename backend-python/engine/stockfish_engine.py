import chess
import chess.engine

STOCKFISH_PATH = "stockfish"  # or full path if needed

engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)


def evaluate_position(fen: str, depth: int = 15):
    board = chess.Board(fen)

    info = engine.analyse(board, chess.engine.Limit(depth=depth))

    score = info["score"].relative

    if score.is_mate():
        return {
            "type": "mate",
            "value": score.mate()
        }

    return {
        "type": "cp",
        "value": score.score()
    }


def evaluate_game(pgn: str):
    game = chess.pgn.read_game(io.StringIO(pgn))

    board = game.board()

    evaluations = []

    for move in game.mainline_moves():
        board.push(move)

        eval = evaluate_position(board.fen())

        evaluations.append({
            "move": move.uci(),
            "fen": board.fen(),
            "evaluation": eval
        })

    return evaluations