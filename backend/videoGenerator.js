import fs from "fs";
import path from "path";
import { createCanvas, loadImage } from "canvas";
import ffmpeg from "fluent-ffmpeg";
import { Chess } from "chess.js";
import { analyzePGN } from "./analysis.js";
import { generateExplanation, speakExplanationToFile } from "./explain.js";
import { createRequire } from "module";

/* ---------- FFMPEG SETUP ---------- */
const require = createRequire(import.meta.url);
const ffprobeStatic = require("ffprobe-static");
ffmpeg.setFfprobePath(ffprobeStatic.path);

/* ---------- GLOBAL ---------- */
let progress = 0;
export { progress };

const FPS = 10;

/* ---------- HELPERS ---------- */
function getAudioDuration(file) {
  return new Promise((res, rej) => {
    ffmpeg.ffprobe(file, (err, meta) => {
      if (err) return rej(err);
      const a = meta.streams.find((s) => s.codec_type === "audio");
      res(parseFloat(a.duration));
    });
  });
}

function lerp(a, b, t) {
  return a + (b - a) * t;
}

/* MERGE ALL AUDIOS */
function mergeAudios(files, out) {
  return new Promise((res, rej) => {
    const txt = files.map((f) => `file '${path.resolve(f)}'`).join("\n");

    fs.writeFileSync("audios.txt", txt);

    ffmpeg()
      .input("audios.txt")
      .inputOptions(["-f concat", "-safe 0"])
      .outputOptions(["-c copy"])
      .on("end", res)
      .on("error", rej)
      .save(out);
  });
}

/* ---------- MAIN ---------- */
export async function generateVideoWithAnalysis(pgn) {
  const framesDir = "frames";
  const audioDir = "temp_audios";

  if (!fs.existsSync(framesDir)) fs.mkdirSync(framesDir);
  if (!fs.existsSync(audioDir)) fs.mkdirSync(audioDir);

  fs.readdirSync(framesDir).forEach((f) =>
    fs.unlinkSync(path.join(framesDir, f)),
  );
  fs.readdirSync(audioDir).forEach((f) =>
    fs.unlinkSync(path.join(audioDir, f)),
  );

  const chess = new Chess();
  const size = 800;
  const sq = size / 8;

  /* LOAD PIECES */
  const pieces = {};
  for (const f of fs.readdirSync("pieces")) {
    pieces[path.basename(f, ".png")] = await loadImage(`pieces/${f}`);
  }

  progress = 10;
  const moves = await analyzePGN(pgn);
  progress = 30;

  let frameIndex = 1;
  const audios = [];

  /* ---------- GENERATE ---------- */
  for (let i = 0; i < moves.length; i++) {
    const m = moves[i];
    const prev = chess.board();
    chess.move({ from: m.from, to: m.to, promotion: "q" });
    const next = chess.board();

    /* AUDIO */
    const audio = await speakExplanationToFile(generateExplanation(m), i);
    audios.push(audio);

    const dur = await getAudioDuration(audio);
    const frames = Math.ceil(dur * FPS);

    for (let f = 0; f < frames; f++) {
      const t = f / frames;
      const cv = createCanvas(size, size);
      const ctx = cv.getContext("2d");

      /* BOARD */
      for (let r = 0; r < 8; r++)
        for (let c = 0; c < 8; c++) {
          ctx.fillStyle = (r + c) % 2 ? "#b58863" : "#f0d9b5";
          ctx.fillRect(c * sq, r * sq, sq, sq);
        }

      /* PIECES */
      for (let r = 0; r < 8; r++)
        for (let c = 0; c < 8; c++) {
          const p0 = prev[r][c];
          const p1 = next[r][c];

          if (p0 && m.from) {
            const fc = m.from.charCodeAt(0) - 97;
            const fr = 8 - m.from[1];
            const tc = m.to.charCodeAt(0) - 97;
            const tr = 8 - m.to[1];

            const img = pieces[p0.color + p0.type.toUpperCase()];

            ctx.drawImage(
              img,
              lerp(fc, tc, t) * sq,
              lerp(fr, tr, t) * sq,
              sq,
              sq,
            );
          } else if (p1) {
            const img = pieces[p1.color + p1.type.toUpperCase()];

            ctx.drawImage(img, c * sq, r * sq, sq, sq);
          }
        }

      /* TEXT */
      ctx.fillStyle = "white";
      ctx.font = "28px Arial";
      ctx.fillText(`Move ${i + 1}: ${m.move} (${m.category})`, 10, size - 20);

      fs.writeFileSync(`${framesDir}/frame_${frameIndex}.png`, cv.toBuffer());
      frameIndex++;
    }

    progress = 30 + Math.floor(((i + 1) / moves.length) * 40);
  }

  /* ---------- AUDIO MERGE ---------- */
  const finalAudio = "final_audio.wav";
  await mergeAudios(audios, finalAudio);

  /* ---------- VIDEO ---------- */
  const finalVideo = `public/video-${Date.now()}.mp4`;

  await new Promise((res, rej) => {
    ffmpeg()
      .addInput(`${framesDir}/frame_%d.png`)
      .inputOptions(["-start_number 1", `-framerate ${FPS}`])
      .addInput(finalAudio)
      .outputOptions([
        "-c:v libx264",
        "-pix_fmt yuv420p",
        "-c:a aac",
        "-shortest",
      ])
      .on("end", res)
      .on("error", rej)
      .save(finalVideo);
  });

  /* CLEAN */
  fs.unlinkSync(finalAudio);
  fs.readdirSync(framesDir).forEach((f) =>
    fs.unlinkSync(path.join(framesDir, f)),
  );

  progress = 100;
  return finalVideo;
}
