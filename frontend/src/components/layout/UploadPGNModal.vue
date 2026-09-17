<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { supabase } from '@/utils/supabase'

const emit = defineEmits(['loaded'])

const dialog = ref(false)
const fileInput = ref(null)
const file = ref(null)
const loading = ref(false)

const openFile = () => fileInput.value?.click()

const selectFile = (e) => {
  const selected = e.target.files[0]
  if (!selected) return
  file.value = selected
}

const removeFile = () => {
  file.value = null
  if (fileInput.value) fileInput.value.value = ''
}

const uploadPGN = async () => {
  if (!file.value) return

  loading.value = true

  try {
    const pgn = await file.value.text()

    const {
      data: { user },
      error: userError,
    } = await supabase.auth.getUser()

    if (userError || !user) {
      console.error('User not authenticated')
      return
    }

    const {
      data: { session },
      error: sessionError,
    } = await supabase.auth.getSession()

    if (sessionError || !session) {
      console.error('No active Supabase session')
      return
    }

    const config = {
      headers: {
        Authorization: `Bearer ${session.access_token}`,
      },
    }

    // 1. Store/load the PGN
    const uploadRes = await axios.post(
       `${import.meta.env.VITE_API_URL}/upload_pgn`,
      {
        pgn: pgn,
        user_id: user.id,
      },
      config,
    )

    // 2. Analyze the PGN
    const analysisRes = await axios.post(
      `${import.meta.env.VITE_API_URL}/analyze`,
      {
        pgn: pgn,
      },
      config,
    )

    const game = uploadRes.data.data?.[0] || uploadRes.data.data

    emit('loaded', {
      game,
      analysis: analysisRes.data,
    })

    dialog.value = false
    removeFile()
  } catch (err) {
    console.error(err.response?.data || err)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-btn
    color="light-blue-darken-4"
    prepend-icon="mdi-chess-king"
    rounded="lg"
    @click="dialog = true"
  >
    Analyze Your Game
  </v-btn>

  <v-dialog v-model="dialog" max-width="440" width="calc(100% - 32px)">
    <v-card rounded="xl">
      <v-card-title class="d-flex align-center py-4">
        <v-icon color="light-green-darken-2" class="mr-3"> mdi-file-chess </v-icon>
        <span class="font-weight-bold">Analyze Your Game</span>

        <v-spacer />

        <v-btn icon="mdi-close" variant="text" size="small" @click="dialog = false" />
      </v-card-title>

      <v-divider />

      <v-card-text class="pa-5">
        <input ref="fileInput" type="file" accept=".pgn" hidden @change="selectFile" />

        <v-sheet
          class="pa-6 text-center"
          rounded="lg"
          border
          color="grey-lighten-5"
          @click="openFile"
        >
          <v-icon size="42" color="light-green-darken-2">
            {{ file ? 'mdi-file-document-check' : 'mdi-file-upload-outline' }}
          </v-icon>

          <div class="text-subtitle-1 font-weight-bold mt-2">
            {{ file ? file.name : 'Select a PGN file' }}
          </div>

          <div class="text-caption text-grey mt-1">
            {{ file ? 'PGN file selected' : 'Upload your chess game in PGN format' }}
          </div>

          <v-btn
            v-if="!file"
            class="mt-4"
            variant="outlined"
            color="light-green-darken-2"
            rounded="lg"
            @click.stop="openFile"
          >
            Choose File
          </v-btn>

          <v-btn
            v-else
            class="mt-4"
            variant="text"
            color="error"
            size="small"
            @click.stop="removeFile"
          >
            Remove File
          </v-btn>
        </v-sheet>
      </v-card-text>

      <v-divider />

      <v-card-actions class="pa-4">
        <v-btn variant="text" :disabled="loading" @click="dialog = false"> Cancel </v-btn>

        <v-spacer />

        <v-btn
          color="light-green-darken-2"
          rounded="lg"
          prepend-icon="mdi-chart-line"
          :loading="loading"
          :disabled="!file"
          @click="uploadPGN"
        >
          Analyze Game
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
