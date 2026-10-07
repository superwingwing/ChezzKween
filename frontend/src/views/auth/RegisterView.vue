<script setup>
import RegisterForm from '@/components/auth/RegisterForm.vue'
import { useDisplay } from 'vuetify'

const { mobile } = useDisplay()

const pieces = [
  { icon: 'mdi-chess-rook', active: false },
  { icon: 'mdi-chess-knight', active: true },
  { icon: 'mdi-chess-bishop', active: false },
  { icon: 'mdi-chess-queen', active: true },
  { icon: 'mdi-chess-king', active: false },
  { icon: 'mdi-chess-pawn', active: false },
  { icon: 'mdi-chess-pawn', active: true },
  { icon: 'mdi-chess-pawn', active: false }
]
</script>

<template>
  <div class="register-page">

    <!-- LEFT: REGISTER FORM -->
    <section class="form-side">

      <div class="form-wrapper">

        <!-- LOGIN LINK -->
        <div class="text-end mb-10">
          <span class="text-caption text-grey-darken-1">
            Already have an account?
          </span>

          <RouterLink
            to="/"
            class="text-caption font-weight-bold text-decoration-none ms-1"
            style="color: #f28c28;"
          >
            Login
          </RouterLink>
        </div>

        <!-- HEADING -->
        <div class="mb-7">
          <h1 class="text-h3 font-weight-black">
            Create Account
          </h1>

          <p class="text-body-2 text-grey-darken-1 mt-2">
            Create your ChessKween account and start improving your game.
          </p>
        </div>

        <!-- REGISTER FORM -->
        <RegisterForm />

      </div>

    </section>


    <!-- RIGHT: CHESSKWEEN VISUAL -->
    <section
      v-if="!mobile"
      class="visual-side"
    >

      <div class="visual-content">

        <!-- BRAND -->
        <div class="d-flex align-center ga-3 mb-8">

          <v-avatar
            color="orange-darken-1"
            rounded="lg"
            size="54"
          >
            <v-icon
              color="white"
              size="30"
            >
              mdi-chess-queen
            </v-icon>
          </v-avatar>

          <div>
            <div class="text-h5 font-weight-black text-white">
              Chess<span style="color: #f28c28;">Kween</span>
            </div>

            <div class="text-caption text-grey-lighten-1 font-weight-bold">
              ANALYTICS HUB
            </div>
          </div>

          <v-icon
            color="orange"
            size="11"
          >
            mdi-circle
          </v-icon>

        </div>


        <!-- ENGINE PREVIEW -->
        <v-card
          rounded="xl"
          elevation="8"
          color="#111111"
          class="engine-preview pa-4"
        >

          <!-- ENGINE HEADER -->
          <div class="d-flex justify-space-between align-center mb-4">

            <div class="d-flex align-center ga-2">

              <v-avatar
                color="orange-darken-2"
                rounded="sm"
                size="30"
              >
                <span class="font-weight-bold text-white">
                  AI
                </span>
              </v-avatar>

              <span class="font-weight-bold text-white">
                ChessKween AI
              </span>

            </div>

            <v-chip
              size="small"
              color="green"
              variant="tonal"
              class="font-weight-bold"
            >
              99.4% Accuracy
            </v-chip>

          </div>

          <v-divider
            color="grey-darken-3"
            class="mb-4"
          />


          <!-- CHESS ENGINE GRID -->
          <v-row dense>

            <v-col
              v-for="(piece, index) in pieces"
              :key="index"
              cols="3"
            >

              <v-card
                height="92"
                rounded="sm"
                :color="piece.active ? '#3b2b20' : '#1b1b1b'"
                class="d-flex align-center justify-center"
              >

                <v-icon
                  :color="piece.active ? 'orange' : 'grey-lighten-1'"
                  size="30"
                >
                  {{ piece.icon }}
                </v-icon>

              </v-card>

            </v-col>

          </v-row>


          <!-- BEST MOVE -->
          <v-card
            color="#080808"
            rounded="lg"
            class="mt-4 pa-3"
          >

            <div class="d-flex align-center ga-3">

              <v-avatar
                color="orange"
                size="38"
              >
                <v-icon color="white">
                  mdi-lightbulb-on
                </v-icon>
              </v-avatar>

              <div>

                <div
                  class="text-caption font-weight-bold"
                  style="color: #f28c28;"
                >
                  Best Move Identified
                </div>

                <div class="text-caption text-grey-lighten-1">
                  Tactical opportunity detected.
                </div>

              </div>

            </div>

          </v-card>

        </v-card>


        <!-- MAIN MESSAGE -->
        <div class="text-center mt-8">

          <h2 class="text-h4 font-weight-black text-white">
            Master Every Move with
            <span style="color: #f28c28;">
              AI Precision
            </span>
          </h2>

          <p class="text-body-2 text-grey-lighten-1 mt-3">
            Elevate your game with style-aware recommendations,
            instant PGN analysis, and real-time engine feedback.
          </p>

        </div>


        <!-- FEATURES -->
        <v-row
          class="mt-5"
          align="center"
        >

          <v-col class="text-center">

            <v-icon
              color="orange"
              size="24"
            >
              mdi-brain
            </v-icon>

            <div class="text-caption text-grey-lighten-1 mt-1">
              Style<br>
              Classification
            </div>

          </v-col>

          <v-divider
            vertical
            color="grey-darken-3"
          />

          <v-col class="text-center">

            <v-icon
              color="orange"
              size="24"
            >
              mdi-magnify
            </v-icon>

            <div class="text-caption text-grey-lighten-1 mt-1">
              Game<br>
              Analysis
            </div>

          </v-col>

          <v-divider
            vertical
            color="grey-darken-3"
          />

          <v-col class="text-center">

            <v-icon
              color="orange"
              size="24"
            >
              mdi-lightbulb-on-outline
            </v-icon>

            <div class="text-caption text-grey-lighten-1 mt-1">
              Personalized<br>
              Recommendations
            </div>

          </v-col>

        </v-row>

      </div>

    </section>

  </div>
</template>

<style scoped>
.register-page {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 50% 50%;
  background: #f7f7f7;
}

.form-side {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  padding: 40px 70px;
}

.form-wrapper {
  width: 100%;
  max-width: 520px;
}

.visual-side {
  min-height: 100vh;
  padding: 45px 55px;
  background: #080808;
}

.visual-content {
  max-width: 650px;
  margin: auto;
}

.engine-preview {
  border: 1px solid #292929;
}

@media (max-width: 960px) {
  .form-side {
    padding: 30px;
  }
}

@media (max-width: 600px) {
  .register-page {
    display: block;
  }

  .form-side {
    min-height: 100vh;
    padding: 25px;
  }
}
</style>