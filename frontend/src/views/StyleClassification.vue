<script setup>
import { ref } from 'vue'
import axios from 'axios'

const fileInput = ref(null)
const files = ref([])
const fileNames = ref([])
const loading = ref(false)

// open file picker
function openFile() {
  fileInput.value.click()
}

// handle file/folder selection
function selectFiles(e) {
  const selected = Array.from(e.target.files)

  // filter only .pgn files
  files.value = selected.filter(f => f.name.toLowerCase().endsWith('.pgn'))

  fileNames.value = files.value.map(f => f.name)

  if (!files.value.length) {
    alert("No PGN files found in selection")
  }
}

// send to backend
async function classifyStyle() {
  if (!files.value.length) return

  loading.value = true
  const formData = new FormData()

  files.value.forEach(f => formData.append("files", f))

  try {
    const res = await axios.post("http://127.0.0.1:8000/classify_style", formData)

    alert(`🎯 Player Style: ${res.data.style}`)
  } catch (err) {
    console.error(err)
    alert("Failed to classify style")
  }

  loading.value = false
}
</script>

<template>
  <div class="card">
    <h3>Upload Games to Classify Player Style</h3>

    <!-- Upload button -->
    <button @click="openFile">
      📂 Upload PGN(s) or Folder
    </button>

    <!-- hidden input -->
    <input
      ref="fileInput"
      type="file"
      accept=".pgn"
      multiple
      webkitdirectory
      @change="selectFiles"
      style="display:none"
    />

    <!-- file list -->
    <p v-if="fileNames.length">
      📄 Files: {{ fileNames.join(", ") }}
    </p>

    <!-- classify -->
    <button
      class="classify-btn"
      @click="classifyStyle"
      :disabled="loading || fileNames.length === 0"
    >
      {{ loading ? "Analyzing..." : "Classify Style 🎯" }}
    </button>
  </div>
</template>

<style scoped>
.card {
  margin-top: 20px;
  padding: 20px;
  border-radius: 10px;
  background: #f5f5f5;
  text-align: center;
}

button {
  margin: 10px;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  border-radius: 6px;
}

.classify-btn {
  background-color: purple;
  color: white;
}
</style>