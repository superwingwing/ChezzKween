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
      <div class="chess-background"></div>

      <!-- Floating Chess Pieces -->
      <v-icon class="floating-piece piece-1" icon="mdi-chess-pawn" />
      <v-icon class="floating-piece piece-2" icon="mdi-chess-knight" />
      <v-icon class="floating-piece piece-3" icon="mdi-chess-bishop" />
      <v-icon class="floating-piece piece-4" icon="mdi-chess-rook" />
      <v-icon class="floating-piece piece-5" icon="mdi-chess-pawn" />

      <v-container
        fluid
        class="error-container"
      >
        <div class="error-content">

          <!-- Animated Queen -->
          <div class="queen-area">
            <div class="queen-glow"></div>

            <v-icon
              icon="mdi-chess-queen"
              class="main-queen"
            />
          </div>

          <!-- 404 -->
          <div class="error-number">
            <span>4</span>
            <span class="zero">0</span>
            <span>4</span>
          </div>

          <!-- Title -->
          <h1 class="error-title">
            PAGE NOT FOUND
          </h1>

          <p class="error-description">
            Looks like this move wasn't found on the board.
            The page you're looking for may have been moved or doesn't exist.
          </p>

          <!-- Chess line -->
          <div class="chess-line">
            <div></div>

            <v-icon icon="mdi-chess-pawn" />
            <v-icon icon="mdi-chess-knight" />
            <v-icon icon="mdi-chess-bishop" />
            <v-icon icon="mdi-chess-rook" />

            <div></div>
          </div>

          <!-- Buttons -->
          <div class="actions">

            <v-btn
              color="light-blue-darken-4"
              size="large"
              rounded="lg"
              prepend-icon="mdi-home-outline"
              class="home-btn"
              @click="goHome"
            >
              Back to Home
            </v-btn>

            <v-btn
              color="light-blue-darken-4"
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

          <!-- Branding -->
          <div class="branding">
            <v-icon
              icon="mdi-chess-queen"
              size="18"
              color="light-blue-darken-4"
            />

            <span>ChessKween</span>
          </div>

        </div>
      </v-container>
    </v-main>
  </v-app>
</template>

<style scoped>

/* =========================================
   FULL SCREEN
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
}


/* =========================================
   BACKGROUND
   ========================================= */

.chess-background {
  position: absolute;
  inset: 0;

  opacity: 0.035;

  background-image:
    linear-gradient(
      45deg,
      #01579b 25%,
      transparent 25%
    ),
    linear-gradient(
      -45deg,
      #01579b 25%,
      transparent 25%
    ),
    linear-gradient(
      45deg,
      transparent 75%,
      #01579b 75%
    ),
    linear-gradient(
      -45deg,
      transparent 75%,
      #01579b 75%
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
   CONTENT
   ========================================= */

.error-container {
  position: relative;
  z-index: 5;

  height: 100%;
  min-height: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 20px;
}

.error-content {
  width: 100%;
  max-width: 850px;

  text-align: center;
}


/* =========================================
   QUEEN
   ========================================= */

.queen-area {
  position: relative;

  width: 90px;
  height: 90px;

  margin: 0 auto 5px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.main-queen {
  position: relative;
  z-index: 2;

  font-size: 76px;

  color: #01579b;

  animation:
    queen-float 3s ease-in-out infinite,
    queen-glow 2.5s ease-in-out infinite alternate;
}

.queen-glow {
  position: absolute;

  width: 70px;
  height: 70px;

  border-radius: 50%;

  background: rgba(1, 87, 155, 0.16);

  filter: blur(25px);

  animation: glow-pulse 2.5s ease-in-out infinite;
}


/* =========================================
   404
   ========================================= */

.error-number {
  display: flex;

  justify-content: center;
  align-items: center;

  gap: clamp(5px, 1vw, 14px);

  font-size: clamp(100px, 20vw, 230px);

  line-height: 0.78;

  font-weight: 900;

  letter-spacing: clamp(-8px, -1vw, -14px);

  color: #01579b;

  user-select: none;
}

.error-number span {
  display: inline-block;

  animation: number-float 3.5s ease-in-out infinite;
}

.error-number span:nth-child(1) {
  animation-delay: 0s;
}

.error-number span:nth-child(2) {
  animation-delay: 0.2s;
}

.error-number span:nth-child(3) {
  animation-delay: 0.4s;
}


/* =========================================
   ZERO
   ========================================= */

.zero {
  position: relative;

  width: clamp(90px, 15vw, 180px);
  height: clamp(90px, 15vw, 180px);

  display: flex;
  align-items: center;
  justify-content: center;

  border: clamp(8px, 1.2vw, 14px) solid #01579b;

  border-radius: 50%;

  font-size: 0;

  animation:
    zero-rotate 8s linear infinite,
    zero-pulse 2.5s ease-in-out infinite;
}

.zero::after {
  content: "♛";

  position: absolute;

  font-size: clamp(35px, 6vw, 75px);

  color: #01579b;

  animation: queen-inside 3s ease-in-out infinite;
}


/* =========================================
   TITLE
   ========================================= */

.error-title {
  margin: 28px 0 0;

  font-size: clamp(22px, 3vw, 36px);

  font-weight: 800;

  letter-spacing: 4px;

  color: #263238;
}


/* =========================================
   DESCRIPTION
   ========================================= */

.error-description {
  max-width: 580px;

  margin: 12px auto 0;

  color: #607d8b;

  font-size: clamp(13px, 1.6vw, 16px);

  line-height: 1.6;
}


/* =========================================
   CHESS LINE
   ========================================= */

.chess-line {
  display: flex;

  justify-content: center;
  align-items: center;

  gap: 14px;

  margin: 20px auto;

  color: #01579b;
}

.chess-line div {
  width: clamp(35px, 8vw, 100px);
  height: 1px;

  background: rgba(1, 87, 155, 0.25);
}

.chess-line .v-icon {
  font-size: 21px;

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

  justify-content: center;
  align-items: center;

  gap: 12px;

  margin-top: 20px;
}

.home-btn {
  min-width: 170px;

  color: #ffffff;

  font-weight: 600;

  box-shadow:
    0 8px 22px rgba(1, 87, 155, 0.22);
}

.back-btn {
  min-width: 135px;

  font-weight: 600;
}


/* =========================================
   BRANDING
   ========================================= */

.branding {
  display: flex;

  justify-content: center;
  align-items: center;

  gap: 7px;

  margin-top: 25px;

  color: #78909c;

  font-size: 13px;

  font-weight: 600;
}


/* =========================================
   FLOATING CHESS PIECES
   ========================================= */

.floating-piece {
  position: absolute;

  z-index: 2;

  color: #01579b;

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

@keyframes queen-float {
  0%,
  100% {
    transform: translateY(0) rotate(0deg);
  }

  50% {
    transform: translateY(-10px) rotate(3deg);
  }
}

@keyframes queen-glow {
  from {
    filter: drop-shadow(0 0 5px rgba(1, 87, 155, 0.2));
  }

  to {
    filter: drop-shadow(0 0 20px rgba(1, 87, 155, 0.5));
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
    transform: translateY(-7px);
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
    box-shadow: 0 0 0 rgba(1, 87, 155, 0);
  }

  50% {
    box-shadow: 0 0 35px rgba(1, 87, 155, 0.15);
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
    padding: 12px;
  }

  .queen-area {
    width: 65px;
    height: 65px;
  }

  .main-queen {
    font-size: 55px;
  }

  .queen-glow {
    width: 50px;
    height: 50px;
  }

  .error-title {
    margin-top: 22px;

    letter-spacing: 2px;
  }

  .error-description {
    max-width: 90%;
  }

  .chess-line {
    gap: 8px;

    margin: 16px auto;
  }

  .chess-line .v-icon {
    font-size: 18px;
  }

  .actions {
    margin-top: 16px;

    gap: 8px;
  }

  .home-btn,
  .back-btn {
    min-width: 135px;
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

  .queen-area {
    transform: scale(0.75);
    margin-bottom: -5px;
  }

  .error-title {
    margin-top: 15px;
  }

  .error-description {
    margin-top: 8px;
  }

  .chess-line {
    margin: 12px auto;
  }

  .actions {
    margin-top: 12px;
  }

  .branding {
    margin-top: 12px;
  }
}


/* =========================================
   REDUCE MOTION
   ========================================= */

@media (prefers-reduced-motion: reduce) {

  .main-queen,
  .queen-glow,
  .error-number span,
  .zero,
  .zero::after,
  .chess-line .v-icon,
  .floating-piece {
    animation: none;
  }
}

</style>
