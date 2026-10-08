<script setup>

import { computed } from "vue"

const props = defineProps({

  score: {
    type: Number,
    default: 0
  },

  orientation: {
    type: String,
    default: "white"
  }

})

const whiteHeight = computed(() => {

  const clamped =
    Math.max(
      -5,
      Math.min(
        5,
        props.score
      )
    )

  return ((clamped + 5) / 10) * 100

})

const blackHeight = computed(() =>
  100 - whiteHeight.value
)

const isFlipped = computed(() =>
  props.orientation === "black"
)

</script>

<template>

  <div
    class="eval-container"
    :class="{
      flipped: isFlipped
    }"
  >

    <div
      class="black"
      :style="{
        height: blackHeight + '%'
      }"
    ></div>

    <div class="center-line"></div>

    <div
      class="white"
      :style="{
        height: whiteHeight + '%'
      }"
    ></div>

  </div>

</template>

<style scoped>

.eval-container {

  position: relative;

  width: 18px;

  height: 600px;

  display: flex;

  flex-direction: column;

  flex-shrink: 0;

  overflow: hidden;

  border: 2px solid #333;

  border-radius: 4px;

  box-sizing: border-box;

}

/* =========================================
   NORMAL BOARD
   Black = TOP
   White = BOTTOM
========================================= */

.eval-container:not(.flipped) {

  flex-direction: column;

}

/* =========================================
   FLIPPED BOARD
   White = TOP
   Black = BOTTOM
========================================= */

.eval-container.flipped {

  flex-direction: column-reverse;

}

/* =========================================
   BLACK
========================================= */

.black {

  width: 100%;

  background: #000;

  transition:
    height 0.2s ease;

}

/* =========================================
   WHITE
========================================= */

.white {

  width: 100%;

  background: #fff;

  transition:
    height 0.2s ease;

}

/* =========================================
   CENTER LINE
========================================= */

.center-line {

  position: absolute;

  top: 50%;

  left: 0;

  width: 100%;

  height: 2px;

  background: red;

  transform: translateY(-50%);

  z-index: 10;

}

/* =========================================
   TABLET
========================================= */

@media (max-width: 960px) {

  .eval-container {

    width: 16px;

    height: 600px;

  }

}

/* =========================================
   MOBILE
========================================= */

@media (max-width: 600px) {

  .eval-container {

    width: 14px;

    height: auto;

    aspect-ratio: 1 / 40;

  }

}

</style>
