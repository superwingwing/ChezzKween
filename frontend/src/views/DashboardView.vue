<script setup>
import { ref } from "vue"
import axios from "axios"
import { Chess } from "chess.js"
import "chessboard-element"
import StyleClassification from "../components/layout/StyleClassification.vue"
import DashboardLayout from "@/components/layout/DashboardLayout.vue"

// chess logic
const boardRef = ref(null)
const fileInput = ref(null)
const file = ref(null)
const fileName = ref("")
const loading = ref(false)

const chess = new Chess()
const moves = ref([])
const moveIndex = ref(0)

// file handling
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

    alert("PGN loaded!")
  } catch (err) {
    console.error(err)
    alert("Failed to load PGN")
  }

  loading.value = false
}

// board controls
function updateBoard() {
  if (boardRef.value) {
    boardRef.value.setPosition(chess.fen())
  }
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
  <DashboardLayout>

    <v-container fluid>
      <v-row>

        <!-- ♟️ CENTER -->
        <v-col cols="9" class="d-flex justify-center">
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
              <chess-board ref="boardRef" style="width: 500px;" />
            </div>

            <!-- BOTTOM PLAYER -->
            <div class="player mt-n3">
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

            <!-- FILE BUTTON -->
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

        <!-- 🧠 RIGHT -->
        <v-col cols="3">
          <StyleClassification />
        </v-col>

      </v-row>
    </v-container>

  </DashboardLayout>
</template>