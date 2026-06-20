<script setup>
import { ref, computed } from "vue"
import { Chess } from "chess.js"
import { TheChessboard } from "vue3-chessboard"
import "vue3-chessboard/style.css"
import UploadPGNModal from "@/components/layout/UploadPGNModal.vue"

// ongoing to fix rotate board bug:
//keep going
const chess = new Chess()

const moves = ref([])
const moveIndex = ref(0)
const currentGame = ref(null)

const orientation = ref("white")

let boardAPI = null

// =====================
// PLAYER BASE DATA
// =====================
const whitePlayer = computed(() => ({
  name: currentGame.value?.white_name,
  elo: currentGame.value?.white_elo
}))

const blackPlayer = computed(() => ({
  name: currentGame.value?.black_name,
  elo: currentGame.value?.black_elo
}))

// =====================
// DYNAMIC VIEW (Chess.com style)
// =====================
const topPlayer = computed(() =>
  orientation.value === "white" ? blackPlayer.value : whitePlayer.value
)

const bottomPlayer = computed(() =>
  orientation.value === "white" ? whitePlayer.value : blackPlayer.value
)

// =====================
// BOARD NAVIGATION
// =====================
function nextMove() {
  if (moveIndex.value < moves.value.length) {
    chess.move(moves.value[moveIndex.value])
    moveIndex.value++
  }
}

function prevMove() {
  if (moveIndex.value > 0) {
    moveIndex.value--
    chess.reset()

    for (let i = 0; i < moveIndex.value; i++) {
      chess.move(moves.value[i])
    }
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
// LOAD PGN
// =====================
function loadMoves(response) {
  const game = response.data[0]

  currentGame.value = game

  chess.reset()
  chess.loadPgn(game.pgn)

  moves.value = chess.history()

  moveIndex.value = 0
  orientation.value = "white"
}
</script>

<template>
  <div class="text-center">

    <UploadPGNModal @loaded="loadMoves" />

    <!-- TOP PLAYER -->
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

    <!-- BOARD -->
    <div class="board-wrapper">
      <TheChessboard
        class="board"
        :orientation="orientation"
        @board-created="(api) => (boardAPI = api)"
      />

      <!-- BOTTOM PLAYER -->
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

