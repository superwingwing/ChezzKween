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
 <div class="v-row">
      <div class="v-col">
        <SideNavigation v-model="drawerOpen" />
      </div>
      <div  class="v-col" style="max-width: 600px; margin: auto; text-align: center;">
          <br>
          <h2>♟️ ChessKween</h2>

          <!-- hidden file input -->
          <input
            ref="fileInput"
            type="file"
            accept=".pgn"
            @change="selectFile"
            style="display:none"
          />

          <!-- buttons -->
          <button @click="openFile">Select PGN</button>
          <span v-if="fileName">📄 {{ fileName }}</span>
          <br /><br />

          <button @click="uploadPGN" :disabled="loading">
            {{ loading ? "Loading..." : "Load Game" }}
          </button>

          <!-- chessboard -->
          <chess-board
            ref="boardRef"
            style="width: 500px; margin: 20px auto;"
          ></chess-board>

          <!-- controls -->
          <div>
            <button @click="prevMove">⬅️ Back </button>
            <button @click="nextMove">Forward ➡️</button>
          </div>
      </div>
      <div class="v-col">
        <StyleClassification />
      </div>
 </div>

</template>