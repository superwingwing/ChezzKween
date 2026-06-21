# test_engine.py

import chess
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("stockfish.exe")

board = chess.Board()

result = engine.analyse(board, chess.engine.Limit(time=1))

print(result["score"])

engine.quit()