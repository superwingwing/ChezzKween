<script setup>
import { ref } from "vue"

const features = [
  {
    icon: "mdi-crown",
    title: "Style Classification",
    description:
      "Identifies whether the player is primarily Aggressive or Positional based on patterns across their games.",
  },
  {
    icon: "mdi-chess-knight",
    title: "Game Analysis",
    description:
      "Analyzes an uploaded PGN using Stockfish to evaluate moves, positions, and important game moments.",
  },
  {
    icon: "mdi-chess-rook",
    title: "Style-Based Recommendations",
    description:
      "Selects playable moves that fit the player's style and provides human-like explanations.",
  },
]

const steps = [
  {
    number: "01",
    icon: "mdi-file-upload-outline",
    title: "Upload Your Games",
    description:
      "Upload your PGN games to provide ChessKween with the chess data needed for analysis and style classification.",
  },
  {
    number: "02",
    icon: "mdi-brain",
    title: "Discover Your Style",
    description:
      "ChessKween extracts meaningful playing patterns and classifies your dominant style as Aggressive or Positional.",
  },
  {
    number: "03",
    icon: "mdi-chess-king",
    title: "Analyze Your Game",
    description:
      "Stockfish evaluates your moves and identifies important moments, inaccuracies, mistakes, and blunders.",
  },
  {
    number: "04",
    icon: "mdi-lightbulb-on-outline",
    title: "Get Style-Aware Moves",
    description:
      "Playable engine candidates are filtered according to your playing style to provide more personalized recommendations.",
  },
]

const technologies = [
  {
    icon: "mdi-brain",
    title: "Machine Learning",
    text: "Random Forest classification",
  },
  {
    icon: "mdi-chess-queen",
    title: "Stockfish",
    text: "Chess engine evaluation",
  },
  {
    icon: "mdi-database",
    title: "Supabase",
    text: "Authentication and data storage",
  },
  {
    icon: "mdi-language-python",
    title: "Python",
    text: "Analysis and ML backend",
  },
]

const showDetails = ref(false)

const scrollToFeatures = () => {
  document.getElementById("about-features")?.scrollIntoView({
    behavior: "smooth",
    block: "start",
  })
}
</script>

<template>
  <v-container fluid class="about-page">

    <!-- =========================
         HERO
    ========================== -->
    <section class="hero-section">

      <div class="hero-pattern pattern-one"></div>
      <div class="hero-pattern pattern-two"></div>

      <v-row align="center" class="hero-row">

        <!-- HERO CONTENT -->
        <v-col cols="12" lg="7" class="hero-content">

          <div class="eyebrow">
            <span class="eyebrow-line"></span>
            ABOUT CHESSKWEEN
          </div>

          <h1 class="hero-title">
            AI-Based Chess Player
            <span>Style Classification</span>
            and Move Recommendation System
          </h1>

          <p class="hero-description">
            ChessKween is an AI-powered chess analysis system that identifies
            a player's playing style and provides personalized move
            recommendations using machine learning and Stockfish engine
            analysis.
          </p>

          <div class="hero-actions">
            <v-btn
              size="large"
              rounded="lg"
              class="explore-btn"
              @click="scrollToFeatures"
            >
              <v-icon start size="20">
                mdi-chess-queen
              </v-icon>

              Explore ChessKween

              <v-icon end size="19">
                mdi-arrow-down
              </v-icon>
            </v-btn>
          </div>

          <div class="hero-mini-stats">

            <div class="mini-stat">
              <div class="mini-icon">
                <v-icon size="19">
                  mdi-brain
                </v-icon>
              </div>

              <div>
                <strong>AI Powered</strong>
                <span>Machine Learning</span>
              </div>
            </div>

            <div class="mini-divider"></div>

            <div class="mini-stat">
              <div class="mini-icon">
                <v-icon size="19">
                  mdi-chess-king
                </v-icon>
              </div>

              <div>
                <strong>Stockfish</strong>
                <span>Engine Analysis</span>
              </div>
            </div>

          </div>
        </v-col>

        <!-- HERO IMAGE -->
        <v-col
          cols="12"
          lg="5"
          class="hero-image-column"
        >
          <div class="hero-image-area">

            <div class="image-orbit orbit-one"></div>
            <div class="image-orbit orbit-two"></div>

            <div class="image-glow"></div>

            <div class="image-card">

              <div class="image-card-label">
                <v-icon size="15">
                  mdi-crown
                </v-icon>

                CHESSKWEEN AI
              </div>

              <v-img
                src="/images/chesskween-coach.png"
                alt="ChessKween AI Chess Coach"
                class="chesskween-image"
                contain
              />

              <div class="image-card-bottom">
                <span>YOUR CHESS COACH</span>

                <v-icon size="17">
                  mdi-chess-queen
                </v-icon>
              </div>

            </div>

            <div class="floating-badge badge-top">
              <div class="badge-icon">
                <v-icon size="17">
                  mdi-brain
                </v-icon>
              </div>

              <div>
                <strong>AI Analysis</strong>
                <span>Smart insights</span>
              </div>
            </div>

            <div class="floating-badge badge-bottom">
              <div class="badge-icon">
                <v-icon size="17">
                  mdi-lightbulb-on
                </v-icon>
              </div>

              <div>
                <strong>Style-Aware</strong>
                <span>Personalized moves</span>
              </div>
            </div>

          </div>
        </v-col>

      </v-row>
    </section>


    <!-- =========================
         FEATURES
    ========================== -->
    <section
      id="about-features"
      class="feature-section"
    >

      <v-row>
        <v-col
          v-for="feature in features"
          :key="feature.title"
          cols="12"
          md="4"
        >
          <div class="feature-card">

            <div class="feature-icon">
              <v-icon size="26">
                {{ feature.icon }}
              </v-icon>
            </div>

            <div class="feature-content">
              <span class="feature-number">
                0{{ features.indexOf(feature) + 1 }}
              </span>

              <h3>
                {{ feature.title }}
              </h3>

              <p>
                {{ feature.description }}
              </p>
            </div>

            <div class="feature-arrow">
              <v-icon size="18">
                mdi-arrow-top-right
              </v-icon>
            </div>

          </div>
        </v-col>
      </v-row>

    </section>


    <!-- =========================
         WHAT IS CHESSKWEEN
    ========================== -->
    <section class="about-card">

      <div class="about-card-pattern"></div>

      <v-row
        align="center"
        class="position-relative"
      >

        <v-col cols="12" lg="8">

          <div class="section-label">
            <span></span>
            THE CHESSKWEEN EXPERIENCE
          </div>

          <h2>
            What is
            <span>ChessKween?</span>
          </h2>

          <p class="about-lead">
            ChessKween is designed to analyze chess games in PGN format and
            identify the playing characteristics of a chess player. The system
            extracts meaningful chess features from multiple games and uses
            them to determine the player's dominant style.
          </p>

          <p>
            By combining machine learning and Stockfish analysis, ChessKween
            helps players understand their strengths and weaknesses while
            providing personalized move recommendations that fit the way they
            naturally play chess.
          </p>

          <div class="about-highlights">

            <div class="highlight-item">

              <div class="highlight-icon">
                <v-icon size="18">
                  mdi-chart-line
                </v-icon>
              </div>

              <div>
                <strong>Understand Your Style</strong>
                <span>
                  Discover the characteristics behind your games.
                </span>
              </div>

            </div>

            <div class="highlight-item">

              <div class="highlight-icon">
                <v-icon size="18">
                  mdi-target
                </v-icon>
              </div>

              <div>
                <strong>Make Better Decisions</strong>
                <span>
                  Explore playable moves that fit your style.
                </span>
              </div>

            </div>

          </div>

        </v-col>

        <v-col
          cols="12"
          lg="4"
          class="about-art-column"
        >

          <div class="about-art">

            <div class="art-circle"></div>

            <div class="art-crown">
              <v-icon size="25">
                mdi-crown
              </v-icon>
            </div>

            <div class="art-title">
              Better
              <br />
              Moves
              <br />
              <span>Bigger</span>
              <br />
              Goals
            </div>

            <div class="art-board">
              <span
                v-for="n in 16"
                :key="n"
                :class="{ dark: n % 2 === 0 }"
              ></span>
            </div>

            <div class="art-queen">
              <v-icon size="28">
                mdi-chess-queen
              </v-icon>
            </div>

          </div>

        </v-col>

      </v-row>

    </section>


    <!-- =========================
         HOW IT WORKS
    ========================== -->
    <section class="workflow-section">

      <div class="section-heading">

        <div class="section-label centered">
          <span></span>
          HOW CHESSKWEEN WORKS
          <span></span>
        </div>

        <h2>
          From your games to
          <span>better decisions.</span>
        </h2>

        <p>
          ChessKween combines your playing patterns, machine learning, and
          chess-engine analysis into one personalized experience.
        </p>

      </div>

      <div class="workflow-grid">

        <div
          v-for="(step, index) in steps"
          :key="step.number"
          class="workflow-item"
        >

          <div class="step-number">
            {{ step.number }}
          </div>

          <div class="step-icon">
            <v-icon size="25">
              {{ step.icon }}
            </v-icon>
          </div>

          <h3>
            {{ step.title }}
          </h3>

          <p>
            {{ step.description }}
          </p>

          <div
            v-if="index < steps.length - 1"
            class="step-connector"
          >
            <v-icon size="16">
              mdi-arrow-right
            </v-icon>
          </div>

        </div>

      </div>

    </section>


    <!-- =========================
         PLAYING STYLES
    ========================== -->
    <section class="styles-section">

      <div class="section-heading">

        <div class="section-label centered">
          <span></span>
          PLAYING STYLE
          <span></span>
        </div>

        <h2>
          Two styles.
          <span>One unique player.</span>
        </h2>

        <p>
          ChessKween currently classifies players according to two core
          playing styles.
        </p>

      </div>

      <v-row>

        <!-- AGGRESSIVE -->
        <v-col cols="12" md="6">

          <div class="style-card aggressive-card">

            <div class="style-card-accent"></div>

            <div class="style-card-icon">
              <v-icon size="29">
                mdi-sword-cross
              </v-icon>
            </div>

            <div class="style-card-content">

              <span class="style-tag">
                STYLE 01
              </span>

              <h3>
                Aggressive
              </h3>

              <p>
                Characterized by active attacks, tactical opportunities,
                sacrifices, king pressure, and direct attacking play.
              </p>

              <div class="style-features">

                <span>
                  <v-icon size="14">mdi-check</v-icon>
                  Tactical play
                </span>

                <span>
                  <v-icon size="14">mdi-check</v-icon>
                  King attacks
                </span>

                <span>
                  <v-icon size="14">mdi-check</v-icon>
                  Dynamic positions
                </span>

              </div>

            </div>

          </div>

        </v-col>


        <!-- POSITIONAL -->
        <v-col cols="12" md="6">

          <div class="style-card positional-card">

            <div class="style-card-accent"></div>

            <div class="style-card-icon">
              <v-icon size="29">
                mdi-chess-bishop
              </v-icon>
            </div>

            <div class="style-card-content">

              <span class="style-tag">
                STYLE 02
              </span>

              <h3>
                Positional
              </h3>

              <p>
                Characterized by strong center control, piece activity,
                coordination, space, outposts, and long-term planning.
              </p>

              <div class="style-features">

                <span>
                  <v-icon size="14">mdi-check</v-icon>
                  Center control
                </span>

                <span>
                  <v-icon size="14">mdi-check</v-icon>
                  Piece activity
                </span>

                <span>
                  <v-icon size="14">mdi-check</v-icon>
                  Strategic play
                </span>

              </div>

            </div>

          </div>

        </v-col>

      </v-row>

    </section>


    <!-- =========================
         TECHNOLOGY
    ========================== -->
    <section class="technology-section">

      <div class="technology-header">

        <div>

          <div class="section-label">
            <span></span>
            TECHNOLOGY
          </div>

          <h2>
            Powered by
            <span>intelligent analysis.</span>
          </h2>

        </div>

        <p>
          ChessKween combines machine learning, chess-engine evaluation,
          and modern web technologies to deliver its analysis.
        </p>

      </div>

      <v-row>

        <v-col
          v-for="technology in technologies"
          :key="technology.title"
          cols="12"
          sm="6"
          lg="3"
        >

          <div class="technology-card">

            <div class="technology-icon">
              <v-icon size="23">
                {{ technology.icon }}
              </v-icon>
            </div>

            <h3>
              {{ technology.title }}
            </h3>

            <p>
              {{ technology.text }}
            </p>

          </div>

        </v-col>

      </v-row>

    </section>


    <!-- =========================
         FINAL CTA
    ========================== -->
    <section class="final-card">

      <div class="final-pattern"></div>

      <div class="final-content">

        <div class="final-icon">
          <v-icon size="30">
            mdi-chess-queen
          </v-icon>
        </div>

        <div class="final-text">

          <div class="final-label">
            PLAY. ANALYZE. IMPROVE.
          </div>

          <h2>
            Your games tell a story.
            <span>ChessKween helps you read it.</span>
          </h2>

          <p>
            Understand your style, analyze your decisions, and discover
            moves that fit the way you play.
          </p>

        </div>

        <v-btn
          variant="flat"
          rounded="lg"
          size="large"
          class="final-button"
          @click="showDetails = !showDetails"
        >
          <v-icon start>
            mdi-chess-queen
          </v-icon>

          Start Improving

          <v-icon end>
            mdi-arrow-right
          </v-icon>
        </v-btn>

      </div>

      <div
        v-if="showDetails"
        class="final-message"
      >
        Upload your chess games and let ChessKween analyze your playing
        style and decisions.
      </div>

    </section>

  </v-container>
</template>

<style scoped>

/* =========================================================
   GLOBAL
========================================================= */

.about-page {
  min-height: 100%;
  padding: 28px 28px 60px;

  background:
    radial-gradient(
      circle at 85% 0%,
      rgba(242, 140, 40, 0.045),
      transparent 28%
    ),
    #f5f7fa;

  color: #172033;
}


/* =========================================================
   HERO
========================================================= */

.hero-section {
  position: relative;
  overflow: hidden;

  min-height: 455px;

  border: 1px solid #e5e9ef;
  border-radius: 22px;

  background: #ffffff;

  box-shadow:
    0 18px 50px rgba(7, 23, 45, 0.08);
}

.hero-row {
  position: relative;
  z-index: 2;

  min-height: 455px;
  margin: 0;
}

.hero-content {
  padding: 55px 25px 55px 52px !important;
}

.eyebrow,
.section-label {
  display: flex;
  align-items: center;
  gap: 9px;

  color: #f28c28;

  font-size: 12px;
  font-weight: 900;
  letter-spacing: 1.6px;
}

.eyebrow-line,
.section-label > span {
  width: 28px;
  height: 3px;

  border-radius: 10px;

  background: #f28c28;
}

.hero-title {
  max-width: 720px;

  margin: 16px 0 20px;

  color: #0b1f3a;

  font-size: clamp(37px, 4vw, 57px);
  line-height: 1.04;
  font-weight: 900;

  letter-spacing: -2px;
}

.hero-title span {
  color: #f28c28;
}

.hero-description {
  max-width: 660px;

  margin: 0;

  color: #718096;

  font-size: 15px;
  line-height: 1.75;
}

.hero-actions {
  margin-top: 28px;
}

.explore-btn {
  min-height: 49px;

  padding: 0 23px;

  background: #f28c28 !important;
  color: white !important;

  font-weight: 800;
  letter-spacing: 0.2px;

  box-shadow:
    0 10px 25px rgba(242, 140, 40, 0.25) !important;
}

.explore-btn:hover {
  background: #dc7311 !important;
}

.hero-mini-stats {
  display: flex;
  align-items: center;

  gap: 20px;

  margin-top: 31px;
}

.mini-stat {
  display: flex;
  align-items: center;
  gap: 10px;
}

.mini-icon {
  width: 38px;
  height: 38px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 10px;

  background: #fff3e4;
  color: #f28c28;
}

.mini-stat strong,
.mini-stat span {
  display: block;
}

.mini-stat strong {
  color: #172033;

  font-size: 11px;
  font-weight: 800;
}

.mini-stat span {
  margin-top: 2px;

  color: #8a96a8;

  font-size: 9px;
}

.mini-divider {
  width: 1px;
  height: 31px;

  background: #e5e9ef;
}


/* =========================================================
   HERO BACKGROUND
========================================================= */

.hero-pattern {
  position: absolute;

  border: 1px solid rgba(11, 31, 58, 0.035);

  border-radius: 50%;
}

.pattern-one {
  width: 500px;
  height: 500px;

  right: -260px;
  top: -260px;
}

.pattern-two {
  width: 320px;
  height: 320px;

  right: -130px;
  bottom: -180px;
}


/* =========================================================
   HERO IMAGE
========================================================= */

.hero-image-column {
  display: flex;
  align-items: center;
  justify-content: center;

  min-height: 455px;

  padding: 15px 35px 15px 0 !important;
}

.hero-image-area {
  position: relative;

  width: 100%;
  max-width: 430px;
  height: 420px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.image-card {
  position: relative;
  z-index: 3;

  width: 325px;
  height: 325px;

  padding: 9px;

  overflow: visible;

  border-radius: 50%;

  background: #ffffff;

  box-shadow:
    0 25px 55px rgba(7, 23, 45, 0.18),
    0 0 0 1px rgba(11, 31, 58, 0.08);
}

.chesskween-image {
  width: 100%;
  height: 100%;

  border-radius: 50%;

  overflow: hidden;

  filter:
    drop-shadow(
      0 12px 20px rgba(7, 23, 45, 0.2)
    );

  transition: transform 0.4s ease;
}

.image-card:hover .chesskween-image {
  transform: scale(1.025);
}

.image-card-label {
  position: absolute;
  z-index: 5;

  top: 13px;
  left: 50%;

  display: flex;
  align-items: center;
  gap: 5px;

  padding: 7px 13px;

  border-radius: 30px;

  background: #0b1f3a;

  color: white;

  font-size: 9px;
  font-weight: 900;
  letter-spacing: 1px;

  transform: translateX(-50%);

  box-shadow:
    0 7px 17px rgba(7, 23, 45, 0.2);
}

.image-card-label .v-icon {
  color: #f28c28;
}

.image-card-bottom {
  position: absolute;
  z-index: 5;

  right: 35px;
  bottom: 17px;
  left: 35px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  padding: 9px 13px;

  border-radius: 20px;

  background: rgba(7, 23, 45, 0.92);

  color: white;

  backdrop-filter: blur(8px);
}

.image-card-bottom span {
  font-size: 8px;
  font-weight: 900;
  letter-spacing: 1.8px;
}

.image-card-bottom .v-icon {
  color: #f28c28;
}

.image-glow {
  position: absolute;
  z-index: 1;

  width: 320px;
  height: 320px;

  border-radius: 50%;

  background: rgba(242, 140, 40, 0.1);

  filter: blur(25px);
}

.image-orbit {
  position: absolute;

  border: 1px solid rgba(11, 31, 58, 0.09);

  border-radius: 50%;
}

.orbit-one {
  width: 380px;
  height: 380px;
}

.orbit-two {
  width: 430px;
  height: 250px;

  transform: rotate(-22deg);
}

.floating-badge {
  position: absolute;
  z-index: 7;

  display: flex;
  align-items: center;

  gap: 9px;

  min-width: 140px;

  padding: 10px 13px;

  border: 1px solid #e5e9ef;
  border-radius: 13px;

  background: rgba(255, 255, 255, 0.96);

  box-shadow:
    0 12px 28px rgba(7, 23, 45, 0.12);

  backdrop-filter: blur(12px);
}

.badge-icon {
  width: 32px;
  height: 32px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 9px;

  background: #fff3e4;
  color: #f28c28;
}

.floating-badge strong,
.floating-badge span {
  display: block;
}

.floating-badge strong {
  color: #172033;

  font-size: 10px;
  font-weight: 800;
}

.floating-badge span {
  margin-top: 2px;

  color: #8a96a8;

  font-size: 8px;
}

.badge-top {
  top: 52px;
  right: -4px;
}

.badge-bottom {
  bottom: 53px;
  left: -4px;
}


/* =========================================================
   FEATURES
========================================================= */

.feature-section {
  padding: 22px 0 0;
}

.feature-card {
  position: relative;

  min-height: 155px;

  display: flex;
  align-items: flex-start;

  gap: 19px;

  padding: 23px;

  overflow: hidden;

  border: 1px solid #e5e9ef;
  border-radius: 17px;

  background: #ffffff;

  box-shadow:
    0 8px 25px rgba(7, 23, 45, 0.045);

  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease,
    border-color 0.25s ease;
}

.feature-card::after {
  content: "";

  position: absolute;

  right: -45px;
  bottom: -55px;

  width: 140px;
  height: 140px;

  border-radius: 50%;

  background: rgba(242, 140, 40, 0.045);
}

.feature-card:hover {
  transform: translateY(-4px);

  border-color: rgba(242, 140, 40, 0.35);

  box-shadow:
    0 17px 35px rgba(7, 23, 45, 0.09);
}

.feature-icon {
  flex: 0 0 58px;

  width: 58px;
  height: 58px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 13px;

  background: #0b1f3a;
  color: #f28c28;

  box-shadow:
    0 8px 18px rgba(7, 23, 45, 0.16);
}

.feature-content {
  min-width: 0;
  padding-right: 16px;
}

.feature-number {
  color: #f28c28;

  font-size: 9px;
  font-weight: 900;
  letter-spacing: 1.5px;
}

.feature-content h3 {
  margin: 4px 0 7px;

  color: #0b1f3a;

  font-size: 16px;
  font-weight: 850;
}

.feature-content p {
  margin: 0;

  color: #718096;

  font-size: 12px;
  line-height: 1.65;
}

.feature-arrow {
  position: absolute;

  top: 19px;
  right: 18px;

  color: #c5ccd6;
}

.feature-card:hover .feature-arrow {
  color: #f28c28;
}


/* =========================================================
   ABOUT CARD
========================================================= */

.about-card {
  position: relative;

  margin-top: 22px;

  padding: 40px 42px;

  overflow: hidden;

  border: 1px solid #e5e9ef;
  border-radius: 19px;

  background: #ffffff;

  box-shadow:
    0 10px 35px rgba(7, 23, 45, 0.055);
}

.about-card-pattern {
  position: absolute;

  right: -120px;
  bottom: -160px;

  width: 430px;
  height: 430px;

  border-radius: 50%;

  border: 60px solid rgba(242, 140, 40, 0.045);
}

.position-relative {
  position: relative;
}

.about-card h2,
.workflow-section h2,
.styles-section h2,
.technology-section h2 {
  margin: 9px 0 13px;

  color: #0b1f3a;

  font-size: 30px;
  font-weight: 900;

  letter-spacing: -0.7px;
}

.about-card h2 span,
.workflow-section h2 span,
.styles-section h2 span,
.technology-section h2 span {
  color: #f28c28;
}

.about-card p {
  max-width: 800px;

  margin: 0 0 13px;

  color: #718096;

  font-size: 14px;
  line-height: 1.75;
}

.about-card .about-lead {
  color: #526174;
}

.about-highlights {
  display: flex;
  flex-wrap: wrap;

  gap: 12px;

  margin-top: 22px;
}

.highlight-item {
  display: flex;
  align-items: center;

  gap: 10px;

  min-width: 220px;

  padding: 11px 14px;

  border: 1px solid #e5e9ef;
  border-radius: 12px;

  background: #fafbfc;
}

.highlight-icon {
  width: 35px;
  height: 35px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 9px;

  background: #fff3e4;
  color: #f28c28;
}

.highlight-item strong,
.highlight-item span {
  display: block;
}

.highlight-item strong {
  color: #172033;

  font-size: 11px;
}

.highlight-item span {
  margin-top: 2px;

  color: #8a96a8;

  font-size: 9px;
}


/* =========================================================
   ABOUT ART
========================================================= */

.about-art-column {
  display: flex;
  justify-content: center;
}

.about-art {
  position: relative;

  width: 245px;
  height: 245px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.art-circle {
  position: absolute;

  width: 220px;
  height: 220px;

  border-radius: 50%;

  background: #0b1f3a;

  box-shadow:
    0 20px 40px rgba(7, 23, 45, 0.18);
}

.art-circle::after {
  content: "";

  position: absolute;

  inset: 10px;

  border: 1px solid rgba(242, 140, 40, 0.35);

  border-radius: 50%;
}

.art-crown {
  position: absolute;

  top: 13px;

  z-index: 4;

  color: #f28c28;
}

.art-title {
  position: relative;
  z-index: 3;

  color: white;

  font-family:
    Georgia,
    "Times New Roman",
    serif;

  font-size: 28px;
  font-style: italic;
  font-weight: 700;

  line-height: 0.98;

  text-align: center;
}

.art-title span {
  color: #f28c28;
  font-size: 1.08em;
}

.art-board {
  position: absolute;

  right: -8px;
  bottom: -5px;

  width: 115px;
  height: 115px;

  display: grid;

  grid-template-columns: repeat(4, 1fr);

  transform: rotate(-9deg);

  opacity: 0.28;
}

.art-board span {
  background: #ffffff;
}

.art-board span.dark {
  background: #f28c28;
}

.art-queen {
  position: absolute;

  bottom: 7px;
  left: 12px;

  z-index: 4;

  color: #f28c28;
}


/* =========================================================
   WORKFLOW
========================================================= */

.workflow-section,
.styles-section,
.technology-section {
  padding-top: 54px;
}

.section-heading {
  max-width: 720px;

  margin: 0 auto 30px;

  text-align: center;
}

.section-label.centered {
  justify-content: center;
}

.section-heading h2 {
  margin-top: 11px;
}

.section-heading p {
  margin: 0;

  color: #718096;

  font-size: 14px;
  line-height: 1.7;
}

.workflow-grid {
  display: grid;

  grid-template-columns: repeat(4, 1fr);

  gap: 14px;
}

.workflow-item {
  position: relative;

  min-height: 250px;

  padding: 23px 21px;

  border: 1px solid #e5e9ef;
  border-radius: 16px;

  background: #ffffff;

  box-shadow:
    0 7px 25px rgba(7, 23, 45, 0.045);

  transition:
    transform 0.25s ease,
    border-color 0.25s ease;
}

.workflow-item:hover {
  transform: translateY(-4px);

  border-color: rgba(242, 140, 40, 0.3);
}

.step-number {
  position: absolute;

  top: 15px;
  right: 17px;

  color: #e9ecf1;

  font-size: 30px;
  font-weight: 900;
}

.step-icon {
  width: 54px;
  height: 54px;

  display: flex;
  align-items: center;
  justify-content: center;

  margin-bottom: 20px;

  border-radius: 14px;

  background: #0b1f3a;
  color: #f28c28;
}

.workflow-item h3 {
  margin: 0 0 8px;

  color: #172033;

  font-size: 16px;
  font-weight: 850;
}

.workflow-item p {
  margin: 0;

  color: #718096;

  font-size: 12px;
  line-height: 1.7;
}

.step-connector {
  position: absolute;

  top: 50%;
  right: -21px;

  z-index: 5;

  width: 27px;
  height: 27px;

  display: flex;
  align-items: center;
  justify-content: center;

  border: 1px solid #e5e9ef;
  border-radius: 50%;

  background: white;

  color: #f28c28;

  transform: translateY(-50%);
}


/* =========================================================
   STYLE CARDS
========================================================= */

.style-card {
  position: relative;

  min-height: 225px;

  display: flex;

  gap: 22px;

  padding: 27px;

  overflow: hidden;

  border: 1px solid #e5e9ef;
  border-radius: 18px;

  background: white;

  box-shadow:
    0 8px 28px rgba(7, 23, 45, 0.055);

  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease;
}

.style-card:hover {
  transform: translateY(-4px);

  box-shadow:
    0 15px 35px rgba(7, 23, 45, 0.09);
}

.style-card::before {
  content: "";

  position: absolute;

  top: -80px;
  right: -80px;

  width: 210px;
  height: 210px;

  border-radius: 50%;

  background: rgba(242, 140, 40, 0.045);
}

.style-card-accent {
  position: absolute;

  top: 0;
  bottom: 0;
  left: 0;

  width: 4px;

  background: #f28c28;
}

.positional-card .style-card-accent {
  background: #0b1f3a;
}

.style-card-icon {
  position: relative;

  flex: 0 0 63px;

  width: 63px;
  height: 63px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 15px;

  background: #0b1f3a;
  color: #f28c28;
}

.positional-card .style-card-icon {
  background: #f1f3f6;
  color: #0b1f3a;
}

.style-card-content {
  position: relative;
  z-index: 2;
}

.style-tag {
  color: #f28c28;

  font-size: 9px;
  font-weight: 900;
  letter-spacing: 1.5px;
}

.style-card h3 {
  margin: 2px 0 7px;

  color: #0b1f3a;

  font-size: 22px;
  font-weight: 900;
}

.style-card p {
  max-width: 500px;

  margin: 0;

  color: #718096;

  font-size: 13px;
  line-height: 1.7;
}

.style-features {
  display: flex;
  flex-wrap: wrap;

  gap: 7px;

  margin-top: 16px;
}

.style-features span {
  display: flex;
  align-items: center;

  gap: 4px;

  padding: 5px 8px;

  border-radius: 8px;

  background: #f5f7fa;

  color: #526174;

  font-size: 9px;
  font-weight: 700;
}

.style-features .v-icon {
  color: #f28c28;
}


/* =========================================================
   TECHNOLOGY
========================================================= */

.technology-header {
  display: flex;
  align-items: end;
  justify-content: space-between;

  gap: 30px;

  margin-bottom: 22px;
}

.technology-header h2 {
  margin-bottom: 0;
}

.technology-header > p {
  max-width: 420px;

  margin: 0;

  color: #718096;

  font-size: 13px;
  line-height: 1.7;
}

.technology-card {
  min-height: 155px;

  padding: 22px;

  border: 1px solid #e5e9ef;
  border-radius: 15px;

  background: white;

  box-shadow:
    0 7px 23px rgba(7, 23, 45, 0.04);

  transition:
    transform 0.25s ease,
    border-color 0.25s ease;
}

.technology-card:hover {
  transform: translateY(-3px);

  border-color: rgba(242, 140, 40, 0.35);
}

.technology-icon {
  width: 46px;
  height: 46px;

  display: flex;
  align-items: center;
  justify-content: center;

  margin-bottom: 15px;

  border-radius: 11px;

  background: #0b1f3a;
  color: #f28c28;
}

.technology-card h3 {
  margin: 0 0 5px;

  color: #172033;

  font-size: 14px;
  font-weight: 850;
}

.technology-card p {
  margin: 0;

  color: #8190a2;

  font-size: 11px;
}


/* =========================================================
   FINAL CTA
========================================================= */

.final-card {
  position: relative;

  margin-top: 54px;

  padding: 30px 35px;

  overflow: hidden;

  border-radius: 19px;

  background: #0b1f3a;

  box-shadow:
    0 18px 38px rgba(7, 23, 45, 0.18);
}

.final-pattern {
  position: absolute;

  right: -100px;
  top: -160px;

  width: 400px;
  height: 400px;

  border: 60px solid rgba(242, 140, 40, 0.12);

  border-radius: 50%;
}

.final-content {
  position: relative;
  z-index: 2;

  display: flex;
  align-items: center;

  gap: 20px;
}

.final-icon {
  flex: 0 0 60px;

  width: 60px;
  height: 60px;

  display: flex;
  align-items: center;
  justify-content: center;

  border: 1px solid rgba(242, 140, 40, 0.35);
  border-radius: 15px;

  background: rgba(242, 140, 40, 0.12);

  color: #f28c28;
}

.final-text {
  min-width: 0;
}

.final-label {
  margin-bottom: 4px;

  color: #f28c28;

  font-size: 9px;
  font-weight: 900;
  letter-spacing: 1.5px;
}

.final-content h2 {
  margin: 0;

  color: white;

  font-size: 23px;
  line-height: 1.25;
  font-weight: 850;
}

.final-content h2 span {
  color: #f28c28;
}

.final-content p {
  max-width: 620px;

  margin: 5px 0 0;

  color: rgba(255, 255, 255, 0.68);

  font-size: 11px;
}

.final-button {
  margin-left: auto;

  background: #f28c28 !important;
  color: white !important;

  font-weight: 800;

  white-space: nowrap;

  box-shadow:
    0 8px 20px rgba(0, 0, 0, 0.18);
}

.final-button:hover {
  background: #dc7311 !important;
}

.final-message {
  position: relative;
  z-index: 2;

  margin-top: 17px;

  padding: 11px 15px;

  border: 1px solid rgba(242, 140, 40, 0.2);
  border-radius: 10px;

  background: rgba(242, 140, 40, 0.1);

  color: white;

  font-size: 12px;
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 1200px) {

  .hero-content {
    padding-left: 35px !important;
  }

  .hero-title {
    font-size: 42px;
  }

  .image-card {
    width: 290px;
    height: 290px;
  }

  .orbit-one {
    width: 340px;
    height: 340px;
  }

  .orbit-two {
    width: 380px;
  }

  .workflow-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .step-connector {
    display: none;
  }
}


@media (max-width: 960px) {

  .hero-section,
  .hero-row {
    min-height: auto;
  }

  .hero-content {
    padding: 38px 32px 15px !important;

    text-align: center;
  }

  .eyebrow {
    justify-content: center;
  }

  .hero-title,
  .hero-description {
    margin-right: auto;
    margin-left: auto;
  }

  .hero-actions {
    display: flex;
    justify-content: center;
  }

  .hero-mini-stats {
    justify-content: center;
  }

  .hero-image-column {
    min-height: 390px;

    padding: 0 20px 35px !important;
  }

  .technology-header {
    display: block;
  }

  .technology-header > p {
    margin-top: 10px;
  }
}


@media (max-width: 700px) {

  .about-page {
    padding: 15px 12px 40px;
  }

  .hero-section {
    border-radius: 17px;
  }

  .hero-content {
    padding: 30px 20px 8px !important;
  }

  .hero-title {
    font-size: 33px;
    letter-spacing: -1.2px;
  }

  .hero-description {
    font-size: 14px;
  }

  .hero-mini-stats {
    gap: 12px;
  }

  .mini-divider {
    height: 24px;
  }

  .mini-stat strong {
    font-size: 10px;
  }

  .mini-stat span {
    font-size: 8px;
  }

  .hero-image-column {
    min-height: 340px;
  }

  .hero-image-area {
    height: 330px;
  }

  .image-card {
    width: 250px;
    height: 250px;
  }

  .orbit-one {
    width: 290px;
    height: 290px;
  }

  .orbit-two {
    width: 330px;
    height: 200px;
  }

  .image-card-label {
    font-size: 7px;
  }

  .image-card-bottom {
    right: 27px;
    bottom: 12px;
    left: 27px;
  }

  .floating-badge {
    min-width: 118px;

    padding: 8px 9px;
  }

  .badge-top {
    top: 22px;
    right: -2px;
  }

  .badge-bottom {
    bottom: 22px;
    left: -2px;
  }

  .feature-card {
    min-height: auto;
  }

  .about-card {
    padding: 27px 22px;
  }

  .about-card h2,
  .workflow-section h2,
  .styles-section h2,
  .technology-section h2 {
    font-size: 26px;
  }

  .about-art-column {
    margin-top: 20px;
  }

  .workflow-grid {
    grid-template-columns: 1fr;
  }

  .style-card {
    padding: 21px;
  }

  .final-content {
    align-items: flex-start;
    flex-wrap: wrap;
  }

  .final-button {
    margin-left: 0;
  }
}


@media (max-width: 480px) {

  .hero-title {
    font-size: 29px;
  }

  .hero-mini-stats {
    display: none;
  }

  .hero-image-area {
    transform: scale(0.9);
  }

  .floating-badge {
    display: none;
  }

  .feature-card {
    gap: 14px;
    padding: 18px;
  }

  .feature-icon {
    flex-basis: 51px;

    width: 51px;
    height: 51px;
  }

  .about-highlights {
    display: block;
  }

  .highlight-item + .highlight-item {
    margin-top: 8px;
  }

  .style-card {
    display: block;
  }

  .style-card-icon {
    margin-bottom: 17px;
  }

  .final-card {
    padding: 25px 20px;
  }

  .final-content h2 {
    font-size: 20px;
  }
}
</style>