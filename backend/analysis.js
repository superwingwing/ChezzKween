// analysis.js
import { Chess } from "chess.js";
import { spawn } from "child_process";
import path from "path";

const ENGINE_PATH = path.join(".", "stockfish.exe");

/**
 * Evaluate a position using Stockfish
 */
export function evaluatePosition(fen) {
  return new Promise((resolve) => {
    const engine = spawn(ENGINE_PATH);

    let bestMove = "";
    let evalScore = 0;

    engine.stdout.on("data", (data) => {
      const lines = data.toString().split("\n");

      for (let line of lines) {
        // Read evaluation
        if (line.includes("score cp")) {
          const match = line.match(/score cp (-?\d+)/);
          if (match) evalScore = parseInt(match[1]);
        }

        // Mate detection
        if (line.includes("score mate")) {
          const match = line.match(/score mate (-?\d+)/);
          if (match) {
            evalScore = match[1] > 0 ? 10000 : -10000;
          }
        }

        // Read best move
        if (line.startsWith("bestmove")) {
          bestMove = line.split(" ")[1];
          engine.kill();
          resolve({ bestMove, evalScore });
        }
      }
    });

    engine.stdin.write("uci\n");
    engine.stdin.write("isready\n");
    engine.stdin.write("ucinewgame\n");
    engine.stdin.write(`position fen ${fen}\n`);
    engine.stdin.write("go depth 20\n"); // deeper = better
  });
}

/**
 * Analyze PGN
 */
export async function analyzePGN(pgn) {
  const chess = new Chess();
  chess.loadPgn(pgn, { sloppy: true });

  const moves = chess.history();
  const results = [];
  chess.reset();

  for (const move of moves) {
    const fenBefore = chess.fen();
    const best = await evaluatePosition(fenBefore);

    const playedMove = chess.move(move, { sloppy: true });

    const played = await evaluatePosition(chess.fen());

    const cpLoss = Math.abs(played.evalScore - best.evalScore);

    let category = "Blunder";
    if (move === best.bestMove) category = "Best";
    else if (cpLoss < 30) category = "Excellent";
    else if (cpLoss < 80) category = "Good Move";
    else if (cpLoss < 200) category = "Mistake";

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
