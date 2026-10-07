<script setup>
import { useRouter } from "vue-router"

const router = useRouter()

function goHome() {
  router.push({ name: "dashboard" })
}

function goBack() {
  router.back()
}
</script>

<template>
  <v-app class="not-found-page">
    <v-main class="main-content">

      <!-- BACKGROUND -->
      <div class="chess-background"></div>

      <!-- FLOATING CHESS PIECES -->
      <v-icon
        class="floating-piece piece-1"
        icon="mdi-chess-pawn"
      />

      <v-icon
        class="floating-piece piece-2"
        icon="mdi-chess-knight"
      />

      <v-icon
        class="floating-piece piece-3"
        icon="mdi-chess-bishop"
      />

      <v-icon
        class="floating-piece piece-4"
        icon="mdi-chess-rook"
      />

      <v-icon
        class="floating-piece piece-5"
        icon="mdi-chess-pawn"
      />

      <!-- MAIN CONTENT -->
      <v-container
        fluid
        class="error-container"
      >
        <v-card
          class="error-card"
          rounded="xl"
          elevation="0"
        >

          <!-- QUEEN -->
          <div class="queen-area">
            <div class="queen-glow"></div>

            <v-avatar
              class="queen-avatar"
              size="86"
            >
              <v-icon
                icon="mdi-chess-queen"
                size="52"
              />
            </v-avatar>
          </div>

          <!-- 404 -->
          <div class="error-number">
            <span>4</span>

            <span class="zero">
              <span class="zero-queen">♛</span>
            </span>

            <span>4</span>
          </div>

          <!-- TITLE -->
          <h1 class="error-title">
            PAGE NOT FOUND
          </h1>

          <!-- DESCRIPTION -->
          <p class="error-description">
            Looks like this move wasn't found on the board.
            The page you're looking for may have been moved
            or doesn't exist.
          </p>

          <!-- CHESS DIVIDER -->
          <div class="chess-line">
            <span></span>

            <v-icon icon="mdi-chess-pawn" />
            <v-icon icon="mdi-chess-knight" />
            <v-icon icon="mdi-chess-bishop" />
            <v-icon icon="mdi-chess-rook" />

            <span></span>
          </div>

          <!-- BUTTONS -->
          <div class="actions">

            <v-btn
              color="orange-darken-1"
              size="large"
              rounded="lg"
              prepend-icon="mdi-home-outline"
              class="home-btn"
              elevation="4"
              @click="goHome"
            >
              Back to Home
            </v-btn>

            <v-btn
              color="orange-darken-1"
              variant="outlined"
              size="large"
              rounded="lg"
              prepend-icon="mdi-arrow-left"
              class="back-btn"
              @click="goBack"
            >
              Go Back
            </v-btn>

          </div>

          <!-- BRANDING -->
          <div class="branding">
            <v-avatar
              size="30"
              color="#fff3e6"
              rounded="lg"
            >
              <v-icon
                icon="mdi-chess-queen"
                size="17"
                color="orange-darken-2"
              />
            </v-avatar>

            <span class="branding-text">
              Chess<span>Kween</span>
            </span>
          </div>

        </v-card>
      </v-container>

    </v-main>
  </v-app>
</template>

<style scoped>

/* =========================================
   PAGE
   ========================================= */

.not-found-page {
  width: 100%;
  height: 100dvh;
  overflow: hidden;

  background: #ffffff;
}

.main-content {
  position: relative;

  width: 100%;
  height: 100dvh;

  overflow: hidden;

  background:
    radial-gradient(
      circle at 50% 35%,
      rgba(242, 140, 40, 0.10),
      transparent 38%
    ),
    linear-gradient(
      180deg,
      #ffffff 0%,
      #fafafa 55%,
      #f5f5f5 100%
    );
}


/* =========================================
   CHESS BOARD BACKGROUND
   ========================================= */

.chess-background {
  position: absolute;
  inset: 0;

  opacity: 0.035;

  background-image:
    linear-gradient(
      45deg,
      #f28c28 25%,
      transparent 25%
    ),
    linear-gradient(
      -45deg,
      #f28c28 25%,
      transparent 25%
    ),
    linear-gradient(
      45deg,
      transparent 75%,
      #f28c28 75%
    ),
    linear-gradient(
      -45deg,
      transparent 75%,
      #f28c28 75%
    );

  background-size: 80px 80px;

  background-position:
    0 0,
    0 40px,
    40px -40px,
    -40px 0;

  pointer-events: none;
}


/* =========================================
   CONTAINER
   ========================================= */

.error-container {
  position: relative;

  z-index: 5;

  height: 100%;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 24px;
}


/* =========================================
   ERROR CARD
   ========================================= */

.error-card {
  width: 100%;
  max-width: 760px;

  padding: 38px 42px 28px;

  text-align: center;

  background:
    linear-gradient(
      145deg,
      #ffffff 0%,
      #fafafa 100%
    );

  border: 1px solid #e6e6e6;

  box-shadow:
    0 24px 60px rgba(0, 0, 0, 0.08),
    0 6px 18px rgba(242, 140, 40, 0.06);

  animation: card-enter 0.6s ease-out;
}


/* =========================================
   QUEEN
   ========================================= */

.queen-area {
  position: relative;

  width: 86px;
  height: 86px;

  margin: 0 auto 8px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.queen-avatar {
  position: relative;

  z-index: 2;

  background:
    linear-gradient(
      135deg,
      #111111,
      #252525
    );

  border: 2px solid #f28c28;

  color: #f28c28;

  box-shadow:
    0 10px 30px rgba(242, 140, 40, 0.18);

  animation: queen-float 3s ease-in-out infinite;
}

.queen-glow {
  position: absolute;

  width: 70px;
  height: 70px;

  border-radius: 50%;

  background: rgba(242, 140, 40, 0.18);

  filter: blur(25px);

  animation: glow-pulse 2.5s ease-in-out infinite;
}


/* =========================================
   404
   ========================================= */

.error-number {
  display: flex;

  align-items: center;
  justify-content: center;

  gap: 10px;

  margin-top: 2px;

  font-size: clamp(100px, 18vw, 190px);

  line-height: 0.8;

  font-weight: 900;

  letter-spacing: -10px;

  color: #111111;

  user-select: none;
}

.error-number > span {
  display: inline-block;

  animation: number-float 3.5s ease-in-out infinite;
}

.error-number > span:first-child {
  animation-delay: 0s;
}

.error-number > span:last-child {
  animation-delay: 0.4s;
}


/* =========================================
   ZERO
   ========================================= */

.zero {
  position: relative;

  width: clamp(85px, 14vw, 160px);
  height: clamp(85px, 14vw, 160px);

  display: flex;
  align-items: center;
  justify-content: center;

  border:
    clamp(8px, 1vw, 13px)
    solid
    #f28c28;

  border-radius: 50%;

  font-size: 0;

  animation:
    zero-rotate 8s linear infinite,
    zero-pulse 2.5s ease-in-out infinite;
}

.zero-queen {
  position: absolute;

  font-size: clamp(35px, 6vw, 70px);

  color: #f28c28;

  animation: queen-inside 3s ease-in-out infinite;
}


/* =========================================
   TITLE
   ========================================= */

.error-title {
  margin: 24px 0 0;

  color: #111111;

  font-size: clamp(24px, 3vw, 34px);

  font-weight: 900;

  letter-spacing: 2px;
}


/* =========================================
   DESCRIPTION
   ========================================= */

.error-description {
  max-width: 560px;

  margin: 10px auto 0;

  color: #666666;

  font-size: 14px;

  line-height: 1.7;
}


/* =========================================
   CHESS LINE
   ========================================= */

.chess-line {
  display: flex;

  align-items: center;
  justify-content: center;

  gap: 13px;

  margin: 22px auto;

  color: #f28c28;
}

.chess-line span {
  width: clamp(35px, 8vw, 90px);

  height: 1px;

  background: #e0e0e0;
}

.chess-line .v-icon {
  font-size: 20px;

  animation: piece-bounce 2s ease-in-out infinite;
}

.chess-line .v-icon:nth-child(3) {
  animation-delay: 0.15s;
}

.chess-line .v-icon:nth-child(4) {
  animation-delay: 0.3s;
}

.chess-line .v-icon:nth-child(5) {
  animation-delay: 0.45s;
}


/* =========================================
   BUTTONS
   ========================================= */

.actions {
  display: flex;

  align-items: center;
  justify-content: center;

  gap: 12px;

  margin-top: 22px;
}

.home-btn {
  min-width: 170px;

  color: #ffffff !important;

  font-weight: 700;

  box-shadow:
    0 8px 24px rgba(242, 140, 40, 0.25);
}

.back-btn {
  min-width: 135px;

  font-weight: 700;

  background: #ffffff;
}


/* =========================================
   BRANDING
   ========================================= */

.branding {
  display: flex;

  align-items: center;
  justify-content: center;

  gap: 8px;

  margin-top: 24px;

  color: #555555;

  font-size: 13px;

  font-weight: 800;
}

.branding-text span {
  color: #f28c28;
}


/* =========================================
   FLOATING PIECES
   ========================================= */

.floating-piece {
  position: absolute;

  z-index: 2;

  color: #f28c28;

  opacity: 0.08;

  pointer-events: none;
}

.piece-1 {
  top: 12%;
  left: 8%;

  font-size: 50px;

  animation: float-1 7s ease-in-out infinite;
}

.piece-2 {
  top: 20%;
  right: 10%;

  font-size: 60px;

  animation: float-2 8s ease-in-out infinite;
}

.piece-3 {
  bottom: 15%;
  left: 12%;

  font-size: 45px;

  animation: float-3 9s ease-in-out infinite;
}

.piece-4 {
  bottom: 18%;
  right: 12%;

  font-size: 55px;

  animation: float-4 7s ease-in-out infinite;
}

.piece-5 {
  top: 48%;
  left: 3%;

  font-size: 35px;

  animation: float-2 6s ease-in-out infinite;
}


/* =========================================
   ANIMATIONS
   ========================================= */

@keyframes card-enter {
  from {
    opacity: 0;
    transform: translateY(18px) scale(0.98);
  }

  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes queen-float {
  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-8px);
  }
}

@keyframes glow-pulse {
  0%,
  100% {
    transform: scale(0.8);
    opacity: 0.4;
  }

  50% {
    transform: scale(1.2);
    opacity: 0.8;
  }
}

@keyframes number-float {
  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-6px);
  }
}

@keyframes zero-rotate {
  0%,
  100% {
    transform: rotate(0deg);
  }

  50% {
    transform: rotate(3deg);
  }
}

@keyframes zero-pulse {
  0%,
  100% {
    box-shadow: 0 0 0 rgba(242, 140, 40, 0);
  }

  50% {
    box-shadow:
      0 0 35px rgba(242, 140, 40, 0.18);
  }
}

@keyframes queen-inside {
  0%,
  100% {
    transform: translateY(0) scale(1);
  }

  50% {
    transform: translateY(-5px) scale(1.08);
  }
}

@keyframes piece-bounce {
  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-5px);
  }
}

@keyframes float-1 {
  0%,
  100% {
    transform: translate(0, 0) rotate(-10deg);
  }

  50% {
    transform: translate(20px, -25px) rotate(10deg);
  }
}

@keyframes float-2 {
  0%,
  100% {
    transform: translate(0, 0) rotate(5deg);
  }

  50% {
    transform: translate(-20px, 25px) rotate(-10deg);
  }
}

@keyframes float-3 {
  0%,
  100% {
    transform: translate(0, 0);
  }

  50% {
    transform: translate(25px, -20px);
  }
}

@keyframes float-4 {
  0%,
  100% {
    transform: translate(0, 0) rotate(5deg);
  }

  50% {
    transform: translate(-25px, -15px) rotate(-5deg);
  }
}


/* =========================================
   MOBILE
   ========================================= */

@media (max-width: 600px) {

  .error-container {
    padding: 14px;
  }

  .error-card {
    padding: 28px 18px 22px;
  }

  .queen-area {
    width: 70px;
    height: 70px;
  }

  .queen-avatar {
    width: 68px !important;
    height: 68px !important;
  }

  .queen-avatar .v-icon {
    font-size: 42px !important;
  }

  .error-title {
    margin-top: 20px;

    letter-spacing: 1px;
  }

  .error-description {
    max-width: 92%;
  }

  .chess-line {
    gap: 8px;

    margin: 17px auto;
  }

  .chess-line .v-icon {
    font-size: 17px;
  }

  .actions {
    flex-direction: column;

    width: 100%;

    gap: 9px;
  }

  .home-btn,
  .back-btn {
    width: 100%;

    min-width: 0;
  }

  .branding {
    margin-top: 18px;
  }

  .floating-piece {
    display: none;
  }
}


/* =========================================
   SMALL PHONES
   ========================================= */

@media (max-height: 650px) {

  .error-card {
    padding-top: 20px;
    padding-bottom: 18px;
  }

  .queen-area {
    transform: scale(0.75);

    margin-bottom: -5px;
  }

  .error-title {
    margin-top: 12px;
  }

  .error-description {
    margin-top: 7px;
  }

  .chess-line {
    margin: 11px auto;
  }

  .actions {
    margin-top: 11px;
  }

  .branding {
    margin-top: 12px;
  }
}


/* =========================================
   REDUCE MOTION
   ========================================= */

@media (prefers-reduced-motion: reduce) {

  .error-card,
  .queen-avatar,
  .queen-glow,
  .error-number > span,
  .zero,
  .zero-queen,
  .chess-line .v-icon,
  .floating-piece {
    animation: none;
  }
}

</style>