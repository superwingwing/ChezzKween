<script setup>
import { ref } from "vue"
import axios from "axios"
import { Chess } from "chess.js"
import "chessboard-element"

const boardRef = ref(null)
const fileInput = ref(null)
const file = ref(null)
const fileName = ref("")
const loading = ref(false)

const chess = new Chess()
const moves = ref([])
const moveIndex = ref(0)

function openFile() {
  fileInput.value.click()
}

function selectFile(e) {
  file.value = e.target.files[0]
  fileName.value = file.value.name
}

async function uploadPGN() {
  if (!file.value) return alert("Upload a PGN first")

  loading.value = true
  const formData = new FormData()
  formData.append("file", file.value)

  try {
    const res = await axios.post("http://127.0.0.1:8000/upload_pgn", formData)

    moves.value = res.data.moves || []
    moveIndex.value = 0
    chess.reset()
    updateBoard()
  } catch (err) {
    console.error(err)
    alert("Failed to load PGN")
  }

  loading.value = false
}

function updateBoard() {
  boardRef.value?.setPosition(chess.fen())
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
</script>

<template>
  <div class="text-center">

    <!-- TOP PLAYER (normal) -->
    <div class="player mb-0">
      <div class="left">
        <img src="/images/pic1.jpg" class="avatar" />
        <div>
          <div class="name">super-wingwing</div>
          <div class="rating">PH (2244)</div>
        </div>
      </div>
      <div class="timer">10:00</div>
    </div>

    <!-- BOARD + OVERLAY -->
    <div class="board-wrapper">

      <!-- BOARD -->
      <chess-board ref="boardRef" class="board" />

      <!-- BOTTOM PLAYER (overlay) -->
      <div class="player bottom-player">
        <div class="left">
          <img src="/images/pic1.jpg" class="avatar" />
          <div>
            <div class="name">bandera-7</div>
            <div class="rating">UA (2211)</div>
          </div>
        </div>
        <div class="timer">10:00</div>
      </div>

    </div>

    <!-- CONTROLS -->
    <div class="mb-4">
      <v-btn @click="prevMove">⬅️ Back</v-btn>
      <v-btn @click="nextMove">Forward ➡️</v-btn>
    </div>

    <!-- FILE -->
    <input ref="fileInput" type="file" accept=".pgn" @change="selectFile" hidden />

    <v-btn @click="openFile">Select PGN</v-btn>

    <div v-if="fileName">📄 {{ fileName }}</div>

    <v-btn :loading="loading" @click="uploadPGN">
      Load Game
    </v-btn>

  </div>
</template>

<style scoped>
/* BOARD WRAPPER */
.board-wrapper {
  position: relative;
  width: fit-content;
  margin: 20px auto;
}

/* BOARD */
.board {
  width: 600px;
  max-width: 95vw;
}

/* PLAYER (TOP NORMAL) */
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

/* OVERLAY PLAYER (BOTTOM ONLY) */
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

/* PLAYER LEFT */
.player .left {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* AVATAR */
.avatar {
  width: 36px;
  height: 36px;
  border-radius: 6px;
}

/* TEXT */
.name {
  font-weight: bold;
  font-size: 14px;
}

.rating {
  font-size: 12px;
  color: #aaa;
}

/* TIMER */
.timer {
  background: #3a3a3a;
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 13px;
}
</style>