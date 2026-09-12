print("LOADED TACTICAL EXTRACTOR:", __file__)

from ml.analysis import tactical


def initialize(features):
    # Numeric features
    features["tactical_captures"] = 0
    features["hanging_captures"] = 0
    features["winning_exchanges"] = 0
    features["discovered_checks"] = 0
    features["double_checks"] = 0
    features["material_winning_combinations"] = 0


def update(board, move, features):
    summary = tactical.tactical_summary(board, [move])

    # Map detailed results to numeric features
    key_map = {
        "tactical_capture_moves": "tactical_captures",
        "hanging_capture_moves": "hanging_captures",
        "winning_exchange_moves": "winning_exchanges",
        "discovered_check_moves": "discovered_checks",
        "double_check_moves": "double_checks",
        "material_winning_moves": "material_winning_combinations"
    }

    for key, value in summary.items():
        if key in key_map:
            feature_key = key_map[key]

            if isinstance(value, list):
                features[feature_key] += len(value)
            elif isinstance(value, (int, float)):
                features[feature_key] += value

        elif isinstance(value, (int, float)):
            features.setdefault(key, 0)
            features[key] += value


def finalize(features):
    total = max(features["total_moves"], 1)

    # Tactical rates
    features["tactical_capture_rate"] = round(
        features["tactical_captures"] / total, 4
    )
    features["hanging_capture_rate"] = round(
        features["hanging_captures"] / total, 4
    )
    features["winning_exchange_rate"] = round(
        features["winning_exchanges"] / total, 4
    )
    features["double_check_rate"] = round(
        features["double_checks"] / total, 4
    )
    features["discovered_check_rate"] = round(
        features["discovered_checks"] / total, 4
    )