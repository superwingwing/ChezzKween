import chess
from ml.analysis.material import analyze_material

def detect_material_reason(before: chess.Board, after: chess.Board):

    material = analyze_material(before, after)
    reasons = []

    # White gained material
    if material["white_change"] > 0:
        reasons.append({
            "reason": "material_gain",
            "confidence": 95,
            "details": {
                "side": "white",
                "change": material["white_change"]
            }
        })

    # White lost material
    elif material["white_change"] < 0:
        reasons.append({
            "reason": "material_loss",
            "confidence": 95,
            "details": {
                "side": "white",
                "change": abs(material["white_change"])
            }
        })

    # Black gained material
    if material["black_change"] > 0:
        reasons.append({
            "reason": "material_gain",
            "confidence": 95,
            "details": {
                "side": "black",
                "change": material["black_change"]
            }
        })

    # Black lost material
    elif material["black_change"] < 0:
        reasons.append({
            "reason": "material_loss",
            "confidence": 95,
            "details": {
                "side": "black",
                "change": abs(material["black_change"])
            }
        })

    # Material balance improved
    balance_change = (
        material["balance_after"] -
        material["balance_before"]
    )

    if balance_change > 0:
        reasons.append({
            "reason": "material_advantage",
            "confidence": 90,
            "details": {
                "side": "white",
                "change": balance_change
            }
        })

    elif balance_change < 0:
        reasons.append({
            "reason": "material_advantage",
            "confidence": 90,
            "details": {
                "side": "black",
                "change": abs(balance_change)
            }
        })

    if not reasons:
        return None

    reasons.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    return reasons[0]