from engine.stockfish_engine import evaluate_game


def analyze_pgn(pgn: str):
    evaluations = evaluate_game(pgn)

    # SIMPLE METRICS (you can improve later)
    blunders = 0
    mistakes = 0
    inaccuracies = 0

    prev = None

    for e in evaluations:
        val = e["evaluation"]["value"]

        if prev is not None:
            diff = abs(val - prev)

            if diff > 300:
                blunders += 1
            elif diff > 150:
                mistakes += 1
            elif diff > 80:
                inaccuracies += 1

        prev = val

    return {
        "evaluations": evaluations,
        "summary": {
            "blunders": blunders,
            "mistakes": mistakes,
            "inaccuracies": inaccuracies
        }
    }