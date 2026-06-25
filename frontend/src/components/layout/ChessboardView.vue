<script setup>
import { ref, computed } from "vue"
import { Chess } from "chess.js"
import { TheChessboard } from "vue3-chessboard"
import "vue3-chessboard/style.css"
import UploadPGNModal from "@/components/layout/UploadPGNModal.vue"
import MoveQuality from "@/components/layout/MoveQuality.vue"

const chess = new Chess()

const moves = ref([])
const moveIndex = ref(0)
const currentGame = ref(null)
const orientation = ref("white")

const evaluations = ref([])

let boardAPI = null

const emit = defineEmits(["update-eval"])

const isNavigating = ref(false)

const currentQuality = computed(() => {
  const current = evaluations.value[moveIndex.value - 1]
  return current?.quality || ""
})
// =====================
// PLAYERS
// =====================
const whitePlayer = computed(() => ({
  name: currentGame.value?.white_name,
  elo: currentGame.value?.white_elo
}))

const blackPlayer = computed(() => ({
  name: currentGame.value?.black_name,
  elo: currentGame.value?.black_elo
}))

const topPlayer = computed(() =>
  orientation.value === "white" ? blackPlayer.value : whitePlayer.value
)

const bottomPlayer = computed(() =>
  orientation.value === "white" ? whitePlayer.value : blackPlayer.value
)

// =====================
// GO TO MOVE (CORE)
// =====================
function goToMove(index) {
  isNavigating.value = true

  chess.reset()

  for (let i = 0; i < index; i++) {
    chess.move(moves.value[i])
  }

  moveIndex.value = index

  if (boardAPI) {
    boardAPI.setPosition(chess.fen())

    const current = evaluations.value[index - 1]
  console.log("ENGINE DATA:", current) // 👈 ADD IT HERE

    if (current) {
      // ✅ update eval bar
      // emit("update-eval", current.evaluation)
      emit("update-eval", current.evaluation.value)

      // ✅ draw best move arrow
      if (current.best_move) {
        const from = current.best_move.slice(0, 2)
        const to = current.best_move.slice(2, 4)

        boardAPI.drawMove(from, to, "green")
      } else {
        boardAPI.hideMoves()
      }
    }
  }

  isNavigating.value = false
}

// =====================
// NAVIGATION
// =====================
function nextMove() {
  if (moveIndex.value < moves.value.length) {
    goToMove(moveIndex.value + 1)
  }
}

function prevMove() {
  if (moveIndex.value > 0) {
    goToMove(moveIndex.value - 1)
  }
}

// =====================
// MANUAL MOVE
// =====================
function onMove(move) {
  if (isNavigating.value) return

  const result = chess.move({
    from: move.from,
    to: move.to,
    promotion: "q"
  })

  if (result) {
    if (moveIndex.value < moves.value.length) {
      moves.value = moves.value.slice(0, moveIndex.value)
    }

    moves.value.push(result.san)
    goToMove(moves.value.length)
  }
}

// =====================
// FLIP BOARD
// =====================
function flipBoard() {
  orientation.value =
    orientation.value === "white" ? "black" : "white"
}

// =====================
// LOAD PGN + ENGINE
// =====================
async function loadMoves(response) {
  const game = response.data[0]

  currentGame.value = game

  chess.reset()
  chess.loadPgn(game.pgn)

  moves.value = chess.history()

  goToMove(0)

  orientation.value = "white"

  try {
    const res = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        pgn: game.pgn
      })
    })

    const data = await res.json()

    evaluations.value = data.evaluations

    // initial eval
    if (evaluations.value.length > 0) {
      // emit("update-eval", evaluations.value[0].evaluation)
      emit("update-eval", evaluations.value[0].evaluation.value)
    }

  } catch (err) {
    console.error("Engine error:", err)
  }
}
</script>

<template>
  <div class="text-center">

    <UploadPGNModal @loaded="loadMoves" />

    <!-- TOP PLAYER -->
    <div class="player">
      <div class="left">
        <div class="name">{{ topPlayer.name || "Player" }}</div>
        <div class="rating">{{ topPlayer.elo || "--" }}</div>
      </div>
    </div>

    <!-- BOARD -->
    <div class="board-wrapper">
      <TheChessboard
        class="board"
        :orientation="orientation"
        @move="onMove"
        @board-created="(api) => (boardAPI = api)"
      />

       <MoveQuality
        :quality="currentQuality"
        :square="qualityPosition"
      />

      <!-- BOTTOM PLAYER -->
      <div class="player bottom-player">
        <div class="left">
          <div class="name">{{ bottomPlayer.name || "Player" }}</div>
          <div class="rating">{{ bottomPlayer.elo || "--" }}</div>
        </div>
      </div>
    </div>

    <!-- CONTROLS -->
    <div class="mb-4">
      <v-btn @click="prevMove">⬅️ Back</v-btn>
      <v-btn @click="nextMove">Forward ➡️</v-btn>
      <v-btn @click="flipBoard">🔄 Flip</v-btn>
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
</style>