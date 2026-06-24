<script setup>
defineProps({
  quality: {
    type: String,
    default: ""
  }
})
</script>

<template>
  <div class="quality-icon">
    <span v-if="quality === 'best'">⭐ Best</span>
    <span v-else-if="quality === 'good'">👍 Good</span>
    <span v-else-if="quality === 'inaccuracy'">⚠️ Inaccuracy</span>
    <span v-else-if="quality === 'mistake'">❌ Mistake</span>
    <span v-else-if="quality === 'blunder'">💀 Blunder</span>
  </div>
</template>

<style scoped>
.quality-icon {
  margin-top: 10px;
  font-weight: bold;
  font-size: 16px;
}
</style>