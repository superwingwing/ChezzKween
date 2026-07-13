from fastapi import APIRouter, UploadFile, File
from supabase import create_client
from dotenv import load_dotenv

import chess.pgn
import io
import uuid
import os
import traceback

from ml.feature_extractor import extract_features


# ==========================================
# Supabase
# ==========================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


router = APIRouter()


# ==========================================
# Extract Moves
# ==========================================

def extract_moves(game):

    board = game.board()

    moves = []

    for move in game.mainline_moves():

        moves.append(
            board.san(move)
        )

        board.push(move)

    return " ".join(moves)



# ==========================================
# Upload Style PGN(s)
# ==========================================

@router.post("/upload_style")
async def upload_style(
    files: list[UploadFile] = File(...)
):

    print("==============================")
    print("STYLE UPLOAD STARTED")
    print("FILES:", len(files))
    print("==============================")


    upload_session_id = str(
        uuid.uuid4()
    )


    inserted_games = 0


    # ======================================
    # Loop Uploaded Files
    # ======================================

    for file in files:


        print(
            "Processing:",
            file.filename
        )


        content = await file.read()


        text = content.decode(
            "utf-8",
            errors="ignore"
        )


        stream = io.StringIO(text)


        game_number = 1



        # ==================================
        # Multiple Games In One PGN
        # ==================================

        while True:


            game = chess.pgn.read_game(
                stream
            )


            if game is None:
                break



            try:


                # ==========================
                # Feature Extraction
                # ==========================

                features = extract_features(
                    game
                )


                print(
                    "Extracted:",
                    game_number
                )



                # ==========================
                # Original PGN
                # ==========================

                features["pgn"] = str(
                    game
                )



                # ==========================
                # Moves
                # ==========================

                features["moves"] = extract_moves(
                    game
                )



                # ==========================
                # Upload Information
                # ==========================

                features[
                    "upload_session_id"
                ] = upload_session_id


                features[
                    "game_number"
                ] = game_number



                # ==========================
                # Insert Database
                # ==========================

                result = (
                    supabase
                    .table("style")
                    .insert(features)
                    .execute()
                )


                print(
                    "Inserted:",
                    result.data
                )


                inserted_games += 1

                game_number += 1



            except Exception as e:


                print(
                    "GAME FAILED"
                )

                traceback.print_exc()



    return {


        "message":
            "Style upload complete",


        "games_uploaded":
            inserted_games,


        "upload_session_id":
            upload_session_id

    }