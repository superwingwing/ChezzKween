<script setup>
    defineProps({
      quality: {
        type: String,
        default: ""
      }
    })
</script>

<template>
    <div
      v-if="quality"
      class="quality-badge"
      :class="quality"
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
      width: 42px;
      height: 42px;

      border-radius: 50%;

      display: flex;
      align-items: center;
      justify-content: center;

      font-size: 20px;
      font-weight: bold;

      bottom: 8px;
      right: 8px;

      z-index: 999;
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