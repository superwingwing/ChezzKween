<script setup>
import { computed } from "vue"
import { Chess } from "chess.js"

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },

  game: {
    type: Object,
    default: null
  }
})

const emit = defineEmits([
  "update:modelValue"
])

const dialog = computed({
  get: () => props.modelValue,
  set: value => emit("update:modelValue", value)
})

const gameResult = computed(() => {
  if (!props.game) {
    return {
      winner: "",
      reason: "Game over",
      result: ""
    }
  }

  const chess = new Chess()

  try {
    if (props.game.pgn) {
      chess.loadPgn(props.game.pgn)
    }
  } catch (error) {
    console.error(
      "Failed to load PGN for game result:",
      error
    )
  }

  const whiteName =
    props.game.white_name ||
    props.game.white ||
    "White"

  const blackName =
    props.game.black_name ||
    props.game.black ||
    "Black"

  const pgnHeader =
    chess.header?.() || {}

  const result =
    props.game.result ||
    pgnHeader.Result ||
    ""

  const termination =
    props.game.termination ||
    pgnHeader.Termination ||
    ""

  let winner = ""
  let reason = ""

  /*
   * CHECKMATE
   *
   * chess.turn() is the player whose turn it is.
   * If White is to move and the position is checkmate,
   * Black delivered checkmate.
   */
  if (chess.isCheckmate()) {
    winner =
      chess.turn() === "w"
        ? blackName
        : whiteName

    reason = "checkmate"
  }

  /*
   * RESULT
   */
  else if (result === "1-0") {
    winner = whiteName
  }

  else if (result === "0-1") {
    winner = blackName
  }

  /*
   * DRAW
   */
  else if (result === "1/2-1/2") {
    reason = "draw"
  }

  /*
   * TERMINATION
   */
  if (winner) {
    const terminationText =
      termination.toLowerCase()

    if (
      terminationText.includes("resignation")
    ) {
      reason = "resignation"
    }

    else if (
      terminationText.includes("timeout")
    ) {
      reason = "timeout"
    }

    else if (
      terminationText.includes("time forfeit")
    ) {
      reason = "time forfeit"
    }

    else if (
      terminationText.includes("abandoned")
    ) {
      reason = "abandoned"
    }

    /*
     * If checkmate was detected from the
     * actual board, keep checkmate as the
     * reason even if the PGN termination
     * header is missing.
     */
    else if (!reason) {
      reason = "win"
    }
  }

  /*
   * DRAW REASONS
   */
  if (!winner) {
    if (chess.isStalemate()) {
      reason = "stalemate"
    }

    else if (chess.isThreefoldRepetition()) {
      reason = "threefold repetition"
    }

    else if (chess.isInsufficientMaterial()) {
      reason = "insufficient material"
    }

    else if (
      termination
        .toLowerCase()
        .includes("agreement")
    ) {
      reason = "draw by agreement"
    }

    else if (!reason) {
      reason = "draw"
    }
  }

  return {
    winner,
    reason,
    result
  }
})

const isWinner = computed(() =>
  Boolean(gameResult.value.winner)
)

const resultIcon = computed(() => {
  if (!isWinner.value) {
    return "mdi-handshake"
  }

  if (
    gameResult.value.reason ===
    "checkmate"
  ) {
    return "mdi-chess-king"
  }

  if (
    gameResult.value.reason ===
    "resignation"
  ) {
    return "mdi-flag-checkered"
  }

  if (
    gameResult.value.reason ===
    "timeout"
  ) {
    return "mdi-clock-alert"
  }

  return "mdi-trophy"
})

const resultTitle = computed(() => {
  if (isWinner.value) {
    return `${gameResult.value.winner} won the game`
  }

  return "Game Drawn"
})

const resultSubtitle = computed(() => {
  if (isWinner.value) {
    return `by ${gameResult.value.reason}`
  }

  return gameResult.value.reason
})
</script>

<template>
  <v-dialog
    v-model="dialog"
    max-width="460"
    width="calc(100% - 32px)"
  >
    <v-card
      class="game-end-card"
      rounded="xl"
    >

      <!-- HEADER -->
      <div class="game-end-header">

        <div class="game-end-icon">
          <v-icon
            size="38"
            color="white"
          >
            {{ resultIcon }}
          </v-icon>
        </div>

        <v-btn
          icon="mdi-close"
          variant="text"
          size="small"
          class="close-button"
          @click="dialog = false"
        />

      </div>

      <!-- CONTENT -->
      <v-card-text class="game-end-content">

        <div class="game-over-label">
          GAME OVER
        </div>

        <h2 class="game-end-title">
          {{ resultTitle }}
        </h2>

        <div class="game-end-reason">
          <v-icon
            size="19"
            color="light-blue-darken-3"
          >
            {{
              gameResult.reason === "checkmate"
                ? "mdi-chess-king"
                : gameResult.reason === "resignation"
                  ? "mdi-flag-checkered"
                  : "mdi-information-outline"
            }}
          </v-icon>

          <span>
            {{ resultSubtitle }}
          </span>
        </div>

        <div
          v-if="gameResult.result"
          class="result-badge"
        >
          {{ gameResult.result }}
        </div>

        <v-btn
          color="light-blue-darken-3"
          rounded="lg"
          block
          size="large"
          class="continue-button"
          @click="dialog = false"
        >
          Continue Reviewing
        </v-btn>

      </v-card-text>

    </v-card>
  </v-dialog>
</template>

<style scoped>
.game-end-card {
  overflow: hidden;
  border: 1px solid #dceafa;
  background: #ffffff;
  box-shadow:
    0 25px 70px rgba(15, 55, 95, 0.25);
}

.game-end-header {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 20px 27px;
  background:
    linear-gradient(
      135deg,
      #0d47a1 0%,
      #1976d2 100%
    );
}

.game-end-icon {
  width: 76px;
  height: 76px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4px solid rgba(255, 255, 255, 0.22);
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.13);
  box-shadow:
    0 10px 25px rgba(0, 40, 100, 0.2);
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  color: white;
}

.game-end-content {
  padding: 24px 28px 28px !important;
  text-align: center;
}

.game-over-label {
  color: #1976d2;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 2px;
}

.game-end-title {
  margin: 8px 0 13px;
  color: #102a56;
  font-size: 25px;
  line-height: 1.25;
  font-weight: 800;
}

.game-end-reason {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 8px 15px;
  border-radius: 20px;
  background: #eef7ff;
  color: #486581;
  font-size: 14px;
  font-weight: 600;
}

.result-badge {
  width: fit-content;
  min-width: 50px;
  margin: 17px auto 0;
  padding: 6px 13px;
  border-radius: 8px;
  background: #f2f6fa;
  color: #64788d;
  font-size: 13px;
  font-weight: 800;
}

.continue-button {
  margin-top: 22px;
  font-weight: 700;
}
</style>