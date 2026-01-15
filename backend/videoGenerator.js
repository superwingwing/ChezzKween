// videoGenerator.js
import fs from "fs";
import path from "path";
import { createCanvas, loadImage } from "canvas";
import ffmpeg from "fluent-ffmpeg";
import { Chess } from "chess.js";
import say from "say";
import { analyzePGN } from "./analysis.js";

// Export progress for server
let progress = 0;
export { progress };

/**
 * Generate chess video with dynamic move analysis
 * @param {string} pgn - PGN string of the game
 * @returns {string} path to generated video
 */
export async function generateVideoWithAnalysis(pgn) {
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

  // 1️⃣ Analyze PGN dynamically with Stockfish
  progress = 10;
  const analyzedMoves = await analyzePGN(pgn); // returns array with {move, from, to, category, bestMove, evalBest, evalPlayed}
  progress = 50;

  // 2️⃣ Generate frames
  for (let i = 0; i < analyzedMoves.length; i++) {
    const moveObj = analyzedMoves[i];

    // Make move on chess board
    chess.move({ from: moveObj.from, to: moveObj.to, promotion: "q" });

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

    // Draw move arrows
    if (moveObj.from && moveObj.to) {
      const fromCol = moveObj.from.charCodeAt(0) - "a".charCodeAt(0);
      const fromRow = 8 - parseInt(moveObj.from[1]);
      const toCol = moveObj.to.charCodeAt(0) - "a".charCodeAt(0);
      const toRow = 8 - parseInt(moveObj.to[1]);

      let arrowColor = "gray";
      switch (moveObj.category) {
        case "Book Move":
          arrowColor = "blue";
          break;
        case "Best":
          arrowColor = "green";
          break;
        case "Excellent":
          arrowColor = "lightgreen";
          break;
        case "Good Move":
          arrowColor = "yellow";
          break;
        case "Mistake":
          arrowColor = "orange";
          break;
        case "Blunder":
          arrowColor = "red";
          break;
      }

      ctx.strokeStyle = arrowColor;
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.moveTo(
        fromCol * squareSize + squareSize / 2,
        fromRow * squareSize + squareSize / 2
      );
      ctx.lineTo(
        toCol * squareSize + squareSize / 2,
        toRow * squareSize + squareSize / 2
      );
      ctx.stroke();
    }

    // Draw move text with category
    ctx.fillStyle = "white";
    ctx.font = "28px Arial";
    ctx.fillText(
      `Move ${i + 1}: ${moveObj.move} (${moveObj.category})`,
      10,
      canvasSize - 20
    );

    // Optional: voice narration
    // await speakText(`Move ${i + 1}: ${moveObj.move}. Category: ${moveObj.category}`);

    // Save frame
    const buffer = canvas.toBuffer();
    fs.writeFileSync(`${framesDir}/frame${i}.png`, buffer);

    progress = Math.floor(((i + 1) / analyzedMoves.length) * 50) + 50; // 50-100%
  }

  // 3️⃣ Generate video from frames
  const videoPath = `public/video-${Date.now()}.mp4`;
  await new Promise((resolve, reject) => {
    ffmpeg()
      .addInput(`${framesDir}/frame%d.png`)
      .inputOptions("-start_number 0")
      .inputFPS(1)
      .on("progress", (p) => {
        progress = 50 + Math.floor(p.percent / 2); // smooth 50-100%
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
