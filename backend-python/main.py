# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import os
import io
import chess
import chess.pgn
import chess.svg
import cairosvg
import subprocess
from gtts import gTTS
import chess.engine

# --- Directories ---
FRAMES_DIR = "frames"
OUTPUT_DIR = "output"

os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Serve static files ---
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")

# --- Helpers ---
def clear_frames():
    for f in os.listdir(FRAMES_DIR):
        os.remove(os.path.join(FRAMES_DIR, f))

def generate_frames_with_commentary(pgn_text):
    clear_frames()
    game = chess.pgn.read_game(io.StringIO(pgn_text))
    if game is None:
        raise ValueError("Invalid PGN file")

    board = game.board()
    move_comments = []

    engine = chess.engine.SimpleEngine.popen_uci("stockfish")  # adjust path

    for idx, move in enumerate(game.mainline_moves()):
        board.push(move)

        # SVG -> PNG frame
        svg_path = f"{FRAMES_DIR}/frame_{idx}.svg"
        png_path = f"{FRAMES_DIR}/frame_{idx}.png"
        with open(svg_path, "w") as f:
            f.write(chess.svg.board(board=board))
        cairosvg.svg2png(url=svg_path, write_to=png_path)

        # Stockfish evaluation
        info = engine.analyse(board, chess.engine.Limit(depth=12))
        score = info['score'].white().score(mate_score=10000)
        comment = f"Move {idx+1}: {board.san(move)}"
        if score is not None:
            if score > 50:
                comment += " is strong for White."
            elif score < -50:
                comment += " is strong for Black."
            else:
                comment += " is balanced."
        move_comments.append(comment)

    engine.quit()
    return move_comments, len(game.mainline_moves())

def generate_audio_from_commentary(move_comments):
    full_text = ". ".join(move_comments)
    tts = gTTS(full_text, lang="en")
    audio_path = os.path.join(OUTPUT_DIR, "audio.mp3")
    tts.save(audio_path)
    return audio_path

def generate_video_from_frames(framerate=1):
    output_path = os.path.join(OUTPUT_DIR, "video.mp4")
    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(framerate),
        "-i", f"{FRAMES_DIR}/frame_%d.png",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_path
    ])
    return output_path

def merge_audio_video(video_path, audio_path):
    final_path = os.path.join(OUTPUT_DIR, "final_tutorial.mp4")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-strict", "experimental",
        final_path
    ])
    return final_path

def generate_video(pgn_text):
    move_comments, total_moves = generate_frames_with_commentary(pgn_text)
    framerate = max(1, int(total_moves / (10 * 60)))  # 10 min video
    video_path = generate_video_from_frames(framerate)
    audio_path = generate_audio_from_commentary(move_comments)
    final_path = merge_audio_video(video_path, audio_path)
    return final_path

# --- API Endpoints ---
@app.post("/upload_pgn")
async def upload_pgn(file: UploadFile = File(...)):
    try:
        pgn_text = await file.read()
        pgn_text = pgn_text.decode("utf-8")
        final_video_path = generate_video(pgn_text)
        return JSONResponse({"video_url": f"/output/{os.path.basename(final_video_path)}"})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

@app.get("/videos")
def list_videos():
    files = os.listdir(OUTPUT_DIR)
    videos = [f"/output/{f}" for f in files if f.endswith(".mp4")]
    return {"videos": videos}
