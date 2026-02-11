# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from video.video_generator import generate_video
import os

# --- Directories ---
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- FastAPI app ---
app = FastAPI(title="ChessBuddy AI")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Serve static files ---
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")

# --- Root endpoint ---
@app.get("/")
def root():
    return {"message": "Backend is alive"}

# --- Upload PGN endpoint ---
@app.post("/upload_pgn")
async def upload_pgn(file: UploadFile = File(...)):
    try:
        pgn_bytes = await file.read()
        pgn_text = pgn_bytes.decode("utf-8").strip()
        print("Received PGN content:", pgn_text[:500])  # first 500 chars

        final_video_path = generate_video(pgn_text)

        return JSONResponse({
            "message": "Video generated successfully",
            "video_url": f"/output/{os.path.basename(final_video_path)}"
        })

    except Exception as e:
        print("Error generating video:", e)
        return JSONResponse({"error": f"Failed to generate video: {str(e)}"}, status_code=400)

    try:
        pgn_text = (await file.read()).decode("utf-8").strip()
        if not pgn_text:
            return JSONResponse({"error": "PGN file is empty"}, status_code=400)

        final_video_path = generate_video(pgn_text)

        return JSONResponse({
            "message": "Video generated successfully",
            "video_url": f"/output/{os.path.basename(final_video_path)}"
        })

    except Exception as e:
        # Show clear error
        return JSONResponse({"error": f"Failed to generate video: {str(e)}"}, status_code=400)

# --- List all videos ---
@app.get("/videos")
def list_videos():
    files = os.listdir(OUTPUT_DIR)
    videos = [f"/output/{f}" for f in files if f.endswith(".mp4")]
    return {"videos": videos}
