<script setup>
import { ref } from "vue"
import { Chess } from "chess.js"
import "chessboard-element"

import UploadPGNModal from "@/components/layout/UploadPGNModal.vue"

const boardRef = ref(null)

const chess = new Chess()
const moves = ref([])
const moveIndex = ref(0)

const currentGame = ref(null)

// =====================
// BOARD
// =====================
function updateBoard() {
  boardRef.value?.setPosition(chess.fen())
}

function resetBoard() {
  chess.reset()
  moveIndex.value = 0
  updateBoard()
}

function nextMove() {
  if (moveIndex.value < moves.value.length) {
    chess.move(moves.value[moveIndex.value])
    moveIndex.value++
    updateBoard()
  }
}

function prevMove() {
  if (moveIndex.value > 0) {
    moveIndex.value--
    chess.reset()

    for (let i = 0; i < moveIndex.value; i++) {
      chess.move(moves.value[i])
    }

    updateBoard()
  }
}

// =====================
// FROM BACKEND (UPLOAD)
// =====================
function loadMoves(response) {
  console.log("BACKEND RESPONSE:", response)

  const game = response.data[0]   // 🔥 IMPORTANT

  currentGame.value = game

  chess.reset()
  chess.loadPgn(game.pgn)

  moves.value = chess.history()
  resetBoard()
}
</script>

<template>
  <div class="text-center">

    <!-- UPLOAD MODAL -->
    <div style="margin-bottom: 20px;">
      <UploadPGNModal @loaded="loadMoves" />
    </div>

    <!-- TOP PLAYER -->
    <div class="player">
      <div class="left">
        <div>
          <div class="name">
            {{ currentGame?.white_name || "White" }}
          </div>
          <div class="rating">
            {{ currentGame?.white_elo || "--" }}
          </div>
        </div>
      </div>
    </div>

    <!-- BOARD -->
    <div class="board-wrapper">
      <chess-board ref="boardRef" class="board" />

      <!-- BOTTOM PLAYER -->
      <div class="player bottom-player">
        <div class="left">
          <div>
            <div class="name">
              {{ currentGame?.black_name || "Black" }}
            </div>
            <div class="rating">
              {{ currentGame?.black_elo || "--" }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- CONTROLS -->
    <div class="mb-4">
      <v-btn @click="prevMove">⬅️ Back</v-btn>
      <v-btn @click="nextMove">Forward ➡️</v-btn>
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

  background: #2c2c2c;
  padding: 10px;
  border-radius: 8px;
}

.bottom-player {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;

  width: 100%;
  margin: 0;

  background: rgba(44, 44, 44, 0.9);
  backdrop-filter: blur(6px);

  border-radius: 0 0 8px 8px;
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