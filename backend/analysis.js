// analysis.js
import { Chess } from "chess.js";
import { spawn } from "child_process";
import path from "path";

/**
 * Evaluate a position with Stockfish
 * @param {string} fen - FEN string of current position
 * @param {string} enginePath - path to Stockfish exe
 * @returns {Promise<{bestMove: string, evalScore: number}>}
 */
export function evaluatePosition(
  fen,
  enginePath = path.join(".", "stockfish.exe")
) {
  return new Promise((resolve) => {
    const engine = spawn(enginePath);
    let bestMove = "";
    let evalScore = 0;

    engine.stdout.on("data", (data) => {
      const lines = data.toString().split("\n");
      lines.forEach((line) => {
        if (line.includes("score cp")) {
          // Example line: "info depth 12 score cp 34 ..."
          const match = line.match(/score cp (-?\d+)/);
          if (match) evalScore = parseInt(match[1]);
        }

        if (line.startsWith("bestmove")) {
          bestMove = line.split(" ")[1];
          engine.kill();
          resolve({ bestMove, evalScore });
        }
      });
    });

    engine.stdin.write("uci\n");
    engine.stdin.write("ucinewgame\n");
    engine.stdin.write(`position fen ${fen}\n`);
    engine.stdin.write("go depth 12\n");
  });
}

/**
 * Analyze a PGN and return moves with category, best move, and evaluation
 * @param {string} pgn
 * @returns {Promise<Array>}
 */
export async function analyzePGN(pgn) {
  const chess = new Chess();
  chess.loadPgn(pgn, { sloppy: true });
  const moves = chess.history();
  const results = [];

  chess.reset();

  for (const move of moves) {
    const fenBefore = chess.fen();

    // Evaluate the position before the move
    const best = await evaluatePosition(fenBefore);

    // Play the actual move
    const playedMove = chess.move(move, { sloppy: true });

    // Evaluate the position after the move
    const played = await evaluatePosition(chess.fen());

    const cpLoss = Math.abs(played.evalScore - best.evalScore);

    // Categorize move
    let category = "Blunder";
    if (move === best.bestMove) category = "Best";
    else if (cpLoss < 20) category = "Excellent";
    else if (cpLoss < 50) category = "Good Move";
    else if (cpLoss < 150) category = "Mistake";

    results.push({
      move,
      from: playedMove.from,
      to: playedMove.to,
      bestMove: best.bestMove,
      category,
      evalBest: best.evalScore,
      evalPlayed: played.evalScore,
    });
  }

  return results;
}
