from ml.analysis import tactical

def initialize(features):
    features["tactical_captures"] = 0
    features["hanging_captures"] = 0
    features["winning_exchanges"] = 0
    features["discovered_checks"] = 0
    features["double_checks"] = 0
    features["material_winning_combinations"] = 0

def update(board, move, features):
    moves = [move]
    summary = tactical.tactical_summary(
        board,
        moves
    )
    for key, value in summary.items():
        features[key] += value

def finalize(features):
    total = max(
        features["total_moves"],
        1
    )
    features["tactical_capture_rate"] = round(
        features["tactical_captures"] / total,
        4
    )

    features["hanging_capture_rate"] = round(
        features["hanging_captures"] / total,
        4
    )
    features["winning_exchange_rate"] = round(
        features["winning_exchanges"] / total,
        4
    )
    features["double_check_rate"] = round(
        features["double_checks"] / total,
        4
    )
    features["discovered_check_rate"] = round(
        features["discovered_checks"] / total,
        4
    )