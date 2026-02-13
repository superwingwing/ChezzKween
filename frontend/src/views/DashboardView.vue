<script setup>
import { ref, onMounted } from 'vue'
import PlayerStyleUpload from '@/views/PlayerStyleUpload.vue'
import axios from 'axios'

const fileInput = ref(null)
const file = ref(null)
const fileName = ref('')
const loading = ref(false)
const videos = ref([])

// Open hidden file input
function openFile() { fileInput.value.click() }

// Select a PGN file
function selectFile(e) {
  file.value = e.target.files[0]
  fileName.value = file.value.name
}

// Upload PGN and generate video
async function generateVideo() {
  if (!file.value) return alert("Upload a PGN first")
  loading.value = true
  const formData = new FormData()
  formData.append("file", file.value)
  try {
    // Correct endpoint
    await axios.post("http://localhost:8000/upload_pgn", formData)
    await loadVideos()  // refresh video list
  } catch (err) { 
    console.error(err) 
    alert("Failed to generate video. Check console for details.")
  }
  loading.value = false
}

// Load all videos from backend
async function loadVideos() {
  try {
    // Correct endpoint for listing videos
    const res = await axios.get("http://localhost:8000/videos")
    videos.value = res.data.videos
  } catch (err) { 
    console.error(err) 
    alert("Failed to load videos. Check console.")
  }
}

// Load videos on mount
onMounted(() => { loadVideos() })
</script>

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
      </v-card-text>
    </v-card>

    <!-- All Generated Videos -->
    <v-card class="mt-5">
      <v-card-title>All Generated Videos</v-card-title>
      <v-card-text>
        <div v-if="videos.length === 0">No videos found.</div>
        <div v-for="(video, idx) in videos" :key="idx" class="mt-3">
          <video :src="'http://localhost:8000' + video" controls style="width:100%"></video>
          <p>{{ video.split('/').pop() }}</p>
        </div>
      </v-card-text>
    </v-card>

    <!-- Player Style Classification -->
    <PlayerStyleUpload />
  </v-container>
</template>

<style scoped>
.videos-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
.video-card {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>

