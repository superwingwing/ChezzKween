// videoGenerator.js
import fs from "fs";
import path from "path";
import { createCanvas, loadImage } from "canvas";
import ffmpeg from "fluent-ffmpeg";
import { Chess } from "chess.js";
import say from "say";

// We'll export progress so your server can track it
let progress = 0;
export { progress };

// Main function
export async function generateVideoWithAnalysis(moves) {
  const framesDir = "frames";
  if (!fs.existsSync(framesDir)) fs.mkdirSync(framesDir);
  fs.readdirSync(framesDir).forEach((f) =>
    fs.unlinkSync(path.join(framesDir, f))
  );

  const chess = new Chess();
  const canvasSize = 800;
  const squareSize = canvasSize / 8;

  // Load piece images
  const pieceImages = {};
  const pieceFiles = fs.readdirSync("pieces");
  for (const file of pieceFiles) {
    const key = path.basename(file, ".png"); // e.g., wP, bK
    pieceImages[key] = await loadImage(path.join("pieces", file));
  }

  for (let i = 0; i < moves.length; i++) {
    const move = moves[i];
    const result = chess.move(move, { sloppy: true });
    if (!result) {
      console.warn(`Invalid move skipped: ${move}`);
      continue;
    }

    const canvas = createCanvas(canvasSize, canvasSize);
    const ctx = canvas.getContext("2d");

    // Draw board
    const lightColor = "#f0d9b5";
    const darkColor = "#b58863";
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        ctx.fillStyle = (row + col) % 2 === 0 ? lightColor : darkColor;
        ctx.fillRect(
          col * squareSize,
          row * squareSize,
          squareSize,
          squareSize
        );
      }
    }

    // Draw pieces
    const board = chess.board();
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        const piece = board[row][col];
        if (piece) {
          const key = piece.color + piece.type.toUpperCase(); // wP, bK
          const img = pieceImages[key];
          if (img)
            ctx.drawImage(
              img,
              col * squareSize,
              row * squareSize,
              squareSize,
              squareSize
            );
        }
      }
    }

    // Add move text
    ctx.fillStyle = "white";
    ctx.font = "28px Arial";
    ctx.fillText(`Move ${i + 1}: ${move}`, 10, canvasSize - 20);

    // Optional voice narration
    // await speakText(`Move ${i + 1}: ${move}`);

    // Save frame
    const buffer = canvas.toBuffer();
    fs.writeFileSync(`${framesDir}/frame${i}.png`, buffer);

    progress = Math.floor(((i + 1) / moves.length) * 80);
  }

  // Generate video
  const videoPath = `public/video-${Date.now()}.mp4`;
  await new Promise((resolve, reject) => {
    ffmpeg()
      .addInput(`${framesDir}/frame%d.png`)
      .inputOptions("-start_number 0")
      .inputFPS(1)
      .on("progress", (p) => {
        progress = 80 + Math.floor(p.percent / 5);
      })
      .on("error", (err) => {
        console.error("FFmpeg error:", err);
        reject(err);
      })
      .on("end", () => {
        progress = 100;
        resolve();
      })
      .output(videoPath)
      .run();
  });

  return videoPath;
}

// ---------------- Voice Narration ----------------
function speakText(text) {
  return new Promise((resolve) => {
    say.speak(text, "Alex", 1, resolve);
  });
}
