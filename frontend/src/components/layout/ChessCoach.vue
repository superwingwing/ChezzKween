
<script setup>
import { ref, watch, onBeforeUnmount } from 'vue'

const props = defineProps({
  analysis: {
    type: Object,
    default: null
  }
})

const isSpeaking = ref(false)

const getSpeechText = () => {
  if (!props.analysis) return ''

  let text = `Move ${props.analysis.move}. ${props.analysis.quality}. `

  if (props.analysis.explanation) {
    text += `Explanation: ${props.analysis.explanation}. `
  }

  if (props.analysis.recommendation) {
    text += `Recommendation: ${props.analysis.recommendation}.`
  }

  return text
}

const speakCoach = () => {
  if (!props.analysis || !('speechSynthesis' in window)) return

  window.speechSynthesis.cancel()

  const text = getSpeechText()
  const utterance = new SpeechSynthesisUtterance(text)

  utterance.rate = 0.95
  utterance.pitch = 1.05
  utterance.volume = 1

  utterance.onstart = () => {
    isSpeaking.value = true
  }

  utterance.onend = () => {
    isSpeaking.value = false
  }

  utterance.onerror = () => {
    isSpeaking.value = false
  }

  window.speechSynthesis.speak(utterance)
}

const stopSpeaking = () => {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel()
  }

  isSpeaking.value = false
}

watch(
  () => props.analysis,
  () => {
    stopSpeaking()
  }
)

onBeforeUnmount(() => {
  stopSpeaking()
})
</script>

<template>
  <v-card class="coach-card" elevation="4">

    <v-card-title class="coach-header">
      <div class="coach-avatar">
        <v-img
          src="/images/chesskween-coach.png"
          alt="ChessKween Coach"
          cover
        />
      </div>

      <div class="coach-title">
        <span>ChessKween</span>
        <small>Your Chess Coach</small>
      </div>
    </v-card-title>

    <v-divider />

    <v-card-text class="coach-content">

      <template v-if="analysis">

        <div class="move-row">
          <span class="label">Move</span>
          <strong>{{ analysis.move }}</strong>
        </div>

        <div class="quality">
          {{ analysis.quality }}
        </div>

        <section class="section">
          <h4>
            <v-icon icon="mdi-lightbulb-outline" />
            Explanation
          </h4>

          <p>
            {{ analysis.explanation }}
          </p>
        </section>

        <section
          v-if="analysis.recommendation"
          class="section"
        >
          <h4>
            <v-icon icon="mdi-chess-queen" />
            Recommendation
          </h4>

          <p>
            {{ analysis.recommendation }}
          </p>
        </section>

        <div class="voice-controls">
          <v-btn
            v-if="!isSpeaking"
            class="speak-btn"
            variant="flat"
            prepend-icon="mdi-volume-high"
            @click="speakCoach"
          >
            Listen to ChessKween
          </v-btn>

          <v-btn
            v-else
            class="stop-btn"
            variant="flat"
            prepend-icon="mdi-stop"
            @click="stopSpeaking"
          >
            Stop
          </v-btn>
        </div>

      </template>

      <div
        v-else
        class="empty-state"
      >
        <div class="empty-avatar">
          <v-img
            src="/images/chesskween-coach.png"
            alt="ChessKween Coach"
            cover
          />
        </div>

        <strong>ChessKween is ready!</strong>

        <p>
          Upload a game to receive coaching feedback.
        </p>
      </div>

    </v-card-text>
  </v-card>
</template>

<style scoped>
.coach-card {
  width: 100%;
  max-width: 320px;
  height: 420px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-radius: 16px;
  background: #ffffff;
  color: #17212b;
  border: 1px solid #dce7f2;
}

.coach-header {
  min-height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 10px 16px;
  color: #12395b;
}

.coach-avatar {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  overflow: hidden;
  border-radius: 50%;
  border: 2px solid #2878c8;
  background: #eef6fd;
}

.coach-title {
  display: flex;
  flex-direction: column;
  line-height: 1.15;
}

.coach-title span {
  font-size: 18px;
  font-weight: 700;
}

.coach-title small {
  margin-top: 3px;
  color: #64748b;
  font-size: 11px;
  font-weight: 500;
}

.coach-content {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 16px;
}

.move-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
  padding: 10px 12px;
  border-radius: 10px;
  background: #f3f7fb;
  color: #12395b;
}

.label {
  color: #64748b;
  font-size: 13px;
}

.move-row strong {
  font-size: 17px;
  color: #12395b;
}

.quality {
  padding: 9px 12px;
  border-radius: 10px;
  background: #2878c8;
  color: white;
  text-align: center;
  font-size: 14px;
  font-weight: 700;
  text-transform: capitalize;
}

.section {
  margin-top: 18px;
}

.section h4 {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0 0 7px;
  color: #2878c8;
  font-size: 14px;
  font-weight: 700;
}

.section p {
  margin: 0;
  color: #4b5f73;
  font-size: 13px;
  line-height: 1.6;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.voice-controls {
  display: flex;
  justify-content: center;
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid #e4edf5;
}

.speak-btn,
.stop-btn {
  border-radius: 10px;
  text-transform: none;
  font-size: 12px;
  font-weight: 600;
}

.speak-btn {
  background: #2878c8;
  color: white;
}

.stop-btn {
  background: #e8eef5;
  color: #12395b;
}

.empty-state {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  text-align: center;
  color: #64748b;
}

.empty-avatar {
  width: 110px;
  height: 110px;
  margin-bottom: 4px;
  overflow: hidden;
  border-radius: 50%;
  border: 3px solid #2878c8;
  background: #eef6fd;
}

.empty-state strong {
  color: #12395b;
  font-size: 15px;
}

.empty-state p {
  max-width: 220px;
  margin: 0;
  font-size: 13px;
  line-height: 1.5;
}

@media (max-width: 960px) {
  .coach-card {
    max-width: 100%;
    height: 380px;
  }
}

@media (max-width: 600px) {
  .coach-card {
    width: 100%;
    max-width: none;
    height: 360px;
    border-radius: 14px;
  }

  .coach-header {
    font-size: 16px;
  }

  .coach-content {
    padding: 14px;
  }

  .section p {
    font-size: 12.5px;
  }

  .empty-avatar {
    width: 90px;
    height: 90px;
  }
}
</style>
