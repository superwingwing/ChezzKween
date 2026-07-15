from ml.feature_extractor import extract_features
from ml.predict import predict_features
from fastapi import APIRouter, UploadFile, File
from supabase import create_client
from dotenv import load_dotenv
import chess.pgn
import io
import uuid
import os
import traceback


load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

router = APIRouter()



# Extract SAN Moves
def extract_moves(game):
    board = game.board()
    moves = []
    for move in game.mainline_moves():
        moves.append(board.san(move))
        board.push(move)
    return " ".join(moves)


# Upload Style PGNs
@router.post("/upload_style")
async def upload_style(
    files: list[UploadFile] = File(...)
):

    upload_session_id = str(uuid.uuid4())
    inserted_games = 0
    print("====================================")
    print("STYLE UPLOAD STARTED")
    print("FILES:", len(files))
    print("====================================")
    try:

        # Loop every uploaded PGN file
        for file in files:
            print(f"Processing File: {file.filename}")
            content = await file.read()
            text = content.decode(
                "utf-8",
                errors="ignore"
            )
            stream = io.StringIO(text)
            game_number = 1
            # Read every game inside the PGN
            while True:
                game = chess.pgn.read_game(stream)
                if game is None:
                    break
                try:
                    # Feature Extraction
                    features = extract_features(game)
                    # Machine Learning Prediction
                    prediction = predict_features(features)
                    features["predicted_style"] = prediction["style"]
                    features["confidence"] = prediction["confidence"]
                    # Original PGN
                    features["pgn"] = str(game)
                    # SAN Moves
                    features["moves"] = extract_moves(game)
                    # Upload Information
                    features["upload_session_id"] = upload_session_id
                    features["game_number"] = game_number
                    # Uncomment if your table has this column
                    # features["user_id"] = "<current_user_uuid>"
                    # Save to Supabase
                    result = (
                        supabase
                        .table("style")
                        .insert(features)
                        .execute()
                    )

                    print("--------------------------------")
                    print("Game:", game_number)
                    print("White:", features["white"])
                    print("Black:", features["black"])
                    print("Prediction:", prediction["style"])
                    print("Confidence:", prediction["confidence"])
                    print("--------------------------------")

                    inserted_games += 1
                    game_number += 1

                except Exception:

                    print("FAILED TO PROCESS GAME")

                    traceback.print_exc()

        print("====================================")
        print("UPLOAD COMPLETE")
        print("Games Uploaded:", inserted_games)
        print("====================================")

        return {
            "success": True,
            "games_uploaded": inserted_games,
            "upload_session_id": upload_session_id
        }

    except Exception:

        traceback.print_exc()

        return {
            "success": False,
            "error": "Upload failed."
        }