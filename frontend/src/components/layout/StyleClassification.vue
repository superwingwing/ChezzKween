<script setup>
import { ref } from 'vue'
import { supabase } from '@/utils/supabase'
import AlertNotification from '../common/AlertNotification.vue'

const formSuccessMessage = ref('')
const formErrorMessage = ref('')

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
  event.target.value = ''
}

 
const uploadFiles = async () => {
  if (!selectedFiles.value.length) {
    formErrorMessage.value = 'Please select PGN files.'
    return
  }

  formSuccessMessage.value = ''
  formErrorMessage.value = ''

  uploading.value = true
  progress.value = 0

  let timer

  try {
    const {
      data: { user },
      error: userError,
    } = await supabase.auth.getUser()

    if (userError || !user) {
      throw new Error('You must be logged in to upload games.')
    }

    const formData = new FormData()

    selectedFiles.value.forEach((file) => {
      formData.append('files', file)
    })

    formData.append('user_id', user.id)

    timer = setInterval(() => {
      if (progress.value < 95) {
        progress.value += 5
      }
    }, 300)

    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/upload_style`,
      {
        method: 'POST',
        body: formData,
      },
    )

    const result = await response.json()

    if (!response.ok || result.success === false) {
      throw new Error(
        result.error || 'Failed to upload PGN files.',
      )
    }

    const count = Number(result.games_uploaded) || 0

    if (count === 0) {
      formErrorMessage.value =
        'No games were uploaded. Please check your PGN files.'
    } else {
      formSuccessMessage.value =
        `${count} game${count === 1 ? '' : 's'} uploaded and classified successfully!`
    }

    progress.value = 100

    setTimeout(() => {
      selectedFiles.value = []
      progress.value = 0
      uploading.value = false
    }, 800)
  } catch (error) {
    formErrorMessage.value =
      error.message || 'Failed to upload PGN files.'

    console.error('PGN upload failed:', error)
  } finally {
    if (timer) clearInterval(timer)

    if (progress.value !== 100) {
      uploading.value = false
      progress.value = 0
    }
  }
}
</script>

<template>
  <v-card class="classifier-card" elevation="4">
    <!-- HEADER -->
    <v-card-item class="classifier-header">
      <template #prepend>
        <v-avatar rounded="lg" size="46" class="classifier-icon">
          <v-icon icon="mdi-chess-bishop" size="25" />
        </v-avatar>
      </template>

      <v-card-title class="pa-0 classifier-title">
        Style Classifier & Bulk PGN Analysis
      </v-card-title>

      <v-card-subtitle class="pa-0 classifier-subtitle">
        Classify your profile into Aggressive vs Positional
      </v-card-subtitle>
    </v-card-item>

    <!-- CONTENT -->
    <v-card-text class="classifier-content">
        <AlertNotification
          :form-success-message="formSuccessMessage"
          :form-error-message="formErrorMessage"
        />
      <!-- DROP ZONE -->
      <div class="drop-zone" @click="browseFiles">
        <v-icon icon="mdi-file-upload-outline" size="34" class="upload-icon" />

        <div class="upload-text">
          <strong @click.stop="browseFiles"> Select PGN Files </strong>

          <span> or Drag & Drop Here </span>
        </div>

        <div class="supported-text">Supports Lichess, Chess.com & ChessBase PGNs</div>

        <div v-if="selectedFiles.length" class="file-count">
          <v-icon icon="mdi-file-multiple-outline" size="15" />

          {{ selectedFiles.length }} PGN file(s) selected
        </div>
      </div>

      <!-- FILE INPUT -->
      <input ref="fileInput" type="file" accept=".pgn" multiple hidden @change="selectFiles" />

      <!-- FOLDER INPUT -->
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

      <!-- UPLOAD BUTTON -->
      <v-btn
        block
        size="large"
        class="upload-btn"
        :loading="uploading"
        :disabled="uploading || !selectedFiles.length"
        prepend-icon="mdi-memory"
        @click="uploadFiles"
      >
        {{ uploading ? `Uploading ${progress}%` : 'Upload & Classify Games' }}
      </v-btn>

      <!-- PROGRESS -->
      <v-progress-linear
        v-if="uploading"
        :model-value="progress"
        color="#F28C28"
        bg-color="white"
        bg-opacity=".15"
        rounded
        height="5"
        class="progress"
      />
    </v-card-text>
  </v-card>
</template>

<style scoped>
.classifier-card {
  width: 100%;
  max-width: 100%;
  border-radius: 18px;
  background: #0b1328;
  color: white;
  overflow: hidden;
}

/* HEADER */
.classifier-header {
  padding: 12px 16px 7px !important;
}

.classifier-icon {
  background: rgba(242, 140, 40, 0.22);
  color: #f28c28;
}

.classifier-title {
  color: white !important;
  font-size: 16px !important;
  font-weight: 800 !important;
  line-height: 1.15;
}

.classifier-subtitle {
  margin-top: 2px;
  color: #91a4bf !important;
  font-size: 11px !important;
  line-height: 1.2;
}

/* CONTENT */
.classifier-content {
  padding: 6px 16px 14px !important;
}

/* DROP ZONE */
.drop-zone {
  padding: 20px 14px;
  border: 2px dashed #c76b16;
  border-radius: 15px;
  background: #080f20;
  text-align: center;
  cursor: pointer;
  transition: 0.2s ease;
}

.drop-zone:hover {
  border-color: #f28c28;
  background: #0d162a;
}

.upload-icon {
  color: #ff8735;
  margin-bottom: 5px;
}

/* UPLOAD TEXT */
.upload-text {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px;
  color: #91a4bf;
  font-size: 13px;
}

.upload-text strong {
  color: white;
  cursor: pointer;
}

.supported-text {
  margin-top: 7px;
  color: #91a4bf;
  font-size: 11px;
}

/* FILE COUNT */
.file-count {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  margin-top: 7px;
  color: #f28c28;
  font-size: 10px;
}

/* UPLOAD BUTTON */
.upload-btn {
  margin-top: 12px;
  min-height: 44px;
  border-radius: 13px;
  background: #ff7517 !important;
  color: white !important;
  font-size: 13px;
  font-weight: 800;
  text-transform: none;
  box-shadow: 0 6px 16px rgba(255, 117, 23, 0.18);
}

.upload-btn:hover {
  background: #f56b0c !important;
}

/* PROGRESS */
.progress {
  margin-top: 8px;
}

/* =========================================================
   SHORT LAPTOP SCREENS
========================================================= */

@media (max-height: 820px) and (min-width: 1001px) {
  .classifier-header {
    padding: 10px 14px 5px !important;
  }

  .classifier-title {
    font-size: 15px !important;
  }

  .classifier-subtitle {
    font-size: 10px !important;
  }

  .classifier-content {
    padding: 5px 14px 11px !important;
  }

  .classifier-icon {
    width: 40px !important;
    height: 40px !important;
  }

  .drop-zone {
    padding: 16px 12px;
  }

  .upload-icon {
    margin-bottom: 3px;
  }

  .supported-text {
    margin-top: 5px;
  }

  .upload-btn {
    margin-top: 9px;
    min-height: 40px;
    font-size: 12px;
  }

  .progress {
    margin-top: 6px;
  }
}

/* =========================================================
   VERY SHORT LAPTOP SCREENS
========================================================= */

@media (max-height: 720px) and (min-width: 1001px) {
  .classifier-header {
    padding: 8px 12px 4px !important;
  }

  .classifier-title {
    font-size: 14px !important;
  }

  .classifier-subtitle {
    font-size: 9px !important;
  }

  .classifier-content {
    padding: 4px 12px 9px !important;
  }

  .classifier-icon {
    width: 36px !important;
    height: 36px !important;
  }

  .drop-zone {
    padding: 12px 10px;
    border-radius: 12px;
  }

  .upload-icon {
    font-size: 28px !important;
  }

  .upload-text {
    font-size: 11px;
  }

  .supported-text {
    margin-top: 4px;
    font-size: 9px;
  }

  .file-count {
    margin-top: 5px;
    font-size: 9px;
  }

  .upload-btn {
    margin-top: 7px;
    min-height: 36px;
    border-radius: 10px;
    font-size: 11px;
  }

  .progress {
    margin-top: 5px;
  }
}

/* MOBILE */
@media (max-width: 600px) {
  .classifier-header {
    padding: 12px 14px 7px !important;
  }

  .classifier-content {
    padding: 6px 14px 14px !important;
  }

  .classifier-title {
    font-size: 15px !important;
  }

  .classifier-subtitle {
    font-size: 10px !important;
  }

  .drop-zone {
    padding: 18px 10px;
  }

  .upload-text {
    font-size: 12px;
  }

  .supported-text {
    font-size: 10px;
  }

  .upload-btn {
    min-height: 42px;
  }
}
</style>
