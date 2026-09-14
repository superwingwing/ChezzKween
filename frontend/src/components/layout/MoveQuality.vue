<script setup>
import { computed, onMounted, onBeforeUnmount, ref, nextTick, watch } from "vue"

const props = defineProps({
  quality: String,
  square: String
})

const badgeStyle = ref({})

let resizeObserver = null

function updatePosition() {
  if (!props.square) {
    badgeStyle.value = {}
    return
  }

  const boardRow = document.querySelector(".board-row")
  if (!boardRow) return
  const chessboard = boardRow.querySelector(".board")
  if (!chessboard) return
  const boardRect = chessboard.getBoundingClientRect()
  const rowRect = boardRow.getBoundingClientRect()
  const boardSize = Math.min(
    boardRect.width,
    boardRect.height
  )

  if (!boardSize) return

  const squareSize = boardSize / 8
  const file =
    props.square.charCodeAt(0) - 97

  const rank =
    parseInt(props.square[1])

  /*
    Position badge at the UPPER-RIGHT
    corner of the target square.
  */

  const badgeSize =
    window.innerWidth <= 400
      ? 24
      : window.innerWidth <= 600
        ? 28
        : 32

  const offset = 3

  const left =
    (boardRect.left - rowRect.left) +
    ((file + 1) * squareSize) -
    badgeSize -
    offset

  const top =
    (boardRect.top - rowRect.top) +
    ((8 - rank) * squareSize) +
    offset

  badgeStyle.value = {
    left: `${left}px`,
    top: `${top}px`,
    width: `${badgeSize}px`,
    height: `${badgeSize}px`
  }
}

onMounted(async () => {
  await nextTick()

  updatePosition()

  window.addEventListener(
    "resize",
    updatePosition
  )

  const boardRow =
    document.querySelector(".board-row")

  if (boardRow) {
    resizeObserver =
      new ResizeObserver(() => {
        updatePosition()
      })

    resizeObserver.observe(boardRow)
  }
})

onBeforeUnmount(() => {
  window.removeEventListener(
    "resize",
    updatePosition
  )

  if (resizeObserver) {
    resizeObserver.disconnect()
  }
})

watch(
  () => props.square,
  async () => {
    await nextTick()
    updatePosition()
  }
)

watch(
  () => props.quality,
  async () => {
    await nextTick()
    updatePosition()
  }
)
</script>

<template>
  <div
    v-if="quality && square"
    class="quality-badge"
    :class="quality"
    :style="badgeStyle"
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

  box-sizing: border-box;
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

/* Smaller badge on phones */
@media (max-width: 600px) {
  .quality-badge {
    width: 28px;
    height: 28px;
    font-size: 15px;
  }
}

@media (max-width: 400px) {
  .quality-badge {
    width: 24px;
    height: 24px;
    font-size: 13px;
  }
}

</style>