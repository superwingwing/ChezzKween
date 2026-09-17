<script setup>
import { ref } from "vue"
import { supabase } from "@/utils/supabase"


const fileInput = ref(null)
const folderInput = ref(null)
const selectedFiles = ref([])
const uploading = ref(false)
const progress = ref(0)
const browseFiles = () => fileInput.value?.click()
const browseFolder = () => folderInput.value?.click()

const selectFiles = (event) => {
  const files = Array.from(event.target.files || [])
  selectedFiles.value.push(...files)
  event.target.value = ""
}

const uploadFiles = async () => {
  if (!selectedFiles.value.length) {
    alert("Please select PGN files.")
    return
  }

  // Get the currently logged-in Supabase user
  const { data: { user }, error: userError } =
    await supabase.auth.getUser()

  if (userError || !user) {
    alert("You must be logged in to upload games.")
    return
  }


  uploading.value = true
  progress.value = 0

  const formData = new FormData()
  selectedFiles.value.forEach(file => formData.append("files", file))
  console.log("Logged-in User ID:", user.id)
  formData.append("user_id", user.id)

  const timer = setInterval(() => {
    if (progress.value < 95) progress.value += 5
  }, 300)

  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/upload_style`, {
      method: "POST",
      body: formData
    })

    clearInterval(timer)
    progress.value = 100

    const result = await response.json()

    console.log(result)
    alert(`${result.games_uploaded} games uploaded`)

    setTimeout(() => {
      uploading.value = false
      progress.value = 0
      selectedFiles.value = []
    }, 800)
  } catch (error) {
    clearInterval(timer)
    uploading.value = false
    progress.value = 0
    console.error(error)
    alert("Failed to upload PGN files.")
  }
}
</script>

<template>
  <v-card class="classifier-card" elevation="6">
    <v-card-title class="text-center classifier-title">
      <v-icon icon="mdi-chess-queen" class="mr-2" />
      Style Classifier
    </v-card-title>

    <v-card-text class="classifier-content">
      <div class="drop-zone" @click="browseFiles">
        <v-icon
          icon="mdi-file-upload-outline"
          size="42"
          class="upload-icon"
        />

        <div class="upload-text">
          <strong @click.stop="browseFiles">Select PGN Files</strong>
          <span>or</span>
          <strong @click.stop="browseFolder">Select Folder</strong>
        </div>

        <div v-if="selectedFiles.length" class="file-count">
          <v-icon icon="mdi-file-multiple-outline" size="16" />
          {{ selectedFiles.length }} PGN file(s) selected
        </div>
      </div>

      <input
        ref="fileInput"
        type="file"
        accept=".pgn"
        multiple
        hidden
        @change="selectFiles"
      />

      <input
        ref="folderInput"
        type="file"
        accept=".pgn"
        webkitdirectory
        directory
        multiple
        hidden
        @change="selectFiles"
      />

      <v-btn
        block
        color="white"
        class="upload-btn"
        :loading="uploading"
        :disabled="uploading || !selectedFiles.length"
        @click="uploadFiles"
      >
        {{ uploading ? `Uploading ${progress}%` : "Upload Games" }}
      </v-btn>

      <v-progress-linear
        v-if="uploading"
        :model-value="progress"
        color="white"
        bg-color="white"
        bg-opacity=".25"
        rounded
        height="6"
        class="progress"
      />

      <div class="subtitle">
        Analyze a collection of your chess games.
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.classifier-card {
  width: 100%;
  max-width: 320px;
  border-radius: 18px;
  background: #01579b;
  color: white;
  overflow: hidden;
}

.classifier-title {
  padding: 14px 16px 8px;
  font-size: 18px;
  font-weight: 700;
}

.classifier-content {
  padding: 10px 16px 14px;
}

.drop-zone {
  border: 2px dashed rgba(255,255,255,.55);
  border-radius: 14px;
  padding: 14px 10px;
  text-align: center;
  cursor: pointer;
  transition: .2s ease;
}

.drop-zone:hover {
  background: rgba(255,255,255,.08);
  border-color: white;
}

.upload-icon {
  margin-bottom: 4px;
}

.upload-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 13px;
}

.upload-text strong {
  text-decoration: underline;
  cursor: pointer;
}

.upload-text span {
  opacity: .8;
  font-size: 11px;
}

.file-count {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  margin-top: 8px;
  font-size: 11px;
  opacity: .9;
}

.upload-btn {
  margin-top: 10px;
  min-height: 38px;
  color: #01579b !important;
  font-weight: 700;
  text-transform: none;
  border-radius: 10px;
}

.progress {
  margin-top: 9px;
}

.subtitle {
  margin-top: 8px;
  text-align: center;
  font-size: 11px;
  opacity: .75;
}

@media (max-width: 960px) {
  .classifier-card {
    max-width: 100%;
  }
}

@media (max-width: 600px) {
  .classifier-card {
    border-radius: 14px;
  }

  .classifier-title {
    font-size: 16px;
    padding: 11px 12px 6px;
  }

  .classifier-content {
    padding: 8px 12px 12px;
  }

  .drop-zone {
    padding: 12px 8px;
  }
}
</style>