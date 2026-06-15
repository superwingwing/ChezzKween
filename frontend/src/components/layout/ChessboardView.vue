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

    <!-- BOARD -->
    <chess-board ref="boardRef" style="width: 500px;" />

    <!-- BOTTOM PLAYER -->
    <div class="player">
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