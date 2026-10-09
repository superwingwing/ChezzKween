<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { supabase } from '@/utils/supabase'
import AlertNotification from '../common/AlertNotification.vue'

const formSuccessMessage = ref('')
const formErrorMessage = ref('')

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
  formSuccessMessage.value = ''
  formErrorMessage.value = ''

  try {
    const pgn = await file.value.text()

    const {
      data: { user },
      error: userError,
    } = await supabase.auth.getUser()

    if (userError || !user) {
      throw new Error('Please sign in before analyzing a game.')
    }

    const {
      data: { session },
      error: sessionError,
    } = await supabase.auth.getSession()

    if (sessionError || !session) {
      throw new Error('Your session has expired. Please sign in again.')
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
        pgn,
        user_id: user.id,
      },
      config,
    )

    // 2. Analyze the PGN
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/analyze`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${session.access_token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          pgn,
        }),
      },
    )

    if (!response.ok) {
      throw new Error(`Analysis failed: ${response.status}`)
    }

    if (!response.body) {
      throw new Error('Analysis stream is not available.')
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    let buffer = ''
    let analysisData = null

    while (true) {
      const { value, done } = await reader.read()

      if (done) break

      buffer += decoder.decode(value, { stream: true })

      const events = buffer.split('\n\n')
      buffer = events.pop()

      for (const event of events) {
        const line = event
          .split('\n')
          .find(line => line.startsWith('data: '))

        if (!line) continue

        const payload = JSON.parse(line.slice(6))

        if (payload.type === 'progress') {
          analysisProgress.value = payload.progress
          analysisStatus.value = payload.status
        }

        if (payload.type === 'complete') {
          analysisData = payload.analysis
        }

        if (payload.type === 'error') {
          throw new Error(payload.message)
        }
      }
    }

    if (!analysisData) {
      throw new Error('Analysis did not return a result.')
    }

    if (analysisData.error) {
      throw new Error(analysisData.error)
    }

    formSuccessMessage.value = 'Game analyzed successfully!'
    formErrorMessage.value = ''

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
    // console.error(err.response?.data || err)

    formErrorMessage.value = err.response?.data?.detail || err.message ||
      'Failed to analyze your game. Please try again.'

    analysisStatus.value =
      err.message || 'Analysis failed.'

  } finally {
    loading.value = false
  }
}
</script>

<template>

  <v-btn
    color="#F28C28"
    variant="flat"
    prepend-icon="mdi-cloud-upload-outline"
    rounded="lg"
    height="40"
    class="text-white font-weight-bold"
    @click="dialog = true"
  >
    Analyze Your Game
  </v-btn>

  <AlertNotification
  :form-success-message="formSuccessMessage"
  :form-error-message="formErrorMessage"
/>


  <!-- =====================================================
       UPLOAD DIALOG
  ====================================================== -->

  <v-dialog
    v-model="dialog"
    max-width="480"
    width="calc(100% - 32px)"
  >
    <v-card
      rounded="xl"
      elevation="12"
    >

      <!-- HEADER -->

      <v-card-title
        class="d-flex align-center px-5 py-4"
      >
        <v-avatar
          color="#FFF3E4"
          size="40"
          class="mr-3"
        >
          <v-icon color="#F28C28">
            mdi-file-chess
          </v-icon>
        </v-avatar>

        <div>
          <div class="text-subtitle-1 font-weight-bold">
            Analyze Your Game
          </div>

          <div class="text-caption text-grey">
            Upload a PGN and let Stockfish analyze it
          </div>
        </div>

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


      <!-- CONTENT -->

      <v-card-text class="pa-5">

        <input
          ref="fileInput"
          type="file"
          accept=".pgn"
          hidden
          @change="selectFile"
        />
        <!-- UPLOAD AREA -->

        <v-sheet
          border
          rounded="xl"
          class="pa-7 text-center"
          color="#F8FAFC"
          :class="{ 'bg-grey-lighten-4': loading }"
          @click="!loading && openFile()"
        >

          <v-avatar
            size="54"
            color="#FFF3E4"
          >
            <v-icon
              size="28"
              color="#F28C28"
            >
              {{
                file
                  ? 'mdi-file-document-check'
                  : 'mdi-cloud-upload-outline'
              }}
            </v-icon>
          </v-avatar>

          <div class="text-subtitle-1 font-weight-bold mt-3">
            {{ file ? file.name : 'Upload your PGN file' }}
          </div>

          <div class="text-caption text-grey mt-1">
            {{
              file
                ? 'PGN file selected successfully'
                : 'Click here to select a chess game in PGN format'
            }}
          </div>


          <!-- CHOOSE FILE -->

          <v-btn
            v-if="!file && !loading"
            class="mt-4"
            variant="outlined"
            color="#F28C28"
            rounded="lg"
            @click.stop="openFile"
          >
            Choose PGN File
          </v-btn>


          <!-- REMOVE -->

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


          <!-- PROGRESS -->

          <div
            v-if="loading"
            class="mt-5 text-left"
            @click.stop
          >

            <div
              class="d-flex justify-space-between align-center mb-2"
            >
              <span class="text-caption text-grey-darken-1">
                {{ analysisStatus }}
              </span>

              <strong class="text-caption">
                {{ analysisProgress }}%
              </strong>
            </div>

            <v-progress-linear
              :model-value="analysisProgress"
              height="8"
              rounded
              color="#F28C28"
            />

            <div class="text-caption text-grey mt-2">
              Stockfish is analyzing your game...
            </div>

          </div>

        </v-sheet>

      </v-card-text>


      <v-divider />


      <!-- ACTIONS -->

      <v-card-actions class="px-5 py-4">

        <v-btn
          variant="text"
          :disabled="loading"
          @click="dialog = false"
        >
          Cancel
        </v-btn>

        <v-spacer />

        <v-btn
          color="#F28C28"
          variant="flat"
          rounded="lg"
          prepend-icon="mdi-chart-line"
          :loading="loading"
          :disabled="!file || loading"
          class="text-white font-weight-bold"
          @click="uploadPGN"
        >
          Analyze Game
        </v-btn>

      </v-card-actions>

    </v-card>
  </v-dialog>
</template>