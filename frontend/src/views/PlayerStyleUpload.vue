<script setup>
import { ref } from 'vue'
import axios from 'axios'

const fileInput = ref(null)
const files = ref([])
const fileNames = ref([])
const loading = ref(false)

function openFile() {
  fileInput.value.click()
}

function selectFiles(e) {
  files.value = Array.from(e.target.files)
  fileNames.value = files.value.map(f => f.name)
}

async function classifyStyle() {
  if (!files.value.length) return
  loading.value = true
  const formData = new FormData()
  files.value.forEach(f => formData.append("files", f))
  
  try {
    const res = await axios.post("http://localhost:8000/classify_style", formData)
    alert(`Player Style: ${res.data.style}`)
  } catch (err) {
    console.error(err)
    alert("Failed to classify style. Check console for details.")
  }
  
  loading.value = false
}
</script>

<template>
  <v-card class="mt-5">
    <v-card-title>Upload Games to Classify Player Style</v-card-title>
    <v-card-text>
      <v-btn color="blue" @click="openFile">Upload PGN(s)</v-btn>
      <input ref="fileInput" hidden type="file" accept=".pgn" multiple @change="selectFiles">
      <p v-if="fileNames.length">Files: {{ fileNames.join(", ") }}</p>
      <v-btn
        color="purple"
        class="mt-2"
        @click="classifyStyle"
        :loading="loading"
        :disabled="fileNames.length === 0"
      >
        Classify Style 🎯
      </v-btn>
    </v-card-text>
  </v-card>
</template>

<style scoped>
</style>
