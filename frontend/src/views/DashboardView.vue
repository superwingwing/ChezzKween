<script setup>
import { ref } from "vue"
import axios from "axios"
import { Chess } from "chess.js"
import "chessboard-element"
import SideNavigation from "@/views/SideNavigation.vue"
import StyleClassification from "./StyleClassification.vue" 

// refs
const boardRef = ref(null)
const fileInput = ref(null)
const file = ref(null)
const fileName = ref("")
const loading = ref(false)
const chess = new Chess()
const moves = ref([])
const moveIndex = ref(0)
const drawerOpen = ref(true)

// open file picker
function openFile() {
  fileInput.value.click()
}

// select file
function selectFile(e) {
  file.value = e.target.files[0]
  fileName.value = file.value.name
}

// upload PGN
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
    alert("PGN loaded!")
  } catch (err) {
    console.error(err)
    alert("Failed to load PGN")
  }

  loading.value = false
}

// update board position
function updateBoard() {
  if (boardRef.value) {
    boardRef.value.setPosition(chess.fen())
  }
}

// next move
function nextMove() {
  if (moveIndex.value < moves.value.length) {
    chess.move(moves.value[moveIndex.value])
    moveIndex.value++
    updateBoard()
  }
}

// previous move
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
  <v-container fluid>
    <v-row>

      <!-- 🧭 LEFT: SIDENAV -->
      <v-col cols="2">
        <SideNavigation v-model="drawerOpen" />
      </v-col>

      <!-- ♟️ CENTER: CHESSBOARD -->
      <v-col cols="7" class="d-flex justify-center">
        <div style="max-width: 600px; width: 100%;" class="text-center">

          <!-- TOP PLAYER -->
          <div class="player mb-1">
            <div class="left">
              <img src="/images/pic1.jpg" class="avatar" />
              <div>
                <div class="name">super-wingwing</div>
                <div class="rating">PH (2244)</div>
              </div>
            </div>
            <div class="timer">10:00</div>
          </div>

          <!-- CHESSBOARD -->
          <div class="d-flex justify-center mb-0">
            <chess-board
              ref="boardRef"
              style="width: 500px;"
            ></chess-board>
          </div>

          <!-- BOTTOM PLAYER -->
          <div class="player mb-0 mt-0 mt-n3">
            <div class="left">
              <img src="/images/pic1.jpg" class="avatar" />
              <div>
                <div class="name">bandera-7</div>
                <div class="rating">UA (2211)</div>
              </div>
            </div>
            <div class="timer">10:00</div>
          </div>

          <!-- CONTROLS -->
          <div class="mb-4">
            <v-btn class="mr-2" @click="prevMove">⬅️ Back</v-btn>
            <v-btn @click="nextMove">Forward ➡️</v-btn>
          </div>

          <!-- FILE INPUT -->
          <input
            ref="fileInput"
            type="file"
            accept=".pgn"
            @change="selectFile"
            style="display:none"
          />

          <!-- FILE BUTTONS -->
          <div class="mb-2">
            <v-btn color="primary" @click="openFile">
              Select PGN
            </v-btn>
          </div>

          <div v-if="fileName" class="mb-2">
            📄 {{ fileName }}
          </div>

          <v-btn
            color="success"
            :loading="loading"
            :disabled="loading"
            @click="uploadPGN"
          >
            Load Game
          </v-btn>

        </div>
      </v-col>

      <!-- 🧠 RIGHT: STYLE CLASSIFIER -->
      <v-col cols="3">
        <StyleClassification />
      </v-col>

    </v-row>
  </v-container>
</template>

<style scoped>
.layout {
  display: flex;
  background: #1e1e1e;
  min-height: 100vh;
  color: white;
}

/* CENTER */
.center {
  flex: 1;
  text-align: center;
  padding: 20px;
}

/* PLAYER */
.player {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #2c2c2c;
  padding: 10px;
  border-radius: 10px;
  width: 500px;
  margin: 10px auto;
}

.player .left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 8px;
}

.name {
  font-weight: bold;
}

.rating {
  font-size: 12px;
  color: #aaa;
}

.timer {
  background: #3a3a3a;
  padding: 5px 10px;
  border-radius: 6px;
}

/* CONTROLS */
.controls {
  margin-top: 15px;
}

.controls button {
  margin: 5px;
  padding: 10px 15px;
  border-radius: 8px;
  border: none;
  background: #4b5563;
  color: white;
  cursor: pointer;
}

.controls button:hover {
  background: #6b7280;
}

/* UPLOAD */
.upload button {
  margin: 5px;
  padding: 8px 12px;
  border-radius: 6px;
  border: none;
  background: #2563eb;
  color: white;
  cursor: pointer;
}

.upload button:hover {
  background: #3b82f6;
}
</style>