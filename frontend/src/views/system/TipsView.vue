<script setup>
import { ref } from "vue"

const currentStep = ref(0)

const tips = [
  {
    title: "Analyze a Specific Game",
    description:
      "Upload a PGN file to analyze a specific chess game, review moves, evaluation, and recommendations.",
    image: "/images/tips/game-analysis.png",
  },
  {
    title: "Classify Your Playing Style",
    description:
      "Upload multiple PGN games to analyze your playing patterns and classify your style as Aggressive or Positional.",
    image: "/images/tips/style-classification.png",
  },
]

const nextStep = () => {
  if (currentStep.value < tips.length - 1) {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const goToStep = (index) => {
  currentStep.value = index
}
</script>

<template>
  <v-container
    fluid
    class="py-8"
    style="max-width: 1000px;"
  >
    <!-- HEADER -->
    <div class="text-center mb-6">
      <div
        class="text-overline font-weight-bold"
        style="color: #F28C28;"
      >
        CHESSKWEEN GUIDE
      </div>

      <h1
        class="text-h4 font-weight-bold"
        style="color: #0B1F3A;"
      >
        How to Use ChessKween
      </h1>

      <p class="text-body-2 text-medium-emphasis mt-2">
        Follow these simple steps to get the most out of ChessKween.
      </p>
    </div>

    <!-- TUTORIAL CARD -->
    <v-card
      rounded="xl"
      elevation="3"
      class="pa-6"
      style="
        border: 1px solid #E5E9EF;
        background: #FFFFFF;
      "
    >
      <!-- STEP -->
      <div class="text-center">
        <v-chip
          size="small"
          variant="tonal"
          color="orange-darken-2"
          class="font-weight-bold mb-2"
        >
          Step {{ currentStep + 1 }} of {{ tips.length }}
        </v-chip>

        <!-- TITLE -->
        <h2
          class="text-h5 font-weight-bold mb-4"
          style="color: #0B1F3A;"
        >
          {{ tips[currentStep].title }}
        </h2>
      </div>

      <!-- IMAGE -->
      <v-hover v-slot="{ isHovering, props }">
        <div
          v-bind="props"
          class="mx-auto"
          style="max-width: 800px; cursor: pointer;"
          @click="nextStep"
        >
          <v-card
            rounded="lg"
            border
            class="overflow-hidden position-relative"
            :elevation="isHovering ? 4 : 1"
          >
            <v-img
              :src="tips[currentStep].image"
              aspect-ratio="16/9"
              cover
              class="bg-grey-lighten-4"
              :style="{
                transform: isHovering ? 'scale(1.01)' : 'scale(1)',
                transition: 'transform .2s ease'
              }"
            />

            <!-- NEXT OVERLAY -->
            <v-chip
              v-if="currentStep < tips.length - 1"
              size="small"
              color="white"
              class="position-absolute"
              style="
                right: 12px;
                bottom: 12px;
                background: rgba(7, 23, 45, .88) !important;
                color: white !important;
              "
            >
              Click image to continue
              <v-icon end size="16">
                mdi-arrow-right
              </v-icon>
            </v-chip>
          </v-card>
        </div>
      </v-hover>

      <!-- DESCRIPTION -->
      <v-card-text class="text-center mx-auto px-2" style="max-width: 700px;">
        <p class="text-body-1 text-medium-emphasis mb-0">
          {{ tips[currentStep].description }}
        </p>
      </v-card-text>

      <!-- DOTS -->
      <div class="d-flex justify-center align-center ga-2 my-3">
        <v-btn
          v-for="(tip, index) in tips"
          :key="index"
          icon
          size="x-small"
          variant="text"
          :aria-label="`Go to step ${index + 1}`"
          @click="goToStep(index)"
        >
          <v-icon
            size="12"
            :color="currentStep === index ? 'orange-darken-2' : 'grey-lighten-1'"
          >
            mdi-circle
          </v-icon>
        </v-btn>
      </div>

      <!-- CONTROLS -->
      <div class="d-flex justify-center ga-3">
        <v-btn
          variant="outlined"
          color="blue-grey-darken-3"
          rounded="lg"
          :disabled="currentStep === 0"
          @click="previousStep"
        >
          <v-icon start>
            mdi-arrow-left
          </v-icon>
          Previous
        </v-btn>

        <v-btn
          color="orange-darken-2"
          rounded="lg"
          :disabled="currentStep === tips.length - 1"
          @click="nextStep"
        >
          Next
          <v-icon end>
            mdi-arrow-right
          </v-icon>
        </v-btn>
      </div>
    </v-card>
  </v-container>
</template>