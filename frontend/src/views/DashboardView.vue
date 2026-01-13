<template>
  <v-container>

    <!-- Upload PGN -->
    <v-card>
      <v-card-title>Upload PGN</v-card-title>
      <v-card-text>
        <v-btn @click="openFile">Upload</v-btn>
        <input ref="fileInput" hidden type="file" accept=".pgn" @change="selectFile">
        <p v-if="fileName">File: {{ fileName }}</p>
      </v-card-text>
    </v-card>

    <!-- Generate Video -->
    <v-card class="mt-5">
      <v-card-title>Generate Video</v-card-title>
      <v-card-text>
        <v-btn color="green" @click="generateVideo" :loading="loading">
          Generate 🎥
        </v-btn>

        <!-- Progress Bar -->
        <v-progress-linear
          v-if="loading"
          :value="progress"
          striped
          color="green"
          class="mt-3"
        ></v-progress-linear>
        <p v-if="loading">{{ progress }}%</p>

        <!-- Video Output -->
            <video
              v-if="videoUrl"
              :key="videoUrl"
              :src="videoUrl"
              controls
              preload="metadata"
              class="mt-4"
              style="width:100%"
            ></video>

      </v-card-text>
    </v-card>

    <!-- Move Analysis -->
    <v-card v-if="analysis.length" class="mt-5">
      <v-card-title>Move Analysis (from Lichess)</v-card-title>
      <v-list>
        <v-list-item
          v-for="(a, idx) in analysis"
          :key="idx"
        >
          Move {{ idx + 1 }}: {{ a.move }} — Eval: {{ a.eval }}
        </v-list-item>
      </v-list>
    </v-card>

  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const fileInput = ref(null)
const file = ref(null)
const fileName = ref('')
const videoUrl = ref('')
const loading = ref(false)
const progress = ref(0)
const analysis = ref([])

let progressInterval = null

// Open file dialog
function openFile() {
  fileInput.value.click()
}

// Select PGN file
function selectFile(e) {
  file.value = e.target.files[0]
  fileName.value = file.value.name
}

// Generate video and fetch analysis
async function generateVideo() {
  if (!file.value) {
    alert('Please upload a PGN file first')
    return
  }

  loading.value = true
  progress.value = 0
  videoUrl.value = ''
  analysis.value = []

  // Start polling progress
  progressInterval = setInterval(async () => {
    try {
      const res = await axios.get('http://localhost:3000/progress')
      progress.value = res.data.progress
    } catch (err) {
      console.error('Progress polling error:', err)
    }
  }, 300)

  // Upload PGN
  const formData = new FormData()
  formData.append('pgn', file.value)

  try {
    const res = await axios.post('http://localhost:3000/upload', formData)

    // Stop progress polling
    clearInterval(progressInterval)
    progress.value = 100

    videoUrl.value = 'http://localhost:3000' + res.data.videoUrl
    analysis.value = res.data.analysis || []
  } catch (err) {
    console.error(err)
    alert('Video generation failed')
    clearInterval(progressInterval)
  } finally {
    loading.value = false
  }
}
</script>
