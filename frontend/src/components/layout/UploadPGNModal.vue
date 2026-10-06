<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { supabase } from '@/utils/supabase'

const emit = defineEmits(['loaded'])

const dialog = ref(false)
const fileInput = ref(null)
const file = ref(null)
const loading = ref(false)

const analysisProgress = ref(0)
const analysisStatus = ref('')

const openFile = () => fileInput.value?.click()

const selectFile = (e) => {
  const selected = e.target.files[0]

  if (!selected) return

  file.value = selected
}

const removeFile = () => {
  file.value = null

  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const uploadPGN = async () => {
  if (!file.value) return

  loading.value = true
  analysisProgress.value = 0
  analysisStatus.value = 'Preparing analysis...'

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

    // 2. Analyze the PGN with live progress
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/analyze`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${session.access_token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          pgn: pgn,
        }),
      },
    )

    if (!response.ok) {
      throw new Error(
        `Analysis failed: ${response.status}`
      )
    }

    if (!response.body) {
      throw new Error(
        'Analysis stream is not available.'
      )
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    let buffer = ''
    let analysisData = null

    while (true) {
      const { value, done } = await reader.read()

      if (done) break

      buffer += decoder.decode(
        value,
        { stream: true }
      )

      const events = buffer.split('\n\n')

      buffer = events.pop()

      for (const event of events) {
        const line = event
          .split('\n')
          .find(line =>
            line.startsWith('data: ')
          )

        if (!line) continue

        const payload = JSON.parse(
          line.slice(6)
        )

        if (payload.type === 'progress') {
          analysisProgress.value =
            payload.progress

          analysisStatus.value =
            payload.status
        }

        if (payload.type === 'complete') {
          analysisData =
            payload.analysis
        }

        if (payload.type === 'error') {
          throw new Error(
            payload.message
          )
        }
      }
    }

    if (!analysisData) {
      throw new Error(
        'Analysis did not return a result.'
      )
    }

    if (analysisData.error) {
      throw new Error(
        analysisData.error
      )
    }

    const game =
      uploadRes.data.data?.[0] ||
      uploadRes.data.data

    emit('loaded', {
      game,
      analysis: analysisData,
    })

    dialog.value = false
    removeFile()

  } catch (err) {
    console.error(
      err.response?.data || err
    )

    analysisStatus.value =
      err.message ||
      'Analysis failed.'

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

  <v-dialog
    v-model="dialog"
    max-width="440"
    width="calc(100% - 32px)"
  >
    <v-card rounded="xl">

      <v-card-title
        class="d-flex align-center py-4"
      >
        <v-icon
          color="light-green-darken-2"
          class="mr-3"
        >
          mdi-file-chess
        </v-icon>

        <span class="font-weight-bold">
          Analyze Your Game
        </span>

        <v-spacer />

        <v-btn
          icon="mdi-close"
          variant="text"
          size="small"
          :disabled="loading"
          @click="dialog = false"
        />
      </v-card-title>

      <v-divider />

      <v-card-text class="pa-5">

        <input
          ref="fileInput"
          type="file"
          accept=".pgn"
          hidden
          @change="selectFile"
        />

        <v-sheet
          class="pa-6 text-center"
          rounded="lg"
          border
          color="grey-lighten-5"
          :class="{ 'loading-sheet': loading }"
          @click="!loading && openFile()"
        >

          <v-icon
            size="42"
            color="light-green-darken-2"
          >
            {{
              file
                ? 'mdi-file-document-check'
                : 'mdi-file-upload-outline'
            }}
          </v-icon>

          <div
            class="text-subtitle-1 font-weight-bold mt-2"
          >
            {{ file ? file.name : 'Select a PGN file' }}
          </div>

          <div class="text-caption text-grey mt-1">
            {{
              file
                ? 'PGN file selected'
                : 'Upload your chess game in PGN format'
            }}
          </div>

          <v-btn
            v-if="!file && !loading"
            class="mt-4"
            variant="outlined"
            color="light-green-darken-2"
            rounded="lg"
            @click.stop="openFile"
          >
            Choose File
          </v-btn>

          <v-btn
            v-else-if="file && !loading"
            class="mt-4"
            variant="text"
            color="error"
            size="small"
            @click.stop="removeFile"
          >
            Remove File
          </v-btn>

          <!-- ANALYSIS PROGRESS -->
          <div
            v-if="loading"
            class="mt-5"
            @click.stop
          >

            <div
              class="d-flex justify-space-between align-center mb-2"
            >
              <span class="text-caption text-grey-darken-1">
                {{ analysisStatus }}
              </span>

              <strong class="text-subtitle-2">
                {{ analysisProgress }}%
              </strong>
            </div>

            <v-progress-linear
              :model-value="analysisProgress"
              height="9"
              rounded
              color="light-green-darken-2"
            />

            <div class="text-caption text-grey mt-2">
              Please wait while Stockfish analyzes your game.
            </div>

          </div>

        </v-sheet>

      </v-card-text>

      <v-divider />

      <v-card-actions class="pa-4">

        <v-btn
          variant="text"
          :disabled="loading"
          @click="dialog = false"
        >
          Cancel
        </v-btn>

        <v-spacer />

        <v-btn
          color="light-green-darken-2"
          rounded="lg"
          prepend-icon="mdi-chart-line"
          :loading="false"
          :disabled="!file || loading"
          @click="uploadPGN"
        >
          Analyze Game
        </v-btn>

      </v-card-actions>

    </v-card>
  </v-dialog>
</template>