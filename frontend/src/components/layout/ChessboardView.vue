<script setup>
import { ref, computed } from "vue"
import { Chess } from "chess.js"
import { TheChessboard } from "vue3-chessboard"
import "vue3-chessboard/style.css"
import UploadPGNModal from "@/components/layout/UploadPGNModal.vue"
import MoveQuality from "@/components/layout/MoveQuality.vue"
import EvaluationBarView from '@/components/layout/EvaluationBarView.vue'

const chess = new Chess()
let boardAPI = null
const evalScore = ref(0) //for the evaluation bar
const pgnMoves = ref([])
const pgnEvaluations = ref([])
const pgnIndex = ref(0)
const branchMoves = ref([])
const branchIndex = ref(0)
const branchStart = ref(null)
const currentGame = ref(null)
const currentAnalysis = ref(null)
const analysisCache = ref({})
const orientation = ref("white")
const isNavigating = ref(false)
const isAnalyzingMove = ref(false)

const emit = defineEmits([
  "update-eval",
  "update-coach"
])

const isExploring = computed(() =>
  branchStart.value !== null
)

const whitePlayer = computed(() => ({
  name: currentGame.value?.white_name,
  elo: currentGame.value?.white_elo
}))

const blackPlayer = computed(() => ({
  name: currentGame.value?.black_name,
  elo: currentGame.value?.black_elo
}))

const topPlayer = computed(() =>
  orientation.value === "white"
    ? blackPlayer.value
    : whitePlayer.value
)

const bottomPlayer = computed(() =>
  orientation.value === "white"
    ? whitePlayer.value
    : blackPlayer.value
)

const currentQuality = computed(() =>
  currentAnalysis.value?.quality || ""
)

const qualityPosition = computed(() =>
  currentAnalysis.value?.to_square || null
)

function updateAnalysis(analysis) {
  currentAnalysis.value = analysis || null

  if (!analysis) {
    evalScore.value = 0
    emit("update-eval", 0)
    emit("update-coach", null)

    if (boardAPI) {
      boardAPI.hideMoves()
    }

    return
  }

  evalScore.value = Number(analysis.evaluation || 0)

  emit("update-eval", evalScore.value)
  emit("update-coach", analysis)

  if (
    boardAPI &&
    typeof analysis.best_move === "string" &&
    analysis.best_move.length >= 4
  ) {
    boardAPI.hideMoves()

    boardAPI.drawMove(
      analysis.best_move.slice(0, 2),
      analysis.best_move.slice(2, 4),
      "green"
    )
  } else if (boardAPI) {
    boardAPI.hideMoves()
  }
}

function resetBranch() {
  branchMoves.value = []
  branchIndex.value = 0
  branchStart.value = null
}

function rebuildPGN(index) {
  chess.reset()

  for (let i = 0; i < index; i++) {
    const move = chess.move(
      pgnMoves.value[i]
    )

    if (!move) {
      console.error(
        "Failed to replay PGN move:",
        pgnMoves.value[i],
        "at index:",
        i
      )
      break
    }
  }
}

function rebuildBranch() {
  chess.reset()

  for (
    let i = 0;
    i < branchStart.value;
    i++
  ) {
    const move = chess.move(
      pgnMoves.value[i]
    )

    if (!move) {
      console.error(
        "Failed to replay PGN move:",
        pgnMoves.value[i]
      )
      return
    }
  }

  for (
    let i = 0;
    i < branchIndex.value;
    i++
  ) {
    const move = branchMoves.value[i]

    const played = chess.move({
      from: move.from,
      to: move.to,
      promotion: move.promotion || undefined
    })

    if (!played) {
      console.error(
        "Failed to replay branch move:",
        move
      )
      return
    }
  }
}

function setBoard() {
  if (boardAPI) {
    boardAPI.setPosition(
      chess.fen()
    )
  }
}

function goToPGN(index) {
  if (isAnalyzingMove.value) return

  isNavigating.value = true

  resetBranch()

  pgnIndex.value = Math.max(
    0,
    Math.min(
      index,
      pgnMoves.value.length
    )
  )

  rebuildPGN(
    pgnIndex.value
  )

  setBoard()

  if (pgnIndex.value === 0) {
    updateAnalysis(null)
  } else {
    updateAnalysis(
      pgnEvaluations.value[
        pgnIndex.value - 1
      ] || null
    )
  }

  isNavigating.value = false
}

function nextMove() {
  if (isAnalyzingMove.value) return

  if (isExploring.value) {
    if (
      branchIndex.value <
      branchMoves.value.length
    ) {
      branchIndex.value++

      rebuildBranch()
      setBoard()

      const analysis =
        branchMoves.value[
          branchIndex.value - 1
        ]?.analysis

      updateAnalysis(
        analysis || null
      )

      return
    }

    return
  }

  if (
    pgnIndex.value <
    pgnMoves.value.length
  ) {
    goToPGN(
      pgnIndex.value + 1
    )
  }
}

function prevMove() {
  if (isAnalyzingMove.value) return

  if (isExploring.value) {
    if (branchIndex.value > 0) {
      branchIndex.value--

      rebuildBranch()
      setBoard()

      if (branchIndex.value === 0) {
        if (branchStart.value === 0) {
          updateAnalysis(null)
        } else {
          updateAnalysis(
            pgnEvaluations.value[
              branchStart.value - 1
            ] || null
          )
        }

        return
      }

      const analysis =
        branchMoves.value[
          branchIndex.value - 1
        ]?.analysis

      updateAnalysis(
        analysis || null
      )

      return
    }

    const returnIndex =
      branchStart.value

    resetBranch()

    pgnIndex.value =
      returnIndex

    rebuildPGN(
      pgnIndex.value
    )

    setBoard()

    if (pgnIndex.value === 0) {
      updateAnalysis(null)
    } else {
      updateAnalysis(
        pgnEvaluations.value[
          pgnIndex.value - 1
        ] || null
      )
    }

    return
  }

  if (pgnIndex.value > 0) {
    goToPGN(
      pgnIndex.value - 1
    )
  }
}

async function onMove(move) {
  if (
    isNavigating.value ||
    isAnalyzingMove.value
  ) {
    return
  }

  const beforeFen =
    chess.fen()

  const moveUci = move.promotion
    ? `${move.from}${move.to}${move.promotion}`
    : `${move.from}${move.to}`

  const played = chess.move({
    from: move.from,
    to: move.to,
    promotion:
      move.promotion || "q"
  })

  if (!played) {
    console.error(
      "Illegal manual move:",
      move
    )
    return
  }

  if (!isExploring.value) {
    branchStart.value =
      pgnIndex.value

    branchMoves.value = []
    branchIndex.value = 0
  }

  if (
    branchIndex.value <
    branchMoves.value.length
  ) {
    branchMoves.value =
      branchMoves.value.slice(
        0,
        branchIndex.value
      )
  }

  const branchMove = {
    from: move.from,
    to: move.to,
    promotion:
      move.promotion || null,
    uci: moveUci,
    san: played.san,
    analysis: null
  }

  branchMoves.value.push(
    branchMove
  )

  branchIndex.value++

  try {
    isAnalyzingMove.value = true

    const cacheKey =
      `${beforeFen}_${moveUci}`

    if (
      analysisCache.value[cacheKey]
    ) {
      branchMove.analysis =
        analysisCache.value[cacheKey]

      updateAnalysis(
        branchMove.analysis
      )

      return
    }

    const response =
      await fetch(
        "http://localhost:8000/analyze-move",
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json"
          },
          body: JSON.stringify({
            fen: beforeFen,
            move_uci: moveUci
          })
        }
      )

    if (!response.ok) {
      throw new Error(
        `HTTP ${response.status}`
      )
    }

    const data =
      await response.json()

    if (data.error) {
      console.error(
        "Manual analysis error:",
        data.error
      )
      return
    }

    analysisCache.value[cacheKey] =
      data

    branchMove.analysis =
      data

    updateAnalysis(data)

  } catch (error) {
    console.error(
      "Manual move analysis failed:",
      error
    )
  } finally {
    isAnalyzingMove.value = false
  }
}

function flipBoard() {
  orientation.value =
    orientation.value === "white"
      ? "black"
      : "white"
}

async function loadMoves(response) {
  try {
    console.log(
      "UPLOAD RESPONSE:",
      response
    )

    let game = null

    if (Array.isArray(response)) {
      game = response[0]
    } else if (
      Array.isArray(response?.data)
    ) {
      game = response.data[0]
    } else if (response?.pgn) {
      game = response
    } else if (response?.data?.pgn) {
      game = response.data
    }

    if (!game) {
      console.error(
        "Could not find uploaded game:",
        response
      )
      return
    }

    if (!game.pgn) {
      console.error(
        "Uploaded game has no PGN:",
        game
      )
      return
    }

    console.log(
      "UPLOADED PGN:",
      game.pgn
    )

    currentGame.value =
      game

    const pgnChess =
      new Chess()

    pgnChess.loadPgn(
      game.pgn
    )

    const history =
      pgnChess.history()

    console.log(
      "PGN HISTORY:",
      history
    )

    if (!history.length) {
      console.error(
        "PGN contains no moves:",
        game.pgn
      )
      return
    }

    pgnMoves.value = [
      ...history
    ]

    console.log(
      "PGN MOVES STORED:",
      pgnMoves.value
    )

    pgnEvaluations.value = []
    pgnIndex.value = 0

    resetBranch()

    currentAnalysis.value =
      null

    analysisCache.value = {}

    orientation.value =
      "white"

    chess.reset()

    if (boardAPI) {
      boardAPI.setPosition(
        chess.fen()
      )

      boardAPI.hideMoves()
    }

    const res =
      await fetch(
        "http://localhost:8000/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json"
          },
          body: JSON.stringify({
            pgn: game.pgn
          })
        }
      )

    if (!res.ok) {
      throw new Error(
        `HTTP ${res.status}`
      )
    }

    const data =
      await res.json()

    console.log(
      "PGN ANALYSIS:",
      data
    )

    if (data.error) {
      console.error(
        "PGN analysis error:",
        data.error
      )
      return
    }

    pgnEvaluations.value =
      data.evaluations || []

    goToPGN(0)

  } catch (error) {
    console.error(
      "PGN loading failed:",
      error
    )
  }
}
</script>

<template>
  <div class="chessboard-container">

    <!-- Upload -->
    <div class="upload-container">
      <UploadPGNModal @loaded="loadMoves" />
    </div>

    <!-- Top Player -->
    <div class="player">
      <div class="player-info">
        <span class="name">
          {{ topPlayer.name || "Player" }}
        </span>

        <span class="rating">
          {{ topPlayer.elo || "--" }}
        </span>
      </div>
    </div>

    <!-- Board -->
    <div class="board-wrapper">
        <!-- Chessboard + Evaluation Bar -->
        <div class="board-row">

          <TheChessboard
            class="board"
            :orientation="orientation"
            @move="onMove"
            @board-created="(api) => (boardAPI = api)"
          />

          <EvaluationBarView
            class="evaluation-bar"
            :score="evalScore"
          />

          <MoveQuality
            :quality="currentQuality"
            :square="qualityPosition"
          />

        </div>

        <!-- Bottom Player -->
        <div class="player bottom-player">
          <div class="player-info">
            <span class="name">
              {{ bottomPlayer.name || "Player" }}
            </span>

            <span class="rating">
              {{ bottomPlayer.elo || "--" }}
            </span>
          </div>
        </div>
   </div>

    <!-- Controls -->
    <div class="controls">

      <v-btn
        class="control-btn"
        color="light-blue-darken-4"
        size="small"
        variant="flat"
        @click="prevMove"
        :disabled="isAnalyzingMove"
      >
        ⬅️ Back
      </v-btn>

      <v-btn
        class="control-btn"
        color="light-blue-darken-4"
        size="small"
        variant="flat"
        @click="nextMove"
        :disabled="isAnalyzingMove"
      >
        Forward ➡️
      </v-btn>

      <v-btn
        class="control-btn"
        color="light-blue-darken-4"
        size="small"
        variant="flat"
        @click="flipBoard"
      >
        🔄 Flip
      </v-btn>

    </div>

    <!-- Exploration -->
    <div
      v-if="isExploring"
      class="exploration-status"
    >
      Exploring variation

      <span v-if="isAnalyzingMove">
        — Analyzing...
      </span>
    </div>

  </div>
</template>

<style scoped>
/* =========================================
   MAIN CONTAINER
========================================= */

.chessboard-container {
  width: 100%;
  max-width: 620px;
  margin: 0 auto;
  padding: 0;
  text-align: center;
  box-sizing: border-box;
}

/* =========================================
   UPLOAD
========================================= */

.upload-container {
  width: 100%;
  margin: 0 0 4px;
  padding: 0;
}

/* =========================================
   BOARD + EVALUATION BAR
========================================= */

.board-wrapper {
  width: 100%;
  margin: 0;
  padding: 0;
}

.board-row {
  display: flex;
  align-items: stretch;
  gap: 0;
  width: 100%;
  margin: 0;
  padding: 0;
}

.board {
  display: block;
  width: min(600px, 100%);
  max-width: 100%;
  margin: 0;
  padding: 0;
  flex: 0 1 600px;
}

/* Evaluation bar */
.evaluation-bar {
  width: 18px;
  min-width: 18px;
  flex: 0 0 18px;
  height: auto;
  margin: 0;
  padding: 0;
  align-self: stretch;
}

/* =========================================
   PLAYER BAR
========================================= */

.player {
  display: flex;
  align-items: center;

  width: min(600px, 100%);

  height: 30px;
  min-height: 30px;

  margin: 2px auto;
  padding: 3px 9px;

  box-sizing: border-box;

  background: #01579B;
  color: white;

  border-radius: 5px;
}

/* Player information */

.player-info {
  display: flex;
  align-items: center;

  gap: 7px;

  min-width: 0;
  width: 100%;
}

/* Player name */

.name {
  min-width: 0;

  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

  font-size: 12px;
  font-weight: 600;
  line-height: 1;
}

/* Rating */

.rating {
  flex-shrink: 0;

  font-size: 10px;
  line-height: 1;

  color: rgba(255, 255, 255, 0.75);
}

/* Bottom player */

.bottom-player {
  margin: 2px auto 0;
}

/* =========================================
   CONTROLS
========================================= */

.controls {
  display: flex;
  justify-content: center;
  align-items: center;

  flex-wrap: wrap;

  gap: 5px;

  width: 100%;

  margin: 5px auto 0;
  padding: 0;
}

.control-btn {
  min-width: 82px;
  height: 32px !important;

  font-size: 12px;
  text-transform: none;
}

/* =========================================
   EXPLORATION
========================================= */

.exploration-status {
  width: 100%;

  margin: 4px auto 0;
  padding: 0;

  font-size: 12px;

  opacity: 0.75;
}

/* =========================================
   TABLET
========================================= */

@media (max-width: 960px) {
  .chessboard-container {
    max-width: 100%;
  }

  .board {
    width: min(600px, 100%);
  }

  .evaluation-bar {
    width: 16px;
    min-width: 16px;
    flex-basis: 16px;
  }

  .player {
    height: 29px;
    min-height: 29px;
    padding: 3px 8px;
  }

  .name {
    font-size: 12px;
  }

  .rating {
    font-size: 10px;
  }

  .controls {
    margin-top: 5px;
  }
}

/* =========================================
   MOBILE
========================================= */

@media (max-width: 600px) {
  .chessboard-container {
    width: 100%;
    padding: 0 2px;
  }

  .upload-container {
    margin-bottom: 2px;
  }

  .board-row {
    width: 100%;
  }

  .board {
    width: calc(100% - 14px);
    flex: 1 1 auto;
  }

  .evaluation-bar {
    width: 14px;
    min-width: 14px;
    flex: 0 0 14px;
  }

  .player {
    height: 27px;
    min-height: 27px;

    margin: 2px auto;
    padding: 3px 7px;

    border-radius: 4px;
  }

  .player-info {
    gap: 6px;
  }

  .name {
    font-size: 11px;
  }

  .rating {
    font-size: 9px;
  }

  .bottom-player {
    margin-top: 2px;
  }

  .controls {
    gap: 4px;
    margin-top: 4px;
  }

  .control-btn {
    min-width: 75px;
    height: 30px !important;
    font-size: 11px;
  }

  .exploration-status {
    font-size: 11px;
    margin-top: 3px;
  }
}

/* =========================================
   VERY SMALL PHONES
========================================= */

@media (max-width: 400px) {
  .chessboard-container {
    padding: 0;
  }

  .board {
    width: calc(100% - 12px);
  }

  .evaluation-bar {
    width: 12px;
    min-width: 12px;
    flex-basis: 12px;
  }

  .player {
    height: 25px;
    min-height: 25px;

    padding: 2px 6px;
  }

  .player-info {
    gap: 5px;
  }

  .name {
    font-size: 10px;
  }

  .rating {
    font-size: 8px;
  }

  .control-btn {
    min-width: 70px;
    height: 28px !important;
    font-size: 10px;
  }
}
</style>