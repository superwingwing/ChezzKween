<script setup>
import { ref } from "vue"

const currentStep = ref(0)

const tips = [
  {
    title: "Analyze a Specific Game",
    description:
      "Upload a PGN file to analyze a specific chess game, review moves, evaluation, and recommendations.",
    image: "/images/tips/game-analysis.png"
  },
  {
    title: "Classify Your Playing Style",
    description:
      "Upload multiple PGN games to analyze your playing patterns and classify your style as Aggressive or Positional.",
    image: "/images/tips/style-classification.png"
  }
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
  <div class="tips-page">

    <!-- Header -->
    <div class="tips-header">
      <h1>How to Use ChessKween</h1>
      <p>
        Follow these simple steps to get the most out of ChessKween.
      </p>
    </div>

    <!-- Tutorial Card -->
    <v-card
      class="tips-card"
      elevation="3"
      rounded="xl"
    >

      <!-- Step -->
      <div class="step-number">
        Step {{ currentStep + 1 }} of {{ tips.length }}
      </div>

      <!-- Title -->
      <h2 class="tip-title">
        {{ tips[currentStep].title }}
      </h2>

      <!-- Clickable Image -->
      <div
        class="tip-image-wrapper"
        @click="nextStep"
      >
        <v-img
          :src="tips[currentStep].image"
          class="tip-image"
          cover
          rounded="lg"
        />

        <div
          v-if="currentStep < tips.length - 1"
          class="image-next"
        >
          Click image to continue
          <v-icon size="18">
            mdi-arrow-right
          </v-icon>
        </div>
      </div>

      <!-- Description -->
      <p class="tip-description">
        {{ tips[currentStep].description }}
      </p>

      <!-- Dots -->
      <div class="step-dots">
        <button
          v-for="(tip, index) in tips"
          :key="index"
          class="dot"
          :class="{ active: currentStep === index }"
          @click="goToStep(index)"
        />
      </div>

      <!-- Controls -->
      <div class="tip-controls">

        <v-btn
          variant="outlined"
          :disabled="currentStep === 0"
          @click="previousStep"
        >
          <v-icon start>
            mdi-arrow-left
          </v-icon>
          Previous
        </v-btn>

        <v-btn
          color="light-blue-darken-4"
          variant="flat"
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

  </div>
</template>

<style scoped>
.tips-page {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 30px 20px 40px;
  box-sizing: border-box;
}

.tips-header {
  text-align: center;
  margin-bottom: 25px;
}

.tips-header h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #01579b;
}

.tips-header p {
  margin: 8px 0 0;
  font-size: 14px;
  color: #666;
}

.tips-card {
  width: 100%;
  padding: 28px;
  box-sizing: border-box;
  text-align: center;
}

.step-number {
  font-size: 13px;
  font-weight: 600;
  color: #777;
  margin-bottom: 8px;
}

.tip-title {
  margin: 0 0 20px;
  font-size: 24px;
  font-weight: 700;
}

.tip-image-wrapper {
  position: relative;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  cursor: pointer;
  overflow: hidden;
  border-radius: 10px;
}

.tip-image {
  width: 100%;
  background: #f5f5f5;
  transition: transform 0.2s ease;
}

.tip-image-wrapper:hover .tip-image {
  transform: scale(1.01);
}

.image-next {
  position: absolute;
  bottom: 12px;
  right: 12px;

  display: flex;
  align-items: center;
  gap: 5px;

  padding: 7px 12px;
  border-radius: 20px;

  background: rgba(0, 0, 0, 0.65);
  color: white;

  font-size: 12px;
}

.tip-description {
  max-width: 700px;
  margin: 20px auto;
  font-size: 15px;
  line-height: 1.6;
  color: #555;
}

.step-dots {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin: 20px 0;
}

.dot {
  width: 9px;
  height: 9px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: #ccc;
  cursor: pointer;
  transition: 0.2s ease;
}

.dot.active {
  width: 11px;
  height: 11px;
  background: #01579b;
}

.tip-controls {
  display: flex;
  justify-content: center;
  gap: 10px;
}

@media (max-width: 600px) {
  .tips-page {
    padding: 20px 10px 30px;
  }

  .tips-header h1 {
    font-size: 23px;
  }

  .tips-card {
    padding: 18px 12px;
  }

  .tip-title {
    font-size: 20px;
    margin-bottom: 15px;
  }

  .tip-description {
    font-size: 13px;
  }

  .tip-controls {
    gap: 6px;
  }
}
</style>