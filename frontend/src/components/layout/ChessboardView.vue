<script setup>
import { ref, computed } from "vue"
import { Chess } from "chess.js"
import { TheChessboard } from "vue3-chessboard"
import "vue3-chessboard/style.css"
import UploadPGNModal from "@/components/layout/UploadPGNModal.vue"
import MoveQuality from "@/components/layout/MoveQuality.vue"

const chess = new Chess()
let boardAPI = null

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
    emit("update-eval", 0)
    emit("update-coach", null)

    if (boardAPI) {
      boardAPI.hideMoves()
    }

    return
  }

  emit(
    "update-eval",
    Number(analysis.evaluation || 0)
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
      <UploadPGNModal
        @loaded="loadMoves"
      />
    </div>

    <!-- Top Player -->
    <div class="player">
      <div class="player-info">
        <div class="name">
          {{ topPlayer.name || "Player" }}
        </div>

        <div class="rating">
          {{ topPlayer.elo || "--" }}
        </div>
      </div>
    </div>

    <!-- Board -->
    <div class="board-wrapper">

      <TheChessboard
        class="board"
        :orientation="orientation"
        @move="onMove"
        @board-created="
          (api) => (boardAPI = api)
        "
      />

      <MoveQuality
        :quality="currentQuality"
        :square="qualityPosition"
      />

      <!-- Bottom Player -->
      <div class="player bottom-player">
        <div class="player-info">
          <div class="name">
            {{ bottomPlayer.name || "Player" }}
          </div>

          <div class="rating">
            {{ bottomPlayer.elo || "--" }}
          </div>
        </div>
      </div>

    </div>

    <!-- Controls -->
    <div class="controls">

      <v-btn
        class="control-btn"
        @click="prevMove"
        :disabled="isAnalyzingMove"
      >
        ⬅️ Back
      </v-btn>

      <v-btn
        class="control-btn"
        @click="nextMove"
        :disabled="isAnalyzingMove"
      >
        Forward ➡️
      </v-btn>

      <v-btn
        class="control-btn"
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
.chessboard-container {
  width: 100%;
  max-width: 620px;
  margin: 0 auto;
  text-align: center;
}

.upload-container {
  width: 100%;
  margin-bottom: 10px;
}

.board-wrapper {
  position: relative;
  width: 100%;
  margin: 0 auto;
}

.board {
  width: min(600px, 100%);
  max-width: 100%;
  margin: 0 auto;
}

.player {
  display: flex;
  align-items: center;
  width: min(600px, 100%);
  min-height: 48px;
  margin: 10px auto;
  padding: 10px 14px;
  background: #8D6E63;
  border-radius: 8px;
  box-sizing: border-box;
}

.player-info {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  max-width: 100%;
}

.name {
  font-weight: bold;
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rating {
  flex-shrink: 0;
  font-size: 12px;
  color: #aaa;
}

.bottom-player {
  margin-top: 10px;
}

.controls {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  width: 100%;
  margin: 16px auto;
}

.control-btn {
  min-width: 90px;
}

.exploration-status {
  width: 100%;
  margin: 10px auto;
  font-size: 13px;
  opacity: 0.75;
}

@media (max-width: 960px) {
  .chessboard-container {
    max-width: 100%;
  }

  .board {
    width: min(600px, 100%);
  }
}

@media (max-width: 600px) {
  .chessboard-container {
    padding: 0 4px;
    box-sizing: border-box;
  }

  .player {
    min-height: 42px;
    margin: 7px auto;
    padding: 8px 10px;
  }

  .name {
    font-size: 13px;
  }

  .rating {
    font-size: 11px;
  }

  .controls {
    gap: 6px;
    margin: 12px auto;
  }

  .control-btn {
    min-width: 82px;
    font-size: 12px;
  }

  .exploration-status {
    font-size: 12px;
  }
}

@media (max-width: 400px) {
  .player {
    padding: 7px 8px;
  }

  .player-info {
    gap: 6px;
  }

  .name {
    font-size: 12px;
  }

  .rating {
    font-size: 10px;
  }

  .control-btn {
    min-width: 75px;
    padding: 0 8px;
  }
}
</style>

