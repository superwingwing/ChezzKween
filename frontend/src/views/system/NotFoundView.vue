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
    <v-main>
      <v-container
        fluid
        class="fill-height pa-4"
      >
        <v-row
          align="center"
          justify="center"
          class="fill-height"
        >
          <v-col
            cols="12"
            sm="10"
            md="8"
            lg="6"
          >
            <v-card
              class="error-card"
              elevation="8"
              rounded="xl"
            >
              <!-- Chess Queen -->
              <div class="queen-wrapper">
                <v-icon
                  icon="mdi-chess-queen"
                  class="queen-icon"
                />
              </div>

              <!-- 404 -->
              <div class="error-number">
                404
              </div>

              <!-- Title -->
              <h1 class="error-title">
                Page Not Found
              </h1>

              <!-- Description -->
              <p class="error-description">
                Oops! The page you're looking for doesn't exist
                or may have been moved.
              </p>

              <!-- Chess Pieces -->
              <div class="chess-decoration">
                <v-icon icon="mdi-chess-pawn" />
                <v-icon icon="mdi-chess-knight" />
                <v-icon icon="mdi-chess-rook" />
                <v-icon icon="mdi-chess-bishop" />
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
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<style scoped>
/* ==============================
   PAGE
   ============================== */

.not-found-page {
  min-height: 100vh;
  background: #ffffff;
}

/* ==============================
   CARD
   ============================== */

.error-card {
  padding: 55px 40px;
  text-align: center;
  background: #ffffff;
  border: 1px solid rgba(1, 87, 155, 0.12);
}

/* ==============================
   QUEEN
   ============================== */

.queen-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.queen-icon {
  font-size: 72px;
  color: #01579b;
}

/* ==============================
   404
   ============================== */

.error-number {
  font-size: clamp(90px, 16vw, 170px);
  line-height: 0.9;
  font-weight: 900;
  letter-spacing: -7px;
  color: #01579b;
}

/* ==============================
   TITLE
   ============================== */

.error-title {
  margin-top: 25px;
  color: #263238;
  font-size: clamp(26px, 4vw, 40px);
  font-weight: 700;
}

/* ==============================
   DESCRIPTION
   ============================== */

.error-description {
  max-width: 550px;
  margin: 15px auto 0;
  color: #607d8b;
  font-size: clamp(14px, 2vw, 17px);
  line-height: 1.7;
}

/* ==============================
   CHESS DECORATION
   ============================== */

.chess-decoration {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 18px;
  margin: 28px 0;
  color: #01579b;
}

.chess-decoration .v-icon {
  font-size: 28px;
}

/* ==============================
   BUTTONS
   ============================== */

.actions {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.home-btn {
  min-width: 175px;
  color: #ffffff;
}

.back-btn {
  min-width: 140px;
}

/* ==============================
   BRANDING
   ============================== */

.branding {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 7px;
  margin-top: 35px;
  color: #78909c;
  font-size: 14px;
  font-weight: 600;
}

/* ==============================
   TABLET / MOBILE
   ============================== */

@media (max-width: 600px) {
  .error-card {
    padding: 40px 22px;
  }

  .queen-icon {
    font-size: 58px;
  }

  .error-number {
    letter-spacing: -5px;
  }

  .error-title {
    margin-top: 18px;
  }

  .chess-decoration {
    gap: 12px;
    margin: 22px 0;
  }

  .chess-decoration .v-icon {
    font-size: 24px;
  }

  .actions {
    flex-direction: column;
    width: 100%;
  }

  .home-btn,
  .back-btn {
    width: 100%;
    max-width: 280px;
  }

  .branding {
    margin-top: 28px;
  }
}

/* ==============================
   SMALL PHONES
   ============================== */

@media (max-width: 360px) {
  .error-card {
    padding: 32px 16px;
  }

  .queen-icon {
    font-size: 50px;
  }

  .error-title {
    font-size: 24px;
  }

  .error-description {
    font-size: 13px;
  }

  .chess-decoration {
    gap: 8px;
  }

  .chess-decoration .v-icon {
    font-size: 21px;
  }
}
</style>
