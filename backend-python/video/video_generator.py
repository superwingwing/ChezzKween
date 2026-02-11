# video/video_generator.py
import os
import io
import re
import subprocess
import chess
import chess.pgn
import chess.svg
import cairosvg
from gtts import gTTS
import chess.engine

# --- Directories ---
FRAMES_DIR = "frames"
OUTPUT_DIR = "output"
os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

STOCKFISH_PATH = "stockfish.exe"  # adjust path if needed

# --- Helpers ---
def clear_frames():
    for f in os.listdir(FRAMES_DIR):
        os.remove(os.path.join(FRAMES_DIR, f))

def evaluate_move(board, move, idx):
    """Simple Stockfish evaluation."""
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    try:
        info = engine.analyse(board, chess.engine.Limit(depth=12))
        score = info['score'].white().score(mate_score=10000)
    except Exception:
        score = None
    finally:
        engine.quit()

    try:
        san_move = board.san(move)
    except Exception:
        san_move = str(move)

    comment = f"Move {idx+1}: {san_move}"
    if score is not None:
        if score > 50:
            comment += " is strong for White."
        elif score < -50:
            comment += " is strong for Black."
        else:
            comment += " is balanced."
    return comment

def generate_frames_with_commentary(pgn_text):
    """Generate frames safely from any PGN."""
    clear_frames()
    move_comments = []

    # Clean PGN: remove BOM and CurrentPosition headers
    pgn_text = pgn_text.replace("\ufeff", "").strip()
    pgn_text_clean = re.sub(r'\[CurrentPosition.*\]', '', pgn_text)

    # Parse PGN
    game = chess.pgn.read_game(io.StringIO(pgn_text_clean))
    if game is None:
        raise ValueError("Invalid PGN file")

    # Start from standard board
    board = game.board()

    for idx, move in enumerate(game.mainline_moves()):
        # Only push legal moves
        if move in board.legal_moves:
            board.push(move)

            # Generate frame
            svg_path = f"{FRAMES_DIR}/frame_{idx}.svg"
            png_path = f"{FRAMES_DIR}/frame_{idx}.png"
            with open(svg_path, "w") as f:
                f.write(chess.svg.board(board=board))
            cairosvg.svg2png(url=svg_path, write_to=png_path)

            # Evaluate move
            comment = evaluate_move(board, move, idx)
            move_comments.append(comment)
        else:
            # Skip illegal moves safely
            print(f"Skipping illegal move: {move}")

    if not move_comments:
        raise ValueError("No valid moves found in PGN")

    return move_comments, len(move_comments)

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
    framerate = max(1, int(total_moves / (10 * 60)))  # ~10 min video
    video_path = generate_video_from_frames(framerate)
    audio_path = generate_audio_from_commentary(move_comments)
    final_path = merge_audio_video(video_path, audio_path)
    return final_path
