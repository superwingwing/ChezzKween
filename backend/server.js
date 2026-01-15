import express from "express";
import multer from "multer";
import fs from "fs";
import cors from "cors";
import { generateVideoWithAnalysis, progress } from "./videoGenerator.js";

const app = express();
app.use(cors());
app.use(express.static("public"));

const upload = multer({ dest: "uploads/" });

// PGN Upload endpoint
app.post("/upload", upload.single("pgn"), async (req, res) => {
  try {
    const pgn = fs.readFileSync(req.file.path, "utf8");

    if (!pgn || !pgn.includes("1.")) {
      return res.status(400).json({ error: "Invalid PGN" });
    }

    // Generate video directly from PGN (with dynamic analysis)
    const videoPath = await generateVideoWithAnalysis(pgn);

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

// List all generated videos
app.get("/videos", (req, res) => {
  try {
    const files = fs
      .readdirSync("public")
      .filter((f) => f.endsWith(".mp4"))
      .map((f) => "/" + f);

    res.json({ videos: files });
  } catch (err) {
    console.error("Error reading public folder:", err);
    res.status(500).json({ videos: [] });
  }
});

app.listen(3000, () => {
  console.log("Backend running at http://localhost:3000");
});
