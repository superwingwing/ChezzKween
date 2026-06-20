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
  fileInput.value?.click()
}

function selectFile(e) {
  const selected = e.target.files[0]
  if (!selected) return

  file.value = selected
  fileName.value = selected.name
}

async function uploadPGN() {
  if (!file.value) return alert("Upload a PGN first")

  loading.value = true

  try {
    const rawPGN = await file.value.text()

    const res = await axios.post("http://127.0.0.1:8000/upload_pgn", {
      pgn: rawPGN
    })

    console.log("BACKEND RESPONSE:", res.data)

    emit("loaded", res.data)

    dialog.value = false
    file.value = null
    fileName.value = ""

  } catch (err) {
    console.error(err.response?.data || err)
    alert("Failed to connect to backend")
  }

  loading.value = false
}
</script>

<template>
  <div style="position: relative; z-index: 9999;">
    <v-btn color="#43A047" @click="open">
      Analyze Your Game
    </v-btn>
  </div>

  <v-dialog v-model="dialog" max-width="500">
    <v-card>
      <v-card-title>Upload PGN</v-card-title>

      <v-card-text>
        <input
          ref="fileInput"
          type="file"
          accept=".pgn"
          hidden
          @change="selectFile"
        />

        <v-btn @click="openFile">Select PGN</v-btn>

        <div v-if="fileName" class="mt-2">
          📄 {{ fileName }}
        </div>

        <v-btn
          class="mt-3"
          color="primary"
          :loading="loading"
          :disabled="!file"
          @click="uploadPGN"
        >
          Analyze Game
        </v-btn>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn text @click="dialog = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>