<script setup>
import { ref, watch, onBeforeUnmount } from "vue"

const props = defineProps({
  analysis: {
    type: Object,
    default: null
  }
})

const isSpeaking = ref(false)

const getSpeechText = () => {
  if (!props.analysis) return ""

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
  if (!props.analysis || !("speechSynthesis" in window)) return

  window.speechSynthesis.cancel()

  const utterance = new SpeechSynthesisUtterance(
    getSpeechText()
  )

  const voices = window.speechSynthesis.getVoices()

  const femaleVoice =
    voices.find(voice =>
      /female|zira|samantha|karen|victoria|susan|aria|jenny|libby|hazel/i.test(
        voice.name
      )
    ) ||
    voices.find(voice =>
      voice.lang.startsWith("en")
    )

  if (femaleVoice) {
    utterance.voice = femaleVoice
    utterance.lang = femaleVoice.lang
  } else {
    utterance.lang = "en-US"
  }

  utterance.rate = 0.88
  utterance.pitch = 1.18
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
  if ("speechSynthesis" in window) {
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
  <v-card
    class="coach-card"
    elevation="0"
  >

    <!-- HEADER -->
    <v-card-item class="coach-header">

      <template #prepend>
        <div class="coach-avatar">
          <v-img
            src="/images/chesskween-coach.png"
            alt="ChessKween Coach"
            cover
          />
          <span class="online-dot"></span>
        </div>
      </template>

      <v-card-title class="pa-0 coach-title">
        ChessKween AI Coach
      </v-card-title>

      <v-card-subtitle class="pa-0 coach-subtitle">
        Style-Aware Recommendation System
      </v-card-subtitle>

      <template #append>
        <v-chip
          size="small"
          variant="outlined"
          class="best-chip"
        >
          <!-- BEST MOVE -->
           {{ analysis.quality || "Chess Analysis" }} move
        </v-chip>
      </template>

    </v-card-item>

    <v-divider />

    <v-card-text class="coach-content">

      <!-- NO ANALYSIS -->
      <div
        v-if="!analysis"
        class="empty-state"
      >
        <v-icon
          size="42"
          color="#F28C28"
        >
          mdi-chess-queen
        </v-icon>

        <strong>ChessKween is ready!</strong>

        <span>
          Upload a game to receive coaching feedback.
        </span>
      </div>

      <!-- ANALYSIS -->
      <template v-else>

        <!-- RECOMMENDED MOVE -->
        <div class="recommended-box">

          <div>
            <div class="recommended-label">
              PLAYED MOVE
            </div>

            <div class="recommended-move">
              {{ analysis.move || "—" }}
            </div>
          </div>

          <v-btn
            v-if="!isSpeaking"
            class="listen-btn"
            variant="flat"
            prepend-icon="mdi-volume-high"
            @click="speakCoach"
          >
            Listen to Coach
          </v-btn>

          <v-btn
            v-else
            class="listen-btn"
            variant="flat"
            prepend-icon="mdi-stop"
            @click="stopSpeaking"
          >
            Stop
          </v-btn>

        </div>

        <!-- EXPLANATION -->
        <div class="explanation-box">

          <div class="explanation-title">
            <v-icon
              size="18"
              color="#F28C28"
            >
              mdi-lightbulb-on
            </v-icon>

            {{ analysis.quality || "Chess Analysis" }}
          </div>

          <p>
            {{ analysis.explanation || "No explanation available." }}
          </p>

          <template v-if="analysis.recommendation">
            <div class="recommendation-title">
              <v-icon
                size="17"
                color="#F28C28"
              >
                mdi-chess-queen
              </v-icon>

              Recommendation
            </div>

            <p>
              {{ analysis.recommendation }}
            </p>
          </template>

        </div>

        <!-- MOVE NOTATION -->
        <div
          v-if="analysis.move"
          class="notation-section"
        >
          <div class="notation-title">
            CURRENT MOVE
          </div>

          <div class="move-item active">
            <span>Move</span>
            <strong>{{ analysis.move }}</strong>
          </div>
        </div>

      </template>

    </v-card-text>

  </v-card>
</template>

<style scoped>
.coach-card {
  width: 100%;
  height: 420px;
  display: flex;
  flex-direction: column;
  border: 1px solid #191a1b;
  border-radius: 18px;
  background: #ffffff;
  color: #0b1f3a;
  overflow: hidden;
}

/* HEADER */
.coach-header {
  padding: 16px 18px 12px !important;
}

.coach-avatar {
  position: relative;
  width: 52px;
  height: 52px;
  overflow: visible;
  border: 2px solid #f28c28;
  border-radius: 15px;
  background: #0b1f3a;
}

.coach-avatar :deep(.v-img) {
  border-radius: 13px;
}

.online-dot {
  position: absolute;
  right: -4px;
  bottom: -4px;
  width: 13px;
  height: 13px;
  border: 2px solid white;
  border-radius: 50%;
  background: #20b486;
}

.coach-title {
  color: #0b1f3a !important;
  font-size: 19px !important;
  font-weight: 800 !important;
  line-height: 1.2;
}

.coach-subtitle {
  margin-top: 3px;
  color: #121314 !important;
  font-size: 12px !important;
}

.best-chip {
  color: #f28c28 !important;
  border-color: #f8c28e !important;
  background: #fffaf5;
  font-size: 10px;
  font-weight: 800;
}

/* CONTENT - SCROLLABLE */
.coach-content {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 14px 18px 18px !important;
}

/* RECOMMENDED MOVE */
.recommended-box {
  min-height: 92px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 15px 20px;
  border-radius: 14px;
  background: #0b1328;
  box-shadow: 0 8px 16px rgba(11, 19, 40, 0.14);
}

.recommended-label {
  color: #91a4bf;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 1px;
}

.recommended-move {
  margin-top: 3px;
  color: #f28c28;
  font-size: 30px;
  font-weight: 800;
  line-height: 1;
}

.listen-btn {
  min-width: 150px;
  height: 40px !important;
  border-radius: 12px !important;
  background: #ff7517 !important;
  color: white !important;
  font-size: 12px;
  font-weight: 700;
  text-transform: none;
}

/* EXPLANATION */
.explanation-box {
  margin-top: 18px;
  padding: 17px 18px;
  border: 1px solid #dfe7f0;
  border-radius: 14px;
  background: #f8fafc;
}

.explanation-title,
.recommendation-title {
  display: flex;
  align-items: center;
  gap: 7px;
  color: #101827;
  font-size: 14px;
  font-weight: 800;
}

.explanation-box p {
  margin: 10px 0 0;
  color: #38506d;
  font-size: 13px;
  line-height: 1.6;
}

.recommendation-title {
  margin-top: 15px;
}

/* MOVE NOTATION */
.notation-section {
  margin-top: 18px;
}

.notation-title {
  margin-bottom: 8px;
  color: #8998ad;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.8px;
}

.move-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 9px 12px;
  border: 1px solid #dce5ef;
  border-radius: 10px;
  background: #f4f7fa;
  color: #8998ad;
  font-size: 13px;
}

.move-item.active {
  border-color: #ffc98f;
  background: #fff7ed;
  color: #f28c28;
}

.move-item strong {
  color: #0b1f3a;
}

.move-item.active strong {
  color: #dc7311;
}

/* EMPTY */
.empty-state {
  min-height: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-align: center;
}

.empty-state strong {
  color: #0b1f3a;
  font-size: 16px;
}

.empty-state span {
  max-width: 230px;
  color: #8190a5;
  font-size: 12px;
  line-height: 1.5;
}

/* SCROLLBAR */
.coach-content::-webkit-scrollbar {
  width: 6px;
}

.coach-content::-webkit-scrollbar-track {
  background: transparent;
}

.coach-content::-webkit-scrollbar-thumb {
  border-radius: 10px;
  background: #cbd5e1;
}

.coach-content::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* RESPONSIVE */
@media (max-width: 600px) {
  .coach-header {
    padding: 14px !important;
  }

  .recommended-box {
    padding: 14px;
  }

  .recommended-move {
    font-size: 26px;
  }

  .listen-btn {
    min-width: 130px;
  }
}
</style>