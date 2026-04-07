# main.py
import io
import chess.pgn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ChessBuddy AI")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend is alive"}

@app.post("/upload_pgn")
async def upload_pgn(file: UploadFile = File(...)):
    try:
        content = (await file.read()).decode("utf-8").strip()
        if not content:
            return JSONResponse({"error": "Empty PGN"}, status_code=400)

        pgn_io = io.StringIO(content)
        game = chess.pgn.read_game(pgn_io)
        if not game:
            return JSONResponse({"error": "Invalid PGN"}, status_code=400)

        board = game.board()
        moves_list = []
        for move in game.mainline_moves():
            moves_list.append(board.san(move))  # ✅ Use SAN for frontend
            board.push(move)

        return {"moves": moves_list}

    except Exception as e:
        return JSONResponse({"error": f"Failed to parse PGN: {str(e)}"}, status_code=400)