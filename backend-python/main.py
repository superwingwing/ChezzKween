from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from video.video_generator import generate_video
import os

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")

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
