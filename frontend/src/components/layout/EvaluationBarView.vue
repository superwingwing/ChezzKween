<script setup>
import { computed } from "vue"

const props = defineProps({
  score: {
    type: Number,
    default: 0
  }
})

// convert engine score → %
function evalToPercent(score) {
  const max = 5
  const clamped = Math.max(Math.min(score, max), -max)
  return ((clamped + max) / (2 * max)) * 100
}

const height = computed(() => evalToPercent(props.score))
</script>

<template>
  <div class="eval-bar">
    <div
      class="eval-fill"
      :style="{ height: height + '%' }"
    ></div>

    <!-- optional text -->
    <div class="eval-text">
      {{ score > 0 ? "+" : "" }}{{ score.toFixed(1) }}
    </div>
  </div>
</template>

<style scoped>
.eval-bar {
  width: 20px;
  height: 600px;
  background: black;
  border-radius: 6px;
  overflow: hidden;
  position: relative;
}

/* white advantage */
.eval-fill {
  position: absolute;
  bottom: 0;
  width: 100%;
  background: white;
  transition: height 0.3s ease;
}

/* score label */
.eval-text {
  position: absolute;
  top: 5px;
  left: 25px;
  font-size: 12px;
  color: white;
}
</style>