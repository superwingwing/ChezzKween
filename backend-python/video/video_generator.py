import os, io, chess, chess.pgn, chess.svg, cairosvg, subprocess
from gtts import gTTS
from engine.stockfish_wrapper import evaluate_move

FRAMES_DIR = "frames"
OUTPUT_DIR = "output"
os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

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

    for idx, move in enumerate(game.mainline_moves()):
        board.push(move)
        # SVG -> PNG frame
        svg_path = f"{FRAMES_DIR}/frame_{idx}.svg"
        png_path = f"{FRAMES_DIR}/frame_{idx}.png"
        with open(svg_path, "w") as f:
            f.write(chess.svg.board(board=board))
        cairosvg.svg2png(url=svg_path, write_to=png_path)

        # Stockfish evaluation
        comment = evaluate_move(board, move, idx)
        move_comments.append(comment)

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
    framerate = max(1, int(total_moves / (10*60)))  # 10 min video
    video_path = generate_video_from_frames(framerate)
    audio_path = generate_audio_from_commentary(move_comments)
    final_path = merge_audio_video(video_path, audio_path)
    return final_path
