import { Chess } from "chess.js";
import { evaluatePosition } from "./analysis.js";

const game = new Chess();

game.move("e4");
game.move("c5");

const fen = game.fen();

evaluatePosition(fen).then(console.log);
