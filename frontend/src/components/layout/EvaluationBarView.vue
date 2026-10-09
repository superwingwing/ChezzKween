<script setup>
import { computed } from "vue"

const props = defineProps({
  score: {
    type: Number,
    default: 0,
  },
  orientation: {
    type: String,
    default: "white",
  },
})

const whiteHeight = computed(() => {
  const clamped = Math.max(-5, Math.min(5, props.score))
  return ((clamped + 5) / 10) * 100
})

const blackHeight = computed(() => 100 - whiteHeight.value)

const isFlipped = computed(() => props.orientation === "black")
</script>

<template>
  <div
    class="eval-container"
    :class="{ flipped: isFlipped }"
    :aria-label="`Evaluation score: ${score}`"
    role="img"
  >
    <div
      class="black"
      :style="{ height: `${blackHeight}%` }"
    ></div>

    <div class="center-line"></div>

    <div
      class="white"
      :style="{ height: `${whiteHeight}%` }"
    ></div>
  </div>
</template>

<style scoped>
.eval-container {
  position: relative;
  display: flex;
  flex-direction: column;
  flex: 0 0 18px;
  width: 18px;
  height: 100%;
  min-height: 0;
  align-self: stretch;
  overflow: hidden;
  border: 1px solid #333;
  border-radius: 3px;
  box-sizing: border-box;
}

/* Normal orientation: black on top, white on bottom */
.eval-container:not(.flipped) {
  flex-direction: column;
}

/* Flipped orientation: white on top, black on bottom */
.eval-container.flipped {
  flex-direction: column-reverse;
}

.black,
.white {
  width: 100%;
  flex: 0 0 auto;
  transition: height 0.2s ease;
}

.black {
  background: #000;
}

.white {
  background: #fff;
}

.center-line {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 2px;
  background: #f28c28;
  transform: translateY(-50%);
  z-index: 2;
  pointer-events: none;
}

/* Tablet */
@media (max-width: 960px) {
  .eval-container {
    flex-basis: 15px;
    width: 15px;
  }
}

/* Mobile */
@media (max-width: 600px) {
  .eval-container {
    flex-basis: 12px;
    width: 12px;
    border-radius: 2px;
  }

  .center-line {
    height: 2px;
  }
}

/* Very narrow screens */
@media (max-width: 360px) {
  .eval-container {
    flex-basis: 10px;
    width: 10px;
  }
}
</style>

