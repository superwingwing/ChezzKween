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
      </v-card-text>
    </v-card>

    <!-- All Generated Videos -->
    <v-card class="mt-5">
      <v-card-title>All Generated Videos</v-card-title>
      <v-card-text>
        <div v-if="videos.length === 0">No videos found.</div>
        <div v-for="(video, idx) in videos" :key="idx" class="mt-3">
          <video
            :src="video"
            controls
            preload="metadata"
            style="width:100%"
          ></video>
        </div>
      </v-card-text>
    </v-card>

  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const fileInput = ref(null)
const file = ref(null)
const fileName = ref('')
const loading = ref(false)
const progress = ref(0)
const videos = ref([])

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

// Generate video and refresh list
async function generateVideo() {
  if (!file.value) {
    alert('Please upload a PGN file first')
    return
  }

  loading.value = true
  progress.value = 0

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
    await axios.post('http://localhost:3000/upload', formData)
    clearInterval(progressInterval)
    progress.value = 100

    // Refresh the video list
    await loadVideos()
  } catch (err) {
    console.error(err)
    alert('Video generation failed')
    clearInterval(progressInterval)
  } finally {
    loading.value = false
  }
}

// Load all generated videos
async function loadVideos() {
  try {
    const res = await axios.get('http://localhost:3000/videos')
    // prepend server origin to each video path
    videos.value = res.data.videos.map(v => 'http://localhost:3000' + v)
  } catch (err) {
    console.error('Failed to load videos:', err)
    videos.value = []
  }
}

// Load videos when component mounts
onMounted(() => {
  loadVideos()
})
</script>
