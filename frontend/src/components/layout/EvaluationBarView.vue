<script setup>
import { computed } from "vue"

const props = defineProps({
  score: {
    type: Number,
    default: 0
  }
})

/*
  Clamp Stockfish eval between -5 and +5
  Then convert to percentage for bar height
*/
const whiteHeight = computed(() => {
  const clamped = Math.max(-5, Math.min(5, props.score))
  return ((clamped + 5) / 10) * 100
})

const blackHeight = computed(() => 100 - whiteHeight.value)
</script>

<template>
  <div class="eval-container">
    <div class="black" :style="{ height: blackHeight + '%' }"></div>
    <div class="white" :style="{ height: whiteHeight + '%' }"></div>
    
  </div>
</template>

<style scoped>
.eval-container {
  width: 18px;
  height: 650px;
  display: flex;
  flex-direction: column;
  border-radius: 6px;
  overflow: hidden;
  border: 2px solid #333;
}

/* White advantage */
.white {
  background: #ffffff;
  transition: height 0.2s ease;
}

/* Black advantage */
.black {
  background: #000000;
  transition: height 0.2s ease;
}
</style>