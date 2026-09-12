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

  /*
    ==========================================================
    EXPLORATION FORWARD
    ==========================================================

    If the user is inside a variation,
    move forward inside that variation first.
    */

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

    /*
      At the end of the exploration.

      DO NOT automatically continue the PGN here.

      The user must press Back until the
      branch point is reached.
    */

    return
  }

  /*
    ==========================================================
    PGN FORWARD
    ==========================================================

    This ALWAYS reads the original uploaded PGN.
    */

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

  /*
    ==========================================================
    EXPLORATION BACKWARD
    ==========================================================
    */

  if (isExploring.value) {
    if (branchIndex.value > 0) {
      branchIndex.value--

      rebuildBranch()
      setBoard()

      /*
        We are back at the branch position.
        Show the PGN analysis for that position.
        */

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

    /*
      branchIndex === 0

      We are exactly at the PGN branch point.

      Remove exploration and return to
      the actual PGN position.
      */

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

  /*
    ==========================================================
    NORMAL PGN BACKWARD
    ==========================================================
    */

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

  /*
    IMPORTANT:
    Do not add "q" to normal moves.

    e2e4
    g1f3
    e1g1

    Promotion:
    e7e8q
    */

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

  /*
    ==========================================================
    START A NEW EXPLORATION
    ==========================================================

    Example:

    PGN:
    e4 e5 Nf3 Nc6

    User is at Nf3.

    branchStart = 3
    */

  if (!isExploring.value) {
    branchStart.value =
      pgnIndex.value

    branchMoves.value = []
    branchIndex.value = 0
  }

  /*
    If the user went backward inside a variation
    and now chooses a different move, delete the
    old continuation.
    */

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

    /*
      Use cached analysis if available.
      */

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

    /*
      Your UploadPGNModal emits res.data,
      NOT the Axios response.

      Handle the array returned by /upload_pgn.
      */

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

    /*
      ========================================================
      READ THE UPLOADED PGN
      ========================================================
      */

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

    /*
      This is now the permanent PGN main line.
      */

    pgnMoves.value = [
      ...history
    ]

    console.log(
      "PGN MOVES STORED:",
      pgnMoves.value
    )

    /*
      Reset everything.
      */

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

    /*
      ========================================================
      SEND ORIGINAL PGN TO STOCKFISH BACKEND
      ========================================================
      */

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

    /*
      Start at the beginning of
      the uploaded PGN.
      */

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
  <div class="text-center">
    <UploadPGNModal
      @loaded="loadMoves"
    />

    <div class="player">
      <div class="left">
        <div class="name">
          {{ topPlayer.name || "Player" }}
        </div>

        <div class="rating">
          {{ topPlayer.elo || "--" }}
        </div>
      </div>
    </div>

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

      <div class="player bottom-player">
        <div class="left">
          <div class="name">
            {{ bottomPlayer.name || "Player" }}
          </div>

          <div class="rating">
            {{ bottomPlayer.elo || "--" }}
          </div>
        </div>
      </div>
    </div>

    <div class="mb-4">
      <v-btn
        @click="prevMove"
        :disabled="isAnalyzingMove"
      >
        ⬅️ Back
      </v-btn>

      <v-btn
        @click="nextMove"
        :disabled="isAnalyzingMove"
      >
        Forward ➡️
      </v-btn>

      <v-btn @click="flipBoard">
        🔄 Flip
      </v-btn>
    </div>

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
.board-wrapper {
  position: relative;
  width: fit-content;
  margin: 20px auto;
}

.board {
  width: 600px;
  max-width: 95vw;
}

.player {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 600px;
  margin: 10px auto;
  background: #8D6E63;
  padding: 10px;
  border-radius: 8px;
}

.player .left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.name {
  font-weight: bold;
  font-size: 14px;
}

.rating {
  font-size: 12px;
  color: #aaa;
}

.exploration-status {
  margin: 10px auto;
  font-size: 13px;
  opacity: 0.75;
}
</style>
