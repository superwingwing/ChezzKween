<script setup>
import { computed } from "vue"

const props = defineProps({
  quality: String,
  square: String
})

const styleObject = computed(() => {
  if (!props.square) return {}

  const file = props.square.charCodeAt(0) - 97
  const rank = parseInt(props.square[1])

  const squareSize = 75

  return {
    left: `${file * squareSize + 4}px`,
    top: `${(8 - rank) * squareSize + 4}px`
  }
})
</script>

<template>
  <div
    v-if="quality && square"
    class="quality-badge"
    :class="quality"
    :style="styleObject"
  >
    <span v-if="quality === 'best'">⭐</span>
    <span v-else-if="quality === 'good'">👍</span>
    <span v-else-if="quality === 'inaccuracy'">⚠️</span>
    <span v-else-if="quality === 'mistake'">❌</span>
    <span v-else-if="quality === 'blunder'">💀</span>
  </div>
</template>

<style scoped>
.quality-badge {
  position: absolute;
  width: 32px;
  height: 32px;

  border-radius: 50%;

  display: flex;
  align-items: center;
  justify-content: center;

  z-index: 9999;

  font-size: 18px;
  pointer-events: none;
}

.best {
  background: #4caf50;
}

.good {
  background: #8bc34a;
}

.inaccuracy {
  background: #ff9800;
}

.mistake {
  background: #f44336;
}

.blunder {
  background: #9c27b0;
}
</style>