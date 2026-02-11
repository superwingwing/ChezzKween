// explain.js
import say from "say";
import fs from "fs";
import path from "path";

if (!fs.existsSync("audio")) fs.mkdirSync("audio");

/**
 * Generate human explanation for a move
 */
export function generateExplanation(moveObj) {
  const { category, evalBest, evalPlayed, bestMove, move } = moveObj;

  const bestEval = (evalBest / 100).toFixed(2);
  const playedEval = (evalPlayed / 100).toFixed(2);
  const diff = (playedEval - bestEval).toFixed(2);

  let explanation = "";

  if (move === bestMove) {
    explanation = `
    Great choice! ${move} is the strongest move in this position.
    It keeps the evaluation at ${playedEval}.
    This move improves your position and follows sound chess principles.
    `;
  } else if (category === "Excellent") {
    explanation = `
    ${move} is an excellent move.
    The engine slightly prefers ${bestMove},
    but your move achieves similar goals.
    The difference is only ${Math.abs(diff)} pawns,
    so both moves are very strong.
    `;
  } else if (category === "Good Move") {
    explanation = `
    ${move} is a good move,
    but Stockfish prefers ${bestMove}.
    Your move slightly weakens the position,
    losing about ${Math.abs(diff)} pawns.
    Still, the position remains playable.
    `;
  } else if (category === "Mistake") {
    explanation = `
    ${move} is a mistake.
    The engine recommends ${bestMove} instead.
    This move loses about ${Math.abs(diff)} pawns,
    giving your opponent a noticeable advantage.
    `;
  } else {
    // Blunder
    explanation = `
    ${move} is a blunder.
    The best move was ${bestMove}.
    This changes the evaluation drastically
    and puts you in a losing position.
    `;
  }

  return explanation.replace(/\s+/g, " ");
}


/**
 * Save narration to WAV file for a move
 */
export function speakExplanationToFile(text, index) {
  return new Promise((resolve, reject) => {
    const filePath = path.join("audio", `move_${index}.wav`);
    say.export(text, "Microsoft David Desktop", 1, filePath, (err) => {
      if (err) reject(err);
      else resolve(filePath);
    });
  });
}
