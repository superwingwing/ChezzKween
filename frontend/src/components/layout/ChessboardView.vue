<script setup>
import { ref, computed } from "vue"
import { Chess } from "chess.js"
import { TheChessboard } from "vue3-chessboard"
import "vue3-chessboard/style.css"
import MoveQuality from "@/components/layout/MoveQuality.vue"
import EvaluationBarView from "@/components/layout/EvaluationBarView.vue"

const chess = new Chess()
let boardAPI = null
const evalScore = ref(0)
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

/* =========================================
   COMPUTED
========================================= */

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

const qualityPosition = computed(() => {
  const analysis = currentAnalysis.value

  if (!analysis?.move) {
    return null
  }

  const move = analysis.move

  const squareMatch = move.match(/[a-h][1-8]$/)

  return squareMatch
    ? squareMatch[0]
    : null
})

/* =========================================
   ANALYSIS
========================================= */

function updateAnalysis(analysis) {
  console.log("========== MOVE QUALITY DEBUG ==========")
  console.log("FULL ANALYSIS:", analysis)
  console.log("QUALITY:", analysis?.quality)
  console.log("MOVE:", analysis?.move)
  console.log("TO SQUARE:", analysis?.to_square)
  console.log("EVALUATION:", analysis?.evaluation)
  console.log("BEST MOVE:", analysis?.best_move)
  console.log("========================================")

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

  evalScore.value = Number(
    analysis.evaluation || 0
  )

  emit(
    "update-eval",
    evalScore.value
  )

  emit(
    "update-coach",
    analysis
  )

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

/* =========================================
   BRANCH / VARIATION
========================================= */

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
      promotion:
        move.promotion || undefined
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

/* =========================================
   PGN NAVIGATION
========================================= */

function goToPGN(index) {
  if (isAnalyzingMove.value) {
    return
  }

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
  if (isAnalyzingMove.value) {
    return
  }

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
  if (isAnalyzingMove.value) {
    return
  }

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

/* =========================================
   MANUAL BOARD MOVE
========================================= */

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
        `${import.meta.env.VITE_API_URL}/analyze-move`,
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

/* =========================================
   BOARD ORIENTATION
========================================= */

function flipBoard() {
  orientation.value =
    orientation.value === "white"
      ? "black"
      : "white"

  if (boardAPI) {
    boardAPI.toggleOrientation()
  }
}

/* =========================================
   LOAD PGN
========================================= */

async function loadMoves(response) {
  try {
    console.log(
      "UPLOAD RESPONSE:",
      response
    )

    let game = null

    if (response?.game) {
      if (
        Array.isArray(
          response.game.data
        )
      ) {
        game =
          response.game.data[0]
      } else {
        game =
          response.game.data ||
          response.game
      }
    }

    if (!game) {
      console.error(
        "Could not find uploaded game:",
        response
      )

      return
    }

    console.log(
      "GAME DATA:",
      game
    )

    if (!game.pgn) {
      console.error(
        "Uploaded game has no PGN:",
        game
      )

      return
    }

    currentGame.value = game

    const pgnChess = new Chess()

    pgnChess.loadPgn(
      game.pgn
    )

    const history =
      pgnChess.history()

    console.log(
      "PGN MOVES:",
      history
    )

    if (!history.length) {
      console.error(
        "PGN contains no moves"
      )

      return
    }

    pgnMoves.value =
      [...history]

    pgnEvaluations.value = []
    pgnIndex.value = 0

    resetBranch()

    currentAnalysis.value = null
    analysisCache.value = {}

    orientation.value = "white"

    chess.reset()

    if (boardAPI) {
      boardAPI.setPosition(
        chess.fen()
      )

      boardAPI.hideMoves()
    }

    const data =
      response.analysis

    console.log(
      "PGN ANALYSIS:",
      data
    )

    if (!data) {
      console.error(
        "No analysis returned"
      )

      return
    }

    if (data.error) {
      console.error(
        "PGN analysis error:",
        data.error
      )

      return
    }

    pgnEvaluations.value =
      data.evaluations || []

    console.log(
      "PGN EVALUATIONS:",
      pgnEvaluations.value
    )

    goToPGN(0)

  } catch (error) {
    console.error(
      "PGN loading failed:",
      error
    )
  }
}

defineExpose({
  loadMoves
})
</script>

<template>
  <div class="chessboard-container">
    <!-- =====================================
         TOP PLAYER
    ====================================== -->

    <div class="player-card">

      <div class="player-avatar">
        <v-icon size="18">
          mdi-chess-king
        </v-icon>
      </div>

      <div class="player-details">

        <div class="player-name">
          {{ topPlayer.name || "Player" }}

          <span
            v-if="topPlayer.elo"
            class="player-elo"
          >
            {{ topPlayer.elo }}
          </span>
        </div>

        <div class="player-side">
          {{ orientation === "white"
            ? "Black"
            : "White"
          }}
          • Playing
        </div>

      </div>

      <div
        v-if="currentAnalysis"
        class="captured-info"
      >
        <span>Analysis</span>
        <strong>
          {{ currentAnalysis.quality || "Ready" }}
        </strong>
      </div>

    </div>

    <!-- =====================================
         CHESSBOARD
    ====================================== -->

    <div class="board-section">

      <div class="board-row">

        <TheChessboard
          class="board"
          :orientation="orientation"
          :board-config="{
            coordinates: true
          }"
          @move="onMove"
          @board-created="
            (api) => (boardAPI = api)
          "
        />

        <EvaluationBarView
          class="evaluation-bar"
          :score="evalScore"
        />

        <MoveQuality
          :quality="currentQuality"
          :square="qualityPosition"
          :orientation="orientation"
        />

      </div>

    </div>

    <!-- =====================================
         BOTTOM PLAYER
    ====================================== -->

    <div class="player-card bottom-player">

      <div class="player-avatar">

        <v-icon size="18">
          mdi-chess-king
        </v-icon>

      </div>

      <div class="player-details">

        <div class="player-name">

          {{ bottomPlayer.name || "Player" }}

          <span
            v-if="bottomPlayer.elo"
            class="player-elo"
          >
            {{ bottomPlayer.elo }}
          </span>

        </div>

        <div class="player-side">
          {{ orientation === "white"
            ? "White"
            : "Black"
          }}
          • Playing
        </div>

      </div>

      <div
        v-if="pgnMoves.length"
        class="move-counter"
      >
        {{ pgnIndex }} /
        {{ pgnMoves.length }}
      </div>

    </div>

    <!-- =====================================
         CONTROLS
    ====================================== -->

    <div class="controls">

      <v-btn
        class="control-btn"
        variant="flat"
        @click="prevMove"
        :disabled="isAnalyzingMove"
      >
        <v-icon size="17">
          mdi-chevron-left
        </v-icon>

        Back
      </v-btn>

      <v-btn
        class="control-btn"
        variant="flat"
        @click="nextMove"
        :disabled="isAnalyzingMove"
      >
        Forward

        <v-icon size="17">
          mdi-chevron-right
        </v-icon>
      </v-btn>

      <v-btn
        class="control-btn"
        variant="flat"
        @click="flipBoard"
      >
        <v-icon size="16">
          mdi-swap-vertical
        </v-icon>

        Flip
      </v-btn>

    </div>

    <!-- =====================================
         EXPLORATION STATUS
    ====================================== -->

    <div
      v-if="isExploring"
      class="exploration-status"
    >

      <v-icon
        size="15"
        color="#F28C28"
      >
        mdi-source-branch
      </v-icon>

      Exploring variation

      <span v-if="isAnalyzingMove">
        — Analyzing...
      </span>

    </div>

  </div>
</template>

<style scoped>

/* =========================================
   CHESSBOARD CONTAINER
========================================= */

.chessboard-container {
  width: 100%;
  max-width: 620px;
  margin: 0 auto;
  padding: 0;
  box-sizing: border-box;
}


/* =========================================
   UPLOAD
========================================= */

.upload-container {
  width: 100%;
  margin: 0 0 10px;
  padding: 0;
}


/* =========================================
   PLAYER CARD
========================================= */

.player-card {
  width: min(600px, 100%);

  min-height: 54px;

  margin: 0 auto 8px;

  padding: 8px 12px;

  display: flex;
  align-items: center;

  gap: 10px;

  box-sizing: border-box;

  background:
    linear-gradient(
      135deg,
      #0B1F3A,
      #07172D
    );

  border: 1px solid
    rgba(255, 255, 255, 0.06);

  border-radius: 10px;

  color: white;

  box-shadow:
    0 8px 20px
    rgba(7, 23, 45, 0.16);
}


/* =========================================
   PLAYER AVATAR
========================================= */

.player-avatar {
  width: 34px;
  height: 34px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 8px;

  background:
    rgba(255, 255, 255, 0.10);

  color: #F28C28;

  border: 1px solid
    rgba(242, 140, 40, 0.25);
}


/* =========================================
   PLAYER DETAILS
========================================= */

.player-details {
  min-width: 0;
  flex: 1;
}

.player-name {
  display: flex;
  align-items: center;

  gap: 6px;

  min-width: 0;

  font-size: 13px;
  font-weight: 700;

  color: #ffffff;

  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.player-elo {
  color: #F28C28;

  font-size: 11px;
  font-weight: 700;

  flex-shrink: 0;
}

.player-side {
  margin-top: 2px;

  font-size: 10px;

  color:
    rgba(255, 255, 255, 0.58);
}


/* =========================================
   ANALYSIS INFO
========================================= */

.captured-info,
.move-counter {
  flex-shrink: 0;

  display: flex;
  align-items: center;

  gap: 5px;

  padding: 6px 9px;

  border-radius: 6px;

  background:
    rgba(255, 255, 255, 0.08);

  border: 1px solid
    rgba(255, 255, 255, 0.08);

  font-size: 10px;

  color:
    rgba(255, 255, 255, 0.60);
}

.captured-info strong,
.move-counter {
  color: #F28C28;
}


/* =========================================
   BOARD SECTION
========================================= */

.board-section {
  width: 100%;

  display: flex;
  justify-content: center;

  margin: 0;
  padding: 0;
}


/* =========================================
   BOARD + EVALUATION BAR
========================================= */

.board-row {
  position: relative;

  display: flex;
  align-items: stretch;

  gap: 0;

  width: min(618px, 100%);

  margin: 0 auto;
  padding: 0;

  box-sizing: border-box;
}

.board {
  display: block;

  width: min(600px, 100%);

  max-width: 100%;

  margin: 0;
  padding: 0;

  flex: 0 1 600px;

  overflow: hidden;

  border-radius: 9px;
}


/* =========================================
   EVALUATION BAR
========================================= */

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
   BOTTOM PLAYER
========================================= */

.bottom-player {
  margin-top: 8px;
  margin-bottom: 0;
}


/* =========================================
   CONTROLS
========================================= */

.controls {
  width: 100%;

  display: flex;
  justify-content: center;
  align-items: center;

  gap: 7px;

  flex-wrap: wrap;

  margin: 12px auto 0;
  padding: 0;
}

.control-btn {
  height: 34px !important;

  min-width: 88px;

  padding: 0 13px !important;

  border-radius: 7px !important;

  background: #0B1F3A !important;

  color: #ffffff !important;

  font-size: 12px;

  font-weight: 600;

  text-transform: none;

  box-shadow: none;

  transition:
    background 0.2s ease,
    transform 0.2s ease;
}

.control-btn:hover {
  background: #F28C28 !important;

  color: #ffffff !important;

  transform: translateY(-1px);
}

.control-btn:disabled {
  opacity: 0.45;
}


/* =========================================
   EXPLORATION
========================================= */

.exploration-status {
  width: fit-content;

  margin: 9px auto 0;
  padding: 6px 11px;

  display: flex;
  align-items: center;

  gap: 5px;

  border-radius: 6px;

  background: #FFF3E4;

  color: #DC7311;

  border: 1px solid
    rgba(242, 140, 40, 0.25);

  font-size: 11px;

  font-weight: 600;
}


/* =========================================
   TABLET
========================================= */

@media (max-width: 960px) {

  .chessboard-container {
    max-width: 100%;
  }

  .board-row {
    width: 100%;
  }

  .board {
    width: min(600px, 100%);
  }

  .evaluation-bar {
    width: 16px;
    min-width: 16px;
    flex-basis: 16px;
  }

  .player-card {
    min-height: 50px;
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
    margin-bottom: 7px;
  }

  .board-row {
    width: 100%;
  }

  .board {
    width: calc(100% - 14px);

    flex: 1 1 auto;

    border-radius: 6px;
  }

  .evaluation-bar {
    width: 14px;
    min-width: 14px;
    flex-basis: 14px;
  }

  .player-card {
    min-height: 46px;

    padding: 7px 9px;

    margin-bottom: 6px;

    border-radius: 8px;

    gap: 8px;
  }

  .player-avatar {
    width: 30px;
    height: 30px;
  }

  .player-name {
    font-size: 12px;
  }

  .player-elo {
    font-size: 10px;
  }

  .player-side {
    font-size: 9px;
  }

  .captured-info {
    display: none;
  }

  .bottom-player {
    margin-top: 6px;
  }

  .controls {
    gap: 5px;
    margin-top: 9px;
  }

  .control-btn {
    min-width: 76px;

    height: 31px !important;

    padding: 0 9px !important;

    font-size: 11px;
  }

  .exploration-status {
    font-size: 10px;
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

  .player-card {
    min-height: 42px;

    padding: 6px 7px;
  }

  .player-avatar {
    width: 27px;
    height: 27px;
  }

  .player-name {
    font-size: 11px;
  }

  .player-side {
    font-size: 8px;
  }

  .move-counter {
    font-size: 9px;
    padding: 5px 7px;
  }

  .control-btn {
    min-width: 70px;

    height: 29px !important;

    font-size: 10px;
  }
}

</style>