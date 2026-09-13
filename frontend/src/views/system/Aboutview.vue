<template>
  <v-container fluid class="about-page py-8">
    <v-row justify="center">
      <v-col cols="12" xl="10">

        <!-- Hero -->
        <v-card class="hero-card mb-8" rounded="xl" elevation="0">
          <v-row align="center" class="pa-6 pa-md-10">
            <v-col cols="12" md="8">
              <div class="section-label mb-3">ABOUT CHESSKWEEN</div>

              <h1 class="hero-title mb-4">
                AI-Based Chess Player
                <span>Style Classification</span>
                and Move Recommendation System
              </h1>

              <p class="hero-description mb-6">
                ChessKween is an AI-powered chess analysis system that
                identifies a player's playing style and provides
                personalized move recommendations using machine learning
                and Stockfish engine analysis.
              </p>

              <v-btn
                color="primary"
                size="large"
                rounded="lg"
                @click="scrollToFeatures"
              >
                Explore ChessKween
                <v-icon end>mdi-arrow-down</v-icon>
              </v-btn>
            </v-col>

            <v-col cols="12" md="4" class="text-center">
              <v-icon class="hero-icon" color="primary">
                mdi-chess-queen
              </v-icon>
            </v-col>
          </v-row>
        </v-card>

        <!-- About -->
        <v-card rounded="xl" elevation="1" class="section-card mb-8">
          <v-card-item>
            <v-card-title class="section-title">
              What is ChessKween?
            </v-card-title>
          </v-card-item>

          <v-card-text class="section-content">
            <p>
              ChessKween is designed to analyze chess games in PGN format
              and identify the playing characteristics of a chess player.
              The system extracts meaningful chess features from multiple
              games and uses them to determine the player's dominant style.
            </p>

            <p>
              The classification focuses on two primary styles:
              <strong>Aggressive</strong> and <strong>Positional</strong>.
              Tactical characteristics such as sacrifices, king attacks,
              tactical captures, and attacking piece activity are considered
              as part of the Aggressive style.
            </p>

            <p>
              After determining the player's style, ChessKween uses
              Stockfish to evaluate the current chess position and identify
              strong candidate moves. These candidates are then considered
              according to the player's classified style to provide a more
              personalized recommendation.
            </p>
          </v-card-text>
        </v-card>

        <!-- Features -->
        <section id="features" class="mb-8">
          <div class="section-heading text-center mb-6">
            <h2 class="section-title">Key Features</h2>
            <p class="section-subtitle">
              Tools designed to provide personalized chess analysis.
            </p>
          </div>

          <v-row>
            <v-col
              v-for="feature in features"
              :key="feature.title"
              cols="12"
              sm="6"
              lg="4"
            >
              <v-card
                class="feature-card h-100"
                rounded="xl"
                elevation="1"
              >
                <v-card-text class="pa-6">
                  <v-avatar
                    color="primary"
                    variant="tonal"
                    size="52"
                    class="mb-4"
                  >
                    <v-icon>{{ feature.icon }}</v-icon>
                  </v-avatar>

                  <h3 class="feature-title mb-2">
                    {{ feature.title }}
                  </h3>

                  <p class="feature-description">
                    {{ feature.description }}
                  </p>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </section>

        <!-- How It Works -->
        <v-card rounded="xl" elevation="1" class="section-card mb-8">
          <v-card-item>
            <v-card-title class="section-title text-center">
              How ChessKween Works
            </v-card-title>

            <v-card-subtitle class="text-center mt-2">
              From chess games to personalized recommendations.
            </v-card-subtitle>
          </v-card-item>

          <v-card-text class="pa-4 pa-md-8">
            <v-row>
              <v-col
                v-for="(step, index) in steps"
                :key="step.title"
                cols="12"
                sm="6"
                lg="4"
              >
                <div class="process-step">
                  <v-avatar
                    color="primary"
                    size="42"
                    class="step-number mb-4"
                  >
                    {{ index + 1 }}
                  </v-avatar>

                  <h3 class="feature-title mb-2">
                    {{ step.title }}
                  </h3>

                  <p class="feature-description">
                    {{ step.description }}
                  </p>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Playing Styles -->
        <section class="mb-8">
          <div class="section-heading text-center mb-6">
            <h2 class="section-title">Playing Styles</h2>
            <p class="section-subtitle">
              ChessKween classifies players using two primary playing styles.
            </p>
          </div>

          <v-row>
            <v-col cols="12" md="6">
              <v-card
                rounded="xl"
                elevation="1"
                class="style-card aggressive-style h-100"
              >
                <v-card-text class="pa-6 pa-md-8">
                  <v-icon
                    size="42"
                    color="error"
                    class="mb-4"
                  >
                    mdi-fire
                  </v-icon>

                  <h3 class="style-title mb-3">
                    Aggressive
                  </h3>

                  <p class="style-description mb-5">
                    A style focused on active play, attacking opportunities,
                    king pressure, tactical operations, and dynamic piece
                    activity.
                  </p>

                  <div class="style-features">
                    <v-chip
                      v-for="item in aggressiveFeatures"
                      :key="item"
                      size="small"
                      class="mr-2 mb-2"
                      variant="tonal"
                    >
                      {{ item }}
                    </v-chip>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>

            <v-col cols="12" md="6">
              <v-card
                rounded="xl"
                elevation="1"
                class="style-card positional-style h-100"
              >
                <v-card-text class="pa-6 pa-md-8">
                  <v-icon
                    size="42"
                    color="primary"
                    class="mb-4"
                  >
                    mdi-chess-board
                  </v-icon>

                  <h3 class="style-title mb-3">
                    Positional
                  </h3>

                  <p class="style-description mb-5">
                    A style focused on strategic improvements, center
                    control, space advantage, piece activity, coordination,
                    and long-term positional benefits.
                  </p>

                  <div class="style-features">
                    <v-chip
                      v-for="item in positionalFeatures"
                      :key="item"
                      size="small"
                      class="mr-2 mb-2"
                      variant="tonal"
                    >
                      {{ item }}
                    </v-chip>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </section>

        <!-- Technologies -->
        <v-card rounded="xl" elevation="1" class="section-card mb-8">
          <v-card-item>
            <v-card-title class="section-title text-center">
              Technology Stack
            </v-card-title>
          </v-card-item>

          <v-card-text class="pa-6 pa-md-8">
            <v-row justify="center">
              <v-col
                v-for="technology in technologies"
                :key="technology.name"
                cols="6"
                sm="4"
                md="3"
                lg="2"
                class="text-center"
              >
                <v-icon
                  size="38"
                  color="primary"
                  class="mb-2"
                >
                  {{ technology.icon }}
                </v-icon>

                <div class="technology-name">
                  {{ technology.name }}
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Purpose -->
        <v-card
          rounded="xl"
          color="primary"
          elevation="0"
          class="purpose-card"
        >
          <v-card-text class="pa-6 pa-md-10 text-center">
            <v-icon
              size="46"
              color="white"
              class="mb-4"
            >
              mdi-school
            </v-icon>

            <h2 class="purpose-title mb-4">
              Project Purpose
            </h2>

            <p class="purpose-description">
              ChessKween aims to provide a personalized chess analysis
              experience by combining machine learning, chess feature
              extraction, and Stockfish engine evaluation. The system
              goes beyond selecting moves based only on engine strength
              by considering the player's classified playing style when
              presenting move recommendations.
            </p>
          </v-card-text>
        </v-card>

      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
const features = [
  {
    title: "PGN Upload",
    icon: "mdi-file-upload-outline",
    description:
      "Upload chess games in PGN format for player style classification and game analysis."
  },
  {
    title: "Style Classification",
    icon: "mdi-brain",
    description:
      "Analyze chess features from multiple games to classify the player's dominant playing style."
  },
  {
    title: "Stockfish Analysis",
    icon: "mdi-chess-queen",
    description:
      "Evaluate chess positions and identify strong candidate moves using the Stockfish engine."
  },
  {
    title: "Game Review",
    icon: "mdi-chart-line",
    description:
      "Review moves, evaluations, positions, and important moments from an analyzed chess game."
  },
  {
    title: "Style-Aware Recommendation",
    icon: "mdi-lightbulb-on-outline",
    description:
      "Consider the player's classified style when selecting suitable moves from strong engine candidates."
  },
  {
    title: "Player Insights",
    icon: "mdi-account-search-outline",
    description:
      "Present useful insights about the player's chess characteristics based on analyzed games."
  }
]

const steps = [
  {
    title: "Upload Games",
    description:
      "Chess games are uploaded in PGN format containing the players, game information, and move history."
  },
  {
    title: "Extract Features",
    description:
      "ChessKween extracts behavioral, tactical, and positional features from the uploaded games."
  },
  {
    title: "Classify Style",
    description:
      "The extracted features are processed by the machine learning classifier to determine the player's style."
  },
  {
    title: "Analyze Position",
    description:
      "Stockfish evaluates the current position and generates strong candidate moves."
  },
  {
    title: "Apply Style Filter",
    description:
      "Candidate moves are evaluated according to their compatibility with the player's classified style."
  },
  {
    title: "Recommend Move",
    description:
      "ChessKween presents a strong move recommendation that is suitable for the player's playing characteristics."
  }
]

const aggressiveFeatures = [
  "King Attacks",
  "Sacrifices",
  "Tactical Play",
  "Attacking Pieces",
  "Queen Attacks"
]

const positionalFeatures = [
  "Center Control",
  "Space Advantage",
  "Piece Activity",
  "Coordination",
  "Outposts"
]

const technologies = [
  {
    name: "Vue.js",
    icon: "mdi-vuejs"
  },
  {
    name: "Vuetify",
    icon: "mdi-view-dashboard-outline"
  },
  {
    name: "Python",
    icon: "mdi-language-python"
  },
  {
    name: "FastAPI",
    icon: "mdi-api"
  },
  {
    name: "Scikit-learn",
    icon: "mdi-brain"
  },
  {
    name: "Stockfish",
    icon: "mdi-chess-queen"
  },
  {
    name: "Supabase",
    icon: "mdi-database-outline"
  }
]

function scrollToFeatures() {
  document.getElementById("features")?.scrollIntoView({
    behavior: "smooth",
    block: "start"
  })
}
</script>

<style scoped>
.about-page {
  min-height: 100vh;
}

.hero-card {
  background: linear-gradient(
    135deg,
    rgba(var(--v-theme-primary), 0.08),
    rgba(var(--v-theme-primary), 0.02)
  );
  border: 1px solid rgba(var(--v-theme-primary), 0.12);
}

.section-label {
  color: rgb(var(--v-theme-primary));
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.12em;
}

.hero-title {
  max-width: 850px;
  font-size: clamp(2rem, 4vw, 3.5rem);
  font-weight: 800;
  line-height: 1.12;
  letter-spacing: -0.02em;
}

.hero-title span {
  color: rgb(var(--v-theme-primary));
}

.hero-description {
  max-width: 720px;
  font-size: 1.05rem;
  line-height: 1.7;
  color: rgba(var(--v-theme-on-surface), 0.68);
}

.hero-icon {
  font-size: clamp(100px, 15vw, 180px);
}

.section-card {
  overflow: hidden;
}

.section-title {
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 700;
}

.section-subtitle {
  max-width: 600px;
  margin: 8px auto 0;
  color: rgba(var(--v-theme-on-surface), 0.62);
}

.section-content {
  max-width: 900px;
  padding: 0 24px 28px;
}

.section-content p {
  margin-bottom: 16px;
  line-height: 1.75;
  color: rgba(var(--v-theme-on-surface), 0.7);
}

.section-content p:last-child {
  margin-bottom: 0;
}

.feature-card {
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

.feature-title {
  font-size: 1.05rem;
  font-weight: 700;
}

.feature-description {
  margin: 0;
  line-height: 1.65;
  color: rgba(var(--v-theme-on-surface), 0.64);
}

.process-step {
  height: 100%;
  padding: 8px;
}

.step-number {
  font-weight: 700;
  color: white;
}

.style-card {
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

.aggressive-style {
  border-top: 3px solid rgb(var(--v-theme-error));
}

.positional-style {
  border-top: 3px solid rgb(var(--v-theme-primary));
}

.style-title {
  font-size: 1.5rem;
  font-weight: 700;
}

.style-description {
  line-height: 1.7;
  color: rgba(var(--v-theme-on-surface), 0.65);
}

.technology-name {
  font-size: 0.9rem;
  font-weight: 600;
}

.purpose-title {
  color: white;
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 700;
}

.purpose-description {
  max-width: 850px;
  margin: 0 auto;
  color: rgba(255, 255, 255, 0.88);
  line-height: 1.75;
}

@media (max-width: 600px) {
  .about-page {
    padding: 24px 12px !important;
  }

  .hero-card .v-row {
    text-align: center;
  }

  .hero-description {
    font-size: 0.95rem;
  }

  .section-content {
    padding: 0 20px 24px;
  }

  .feature-card,
  .style-card {
    border-radius: 16px !important;
  }

  .purpose-description {
    font-size: 0.95rem;
  }
}
</style>

