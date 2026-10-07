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
    max-width="470"
    width="calc(100% - 32px)"
  >
    <v-card
      class="game-end-card"
      rounded="xl"
      elevation="0"
    >

      <!-- HEADER -->
      <div class="game-end-header">

        <div class="header-pattern pattern-one"></div>
        <div class="header-pattern pattern-two"></div>

        <div class="header-content">

          <div class="brand-mark">
            <v-icon
              size="18"
              color="white"
            >
              mdi-chess-queen
            </v-icon>
          </div>

          <div class="game-end-icon">
            <v-icon
              size="39"
              color="white"
            >
              {{ resultIcon }}
            </v-icon>
          </div>

          <div class="header-caption">
            MATCH COMPLETE
          </div>

        </div>

        <v-btn
          icon="mdi-close"
          variant="text"
          size="small"
          class="close-button"
          aria-label="Close"
          @click="dialog = false"
        />

      </div>

      <!-- CONTENT -->
      <v-card-text class="game-end-content">

        <div class="game-over-label">
          <span></span>
          GAME OVER
          <span></span>
        </div>

        <h2 class="game-end-title">
          {{ resultTitle }}
        </h2>

        <div class="result-panel">

          <div class="result-panel-icon">
            <v-icon
              size="23"
              color="#f28c28"
            >
              {{ reasonIcon }}
            </v-icon>
          </div>

          <div class="result-panel-text">

            <span class="result-label">
              RESULT
            </span>

            <strong>
              {{ resultSubtitle }}
            </strong>

          </div>

        </div>

        <div
          v-if="gameResult.result"
          class="result-badge"
        >
          <span>FINAL RESULT</span>

          <strong>
            {{ gameResult.result }}
          </strong>
        </div>

        <v-btn
          color="#f28c28"
          rounded="lg"
          block
          size="large"
          class="continue-button"
          elevation="0"
          @click="dialog = false"
        >
          <v-icon
            start
            size="20"
          >
            mdi-chess-queen
          </v-icon>

          Continue Reviewing

          <v-icon
            end
            size="19"
          >
            mdi-arrow-right
          </v-icon>
        </v-btn>

      </v-card-text>

      <!-- FOOTER -->
      <div class="game-end-footer">

        <v-icon size="15">
          mdi-chess-pawn
        </v-icon>

        <span>
          Keep analyzing. Keep improving.
        </span>

        <v-icon size="15">
          mdi-chess-pawn
        </v-icon>

      </div>

    </v-card>
  </v-dialog>
</template>

<style scoped>
.game-end-card {
  position: relative;
  overflow: hidden;
  border: 1px solid #e7e7e7;
  background: #ffffff;
  box-shadow:
    0 30px 80px rgba(0, 0, 0, 0.28);
}

/* =========================================
   HEADER
========================================= */

.game-end-header {
  position: relative;
  min-height: 215px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background:
    radial-gradient(
      circle at 50% 70%,
      rgba(242, 140, 40, 0.22),
      transparent 35%
    ),
    linear-gradient(
      145deg,
      #080808 0%,
      #151515 55%,
      #222222 100%
    );
}

.header-content {
  position: relative;
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.brand-mark {
  position: absolute;
  top: -55px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border: 1px solid rgba(242, 140, 40, 0.45);
  border-radius: 50%;
  background: rgba(242, 140, 40, 0.14);
}

.game-end-icon {
  width: 84px;
  height: 84px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(242, 140, 40, 0.7);
  border-radius: 50%;
  background:
    linear-gradient(
      145deg,
      #f28c28,
      #d96f0b
    );
  box-shadow:
    0 0 0 8px rgba(242, 140, 40, 0.08),
    0 12px 35px rgba(242, 140, 40, 0.25);
}

.header-caption {
  margin-top: 15px;
  color: rgba(255, 255, 255, 0.65);
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 2.5px;
}

.close-button {
  position: absolute;
  z-index: 5;
  top: 10px;
  right: 10px;
  color: rgba(255, 255, 255, 0.8);
}

.close-button:hover {
  color: #f28c28;
}

/* =========================================
   CHESS PATTERN
========================================= */

.header-pattern {
  position: absolute;
  width: 230px;
  height: 230px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  opacity: 0.06;
  transform: rotate(14deg);
}

.header-pattern::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    conic-gradient(
      from 90deg,
      #ffffff 25%,
      transparent 0 50%,
      #ffffff 0 75%,
      transparent 0
    );
  background-size: 50% 50%;
}

.pattern-one {
  top: -100px;
  left: -55px;
}

.pattern-two {
  right: -55px;
  bottom: -100px;
  transform: rotate(-14deg);
}

/* =========================================
   CONTENT
========================================= */

.game-end-content {
  padding: 28px 30px 30px !important;
  text-align: center;
}

.game-over-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  color: #f28c28;
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 2.2px;
}

.game-over-label span {
  width: 25px;
  height: 2px;
  border-radius: 5px;
  background: #f28c28;
}

.game-end-title {
  margin: 10px 0 20px;
  color: #111111;
  font-size: 25px;
  line-height: 1.25;
  font-weight: 850;
  letter-spacing: -0.4px;
}

/* =========================================
   RESULT PANEL
========================================= */

.result-panel {
  display: flex;
  align-items: center;
  gap: 13px;
  padding: 14px 16px;
  border: 1px solid #ececec;
  border-left: 4px solid #f28c28;
  border-radius: 12px;
  background:
    linear-gradient(
      100deg,
      #fffaf5,
      #ffffff
    );
  text-align: left;
}

.result-panel-icon {
  flex: 0 0 45px;
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 11px;
  background: #fff1e3;
}

.result-panel-text {
  min-width: 0;
}

.result-label {
  display: block;
  margin-bottom: 3px;
  color: #9a9a9a;
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 1.3px;
}

.result-panel-text strong {
  display: block;
  overflow: hidden;
  color: #222222;
  font-size: 14px;
  font-weight: 750;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* =========================================
   RESULT BADGE
========================================= */

.result-badge {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  margin-top: 16px;
  padding: 7px 12px;
  border: 1px solid #e7e7e7;
  border-radius: 8px;
  background: #f7f7f7;
}

.result-badge span {
  color: #999999;
  font-size: 8px;
  font-weight: 800;
  letter-spacing: 1px;
}

.result-badge strong {
  color: #222222;
  font-size: 13px;
  font-weight: 900;
}

/* =========================================
   BUTTON
========================================= */

.continue-button {
  min-height: 48px;
  margin-top: 23px;
  color: #ffffff !important;
  font-weight: 800;
  letter-spacing: 0.1px;
  background:
    linear-gradient(
      135deg,
      #f28c28,
      #df7413
    ) !important;
  box-shadow:
    0 9px 22px rgba(242, 140, 40, 0.25) !important;
}

.continue-button:hover {
  background:
    linear-gradient(
      135deg,
      #ff9d3f,
      #e47b18
    ) !important;
}

/* =========================================
   FOOTER
========================================= */

.game-end-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  border-top: 1px solid #eeeeee;
  background: #fafafa;
  color: #a0a0a0;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.4px;
}

.game-end-footer .v-icon {
  color: #f28c28;
}

/* =========================================
   MOBILE
========================================= */

@media (max-width: 500px) {
  .game-end-header {
    min-height: 195px;
  }

  .game-end-icon {
    width: 75px;
    height: 75px;
  }

  .game-end-content {
    padding: 24px 20px 25px !important;
  }

  .game-end-title {
    font-size: 22px;
  }

  .result-panel {
    padding: 12px;
  }

  .result-panel-text strong {
    font-size: 13px;
  }
}
</style>