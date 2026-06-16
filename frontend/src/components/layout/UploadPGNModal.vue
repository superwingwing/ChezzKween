<script setup>
import { ref } from "vue"
import axios from "axios"

const emit = defineEmits(["loaded"])

const dialog = ref(false)
const fileInput = ref(null)
const file = ref(null)
const fileName = ref("")
const loading = ref(false)

function open() {
  dialog.value = true
}

function openFile() {
  fileInput.value.click()
}

function selectFile(e) {
  file.value = e.target.files[0]
  fileName.value = file.value?.name || ""
}

async function uploadPGN() {
  if (!file.value) return alert("Upload a PGN first")

  loading.value = true
  const formData = new FormData()
  formData.append("file", file.value)

  try {
    const res = await axios.post("http://127.0.0.1:8000/upload_pgn", formData)

    emit("loaded", res.data.moves || [])
    dialog.value = false

    // reset
    file.value = null
    fileName.value = ""
  } catch (err) {
    console.error(err)
    alert("Failed to load PGN")
  }

  loading.value = false
}
</script>

<template>
  <!-- ONE BUTTON -->
  <div style="position: relative; z-index: 9999;">
  <v-btn color="#4CAF50" @click="open">
    Analyze Your Game
  </v-btn>
</div>

  <!-- MODAL -->
  <v-dialog v-model="dialog" max-width="500">
    <v-card>
      <v-card-title>Upload PGN</v-card-title>

      <v-card-text>
        <input
          ref="fileInput"
          type="file"
          accept=".pgn"
          @change="selectFile"
          hidden
        />

        <v-btn @click="openFile">Select PGN</v-btn>

        <div v-if="fileName" class="mt-2">
          📄 {{ fileName }}
        </div>

        <v-btn
          class="mt-3"
          :loading="loading"
          :disabled="!file"
          @click="uploadPGN"
          color="primary"
        >
          Load Game
        </v-btn>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn text @click="dialog = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>