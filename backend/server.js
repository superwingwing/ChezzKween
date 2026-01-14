import express from "express";
import multer from "multer";
import fs from "fs";
import cors from "cors";
import { generateVideoWithAnalysis, progress } from "./videoGenerator.js";
import { Chess } from "chess.js";

const app = express();
app.use(cors());
app.use(express.static("public"));

const upload = multer({ dest: "uploads/" });

// PGN Upload
app.post("/upload", upload.single("pgn"), async (req, res) => {
  try {
    const pgn = fs.readFileSync(req.file.path, "utf8");

    const moves = parsePGN(pgn);

    const videoPath = await generateVideoWithAnalysis(moves);

    fs.unlinkSync(req.file.path);

    res.json({ status: "success", videoUrl: "/" + videoPath });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Video generation failed" });
  }
});


// Progress endpoint
app.get("/progress", (req, res) => {
  res.json({ progress });
});


//parsepgn
function parsePGN(pgn) {
  const chess = new Chess();

  try {
    chess.loadPgn(pgn, { sloppy: true }); // use RAW PGN
  } catch (e) {
    console.error("PGN parse error:", e);
    throw new Error("Invalid PGN");
  }

  return chess.history(); // returns all moves
}

// Endpoint to list all generated videos
app.get("/videos", (req, res) => {
  try {
    const files = fs.readdirSync("public")
      .filter(f => f.endsWith(".mp4")) // only video files
      .map(f => "/" + f); // prepend slash for static serving

    res.json({ videos: files });
  } catch (err) {
    console.error("Error reading public folder:", err);
    res.status(500).json({ videos: [] });
  }
});



app.listen(3000, () => {
  console.log("Backend running at http://localhost:3000");
});
