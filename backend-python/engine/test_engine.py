import chess
from stockfish_engine import create_engine, evaluate_position, close_engine

engine = create_engine()

board = chess.Board(
    "3rr1k1/p1p2nqp/1p2p1p1/5p2/2PP1Q1P/1P4P1/PB3PBK/4R3 b - - 4 30"
)

print("FEN:")
print(board.fen())

print("\nStockfish Analysis:")

result = evaluate_position(
    board,
    engine
)

print(result)

print("\nBest Move:")
print(result["best_move"])

print("\nEvaluation:")
print(result["evaluation"])

print("\nPV:")
for move in result["pv"]:
    print(move)

print("\nCandidates:")

for candidate in result["candidates"]:
    print("----------------")
    print("Eval:", candidate["evaluation"])
    print("Move:", candidate["best_move"])
    print("PV:")
    print(candidate["pv"])


close_engine(engine)