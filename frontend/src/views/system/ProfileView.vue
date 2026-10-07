<script setup>
import { ref, reactive, onMounted } from "vue"
import { useAuthStore } from "@/stores/authUser"
import { supabase } from "@/utils/supabase"
import RecentGames from "@/components/layout/RecentGames.vue"

const authStore = useAuthStore()

const wins = ref(0)
const losses = ref(0)
const draws = ref(0)
const aggressivePercentage = ref(0)
const positionalPercentage = ref(0)
const totalGames = ref(0)

const profile = reactive({
  username: "",
  email: "",
  memberSince: "September 2026",
  avatar: null
})

// Come from authUser.js
if (authStore.user) {
  profile.username = authStore.user.user_metadata?.username || ""
  profile.email = authStore.user.email || ""
}

async function loadStylePercentages() {
  if (!authStore.user) return

  const { data, error } = await supabase
    .from("style")
    .select("predicted_style, white, black, result")
    .eq("user_id", authStore.user.id)

  if (error) {
    console.error("Error loading style percentages:", error)
    return
  }

  const games = data || []

  const aggressive = games.filter(
    game => game.predicted_style === "Aggressive"
  ).length

  const positional = games.filter(
    game => game.predicted_style === "Positional"
  ).length

  totalGames.value = games.length

  if (totalGames.value > 0) {
    aggressivePercentage.value = Math.round(
      (aggressive / totalGames.value) * 100
    )

    positionalPercentage.value = Math.round(
      (positional / totalGames.value) * 100
    )
  }

  // WIN / LOSS / DRAW
  wins.value = 0
  losses.value = 0
  draws.value = 0

  const chessUsername = "super-wingwing"

  games.forEach(game => {
    const white = game.white?.trim()
    const black = game.black?.trim()
    const result = game.result

    // Draw
    if (result === "1/2-1/2") {
      draws.value++
      return
    }

    // You are White
    if (white === chessUsername) {
      if (result === "1-0") {
        wins.value++
      } else if (result === "0-1") {
        losses.value++
      }
    }

    // You are Black
    else if (black === chessUsername) {
      if (result === "0-1") {
        wins.value++
      } else if (result === "1-0") {
        losses.value++
      }
    }
  })
}

const statistics = [
  {
    label: "Games Analyzed",
    value: totalGames,
    icon: "mdi-chess-pawn",
    class: "games"
  },
  {
    label: "Wins",
    value: wins,
    icon: "mdi-trophy-outline",
    class: "wins"
  },
  {
    label: "Losses",
    value: losses,
    icon: "mdi-chart-line",
    class: "losses"
  },
  {
    label: "Draws",
    value: draws,
    icon: "mdi-equal",
    class: "draws"
  }
]

const styleDescription =
  "Your games show a strong preference for active and attacking positions, including king pressure, tactical opportunities, and active piece coordination."

const styleFeatures = [
  "King Attacks",
  "Tactical Play",
  "Active Pieces",
  "Sacrifices"
]

const editDialog = ref(false)

const editForm = reactive({
  username: profile.username,
  email: profile.email
})

function editProfile() {
  editForm.username = profile.username
  editForm.email = profile.email
  editDialog.value = true
}

function saveProfile() {
  profile.username = editForm.username
  profile.email = editForm.email
  editDialog.value = false
}

function changePassword() {
  console.log("Change password")
}

function signOut() {
  console.log("Sign out")
}

onMounted(() => {
  loadStylePercentages()
})
</script>

<template>
  <v-container fluid class="profile-page pa-0">

    <!-- =========================================================
         PROFILE HERO
    ========================================================== -->
    <section class="profile-hero">

      <div class="hero-pattern"></div>

      <div class="hero-content">

        <div class="hero-top">
          <div>
            <div class="hero-eyebrow">
              <v-icon size="15">mdi-chess-queen</v-icon>
              CHESSKWEEN PROFILE
            </div>

            <h1 class="hero-title">
              Player Profile
            </h1>

            <p class="hero-subtitle">
              Your chess identity, statistics, and playing style.
            </p>
          </div>
        </div>

        <div class="profile-identity">

          <div class="avatar-wrapper">
            <v-avatar
              size="104"
              class="profile-avatar"
            >
              <v-img
                v-if="profile.avatar"
                :src="profile.avatar"
                cover
              />

              <span
                v-else
                class="avatar-letter"
              >
                {{ profile.username.charAt(0).toUpperCase() }}
              </span>
            </v-avatar>

            <span class="online-indicator"></span>
          </div>

          <div class="identity-details">

            <div class="identity-label">
              CHESSKWEEN USER
            </div>

            <h2 class="identity-name">
              {{ authStore.user?.user_metadata?.username }}
            </h2>

            <div class="identity-email">
              <v-icon size="16">
                mdi-email-outline
              </v-icon>

              {{ profile.email }}
            </div>

            <div class="identity-meta">
              <span>
                <v-icon size="15">
                  mdi-calendar-outline
                </v-icon>

                Member since {{ profile.memberSince }}
              </span>

              <span>
                <v-icon size="15">
                  mdi-chess-pawn
                </v-icon>

                Chess Player
              </span>
            </div>
          </div>

          <div class="identity-action">
            <v-btn
              class="edit-profile-btn"
              rounded="lg"
              elevation="0"
              @click="editProfile"
            >
              <v-icon start>
                mdi-pencil-outline
              </v-icon>

              Edit Profile
            </v-btn>
          </div>

        </div>
      </div>
    </section>


    <!-- =========================================================
         STATISTICS
    ========================================================== -->
    <section class="stats-wrapper">

      <v-row class="stats-row">

        <v-col
          v-for="stat in statistics"
          :key="stat.label"
          cols="6"
          md="3"
        >

          <div
            class="stat-card"
            :class="`stat-${stat.class}`"
          >

            <div class="stat-icon">
              <v-icon size="23">
                {{ stat.icon }}
              </v-icon>
            </div>

            <div class="stat-content">
              <div class="stat-value">
                {{ stat.value }}
              </div>

              <div class="stat-label">
                {{ stat.label }}
              </div>
            </div>

          </div>

        </v-col>

      </v-row>
    </section>


    <!-- =========================================================
         MAIN CONTENT
    ========================================================== -->
    <section class="content-wrapper">

      <v-row>

        <!-- USER INFORMATION -->
        <v-col
          cols="12"
          lg="5"
        >

          <v-card
            class="dashboard-card information-card"
            elevation="0"
          >

            <div class="card-heading">

              <div class="heading-icon navy-icon">
                <v-icon>
                  mdi-account-outline
                </v-icon>
              </div>

              <div>
                <h3>
                  User Information
                </h3>

                <p>
                  Your ChessKween account details
                </p>
              </div>

            </div>

            <div class="information-list">

              <div class="information-item">

                <div class="information-icon">
                  <v-icon>
                    mdi-account-outline
                  </v-icon>
                </div>

                <div class="information-content">
                  <span>
                    Username
                  </span>

                  <strong>
                    {{ profile.username }}
                  </strong>
                </div>

              </div>


              <div class="information-item">

                <div class="information-icon">
                  <v-icon>
                    mdi-email-outline
                  </v-icon>
                </div>

                <div class="information-content">
                  <span>
                    Email
                  </span>

                  <strong>
                    {{ profile.email }}
                  </strong>
                </div>

              </div>


              <div class="information-item">

                <div class="information-icon">
                  <v-icon>
                    mdi-calendar-outline
                  </v-icon>
                </div>

                <div class="information-content">
                  <span>
                    Member Since
                  </span>

                  <strong>
                    {{ profile.memberSince }}
                  </strong>
                </div>

              </div>


              <div class="information-item">

                <div class="information-icon orange-icon">
                  <v-icon>
                    mdi-chess-pawn
                  </v-icon>
                </div>

                <div class="information-content">

                  <span>
                    Preferred Style
                  </span>

                  <strong>
                    {{ aggressivePercentage }}% Aggressive,
                    {{ positionalPercentage }}% Positional
                  </strong>

                </div>

              </div>

            </div>

          </v-card>

        </v-col>


        <!-- PLAYING STYLE -->
        <v-col
          cols="12"
          lg="7"
        >

          <v-card
            class="dashboard-card style-card"
            elevation="0"
          >

            <div class="card-heading">

              <div class="heading-icon orange-icon">
                <v-icon>
                  mdi-chess-queen
                </v-icon>
              </div>

              <div>
                <h3>
                  Playing Style
                </h3>

                <p>
                  Your chess style distribution
                </p>
              </div>

              <v-spacer />

              <div class="games-count">
                <strong>
                  {{ totalGames }}
                </strong>

                <span>
                  Games
                </span>
              </div>

            </div>


            <div class="style-distribution">

              <!-- AGGRESSIVE -->
              <div class="style-row">

                <div class="style-row-top">

                  <div class="style-label">

                    <span class="style-dot aggressive-dot"></span>

                    <span>
                      Aggressive
                    </span>

                  </div>

                  <strong>
                    {{ aggressivePercentage }}%
                  </strong>

                </div>

                <div class="style-track">
                  <div
                    class="style-fill aggressive-fill"
                    :style="{
                      width: `${aggressivePercentage}%`
                    }"
                  ></div>
                </div>

              </div>


              <!-- POSITIONAL -->
              <div class="style-row">

                <div class="style-row-top">

                  <div class="style-label">

                    <span class="style-dot positional-dot"></span>

                    <span>
                      Positional
                    </span>

                  </div>

                  <strong>
                    {{ positionalPercentage }}%
                  </strong>

                </div>

                <div class="style-track">
                  <div
                    class="style-fill positional-fill"
                    :style="{
                      width: `${positionalPercentage}%`
                    }"
                  ></div>
                </div>

              </div>

            </div>


            <div class="style-description-box">

              <div class="description-icon">
                <v-icon size="20">
                  mdi-lightbulb-outline
                </v-icon>
              </div>

              <p>
                {{ styleDescription }}
              </p>

            </div>


            <div class="characteristics">

              <div class="characteristics-title">
                Dominant Characteristics
              </div>

              <div class="characteristics-list">

                <div
                  v-for="feature in styleFeatures"
                  :key="feature"
                  class="characteristic"
                >
                  <v-icon size="16">
                    mdi-check
                  </v-icon>

                  {{ feature }}
                </div>

              </div>

            </div>

          </v-card>

        </v-col>

      </v-row>


      <!-- =======================================================
           RECENT GAMES
      ======================================================== -->
      <div class="section-block">

        <div class="section-header">

          <div>
            <div class="section-eyebrow">
              GAME ACTIVITY
            </div>

            <h2>
              Recent Games
            </h2>

            <p>
              Review your latest analyzed chess games.
            </p>
          </div>

        </div>

        <div class="recent-games-wrapper">
          <RecentGames />
        </div>

      </div>


      <!-- =======================================================
           ACCOUNT
      ======================================================== -->
      <div class="section-block account-section">

        <div class="section-header">

          <div>
            <div class="section-eyebrow">
              ACCOUNT
            </div>

            <h2>
              Account & Security
            </h2>

            <p>
              Manage your ChessKween account.
            </p>
          </div>

        </div>


        <v-card
          class="dashboard-card account-card"
          elevation="0"
        >

          <div
            class="account-item"
            @click="changePassword"
          >

            <div class="account-left">

              <div class="account-icon">
                <v-icon>
                  mdi-lock-outline
                </v-icon>
              </div>

              <div>
                <strong>
                  Change Password
                </strong>

                <span>
                  Update your account password
                </span>
              </div>

            </div>

            <v-icon class="account-arrow">
              mdi-chevron-right
            </v-icon>

          </div>


          <div class="account-divider"></div>


          <div
            class="account-item logout-item"
            @click="signOut"
          >

            <div class="account-left">

              <div class="account-icon logout-icon">
                <v-icon>
                  mdi-logout
                </v-icon>
              </div>

              <div>
                <strong>
                  Sign Out
                </strong>

                <span>
                  Sign out of your ChessKween account
                </span>
              </div>

            </div>

            <v-icon class="account-arrow">
              mdi-chevron-right
            </v-icon>

          </div>

        </v-card>

      </div>

    </section>


    <!-- =========================================================
         EDIT PROFILE DIALOG
    ========================================================== -->
    <v-dialog
      v-model="editDialog"
      max-width="500"
    >

      <v-card
        class="edit-dialog"
        rounded="xl"
      >

        <div class="dialog-header">

          <div class="dialog-icon">
            <v-icon>
              mdi-account-edit-outline
            </v-icon>
          </div>

          <div>
            <h3>
              Edit Profile
            </h3>

            <p>
              Update your profile information.
            </p>
          </div>

        </div>


        <v-card-text class="dialog-content">

          <v-text-field
            v-model="editForm.username"
            label="Username"
            variant="outlined"
            rounded="lg"
            prepend-inner-icon="mdi-account-outline"
            class="dialog-field"
          />

          <v-text-field
            v-model="editForm.email"
            label="Email"
            variant="outlined"
            rounded="lg"
            type="email"
            prepend-inner-icon="mdi-email-outline"
            class="dialog-field"
          />

        </v-card-text>


        <v-card-actions class="dialog-actions">

          <v-btn
            variant="text"
            class="cancel-btn"
            @click="editDialog = false"
          >
            Cancel
          </v-btn>

          <v-btn
            class="save-btn"
            rounded="lg"
            elevation="0"
            @click="saveProfile"
          >
            <v-icon start>
              mdi-check
            </v-icon>

            Save Changes
          </v-btn>

        </v-card-actions>

      </v-card>

    </v-dialog>

  </v-container>
</template>


<style scoped>

/* =========================================================
   COLOR SYSTEM
========================================================= */

.profile-page {
  --navy: #0b1f3a;
  --navy-dark: #07172d;
  --navy-light: #17345a;

  --orange: #f28c28;
  --orange-dark: #dc7311;
  --orange-soft: #fff3e4;

  --white: #ffffff;
  --background: #f5f7fa;

  --text: #172033;
  --muted: #718096;

  --border: #e5e9ef;

  min-height: 100vh;
  background: var(--background);
  color: var(--text);
}


/* =========================================================
   HERO
========================================================= */

.profile-hero {
  position: relative;
  overflow: hidden;

  background:
    linear-gradient(
      135deg,
      var(--navy-dark) 0%,
      var(--navy) 55%,
      #123158 100%
    );

  color: white;
}

.hero-pattern {
  position: absolute;
  inset: 0;

  opacity: 0.07;

  background-image:
    linear-gradient(
      45deg,
      transparent 25%,
      rgba(255,255,255,.3) 25%,
      rgba(255,255,255,.3) 50%,
      transparent 50%,
      transparent 75%,
      rgba(255,255,255,.3) 75%
    );

  background-size: 70px 70px;

  pointer-events: none;
}

.hero-content {
  position: relative;
  z-index: 1;

  width: min(1180px, calc(100% - 40px));
  margin: auto;

  padding: 46px 0 64px;
}

.hero-eyebrow {
  display: flex;
  align-items: center;
  gap: 8px;

  margin-bottom: 8px;

  color: #ffb35c;

  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.14em;
}

.hero-title {
  margin: 0;

  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 800;
  letter-spacing: -0.03em;
}

.hero-subtitle {
  margin: 7px 0 0;

  color: rgba(255,255,255,.66);

  font-size: 0.95rem;
}

.profile-identity {
  display: flex;
  align-items: center;

  gap: 24px;

  margin-top: 38px;
}

.avatar-wrapper {
  position: relative;
  flex-shrink: 0;
}

.profile-avatar {
  background: var(--orange);

  border: 4px solid rgba(255,255,255,.15);
  box-shadow:
    0 0 0 5px rgba(242,140,40,.25),
    0 12px 30px rgba(0,0,0,.25);
}

.avatar-letter {
  color: white;

  font-size: 2.4rem;
  font-weight: 800;
}

.online-indicator {
  position: absolute;

  right: 5px;
  bottom: 6px;

  width: 15px;
  height: 15px;

  border-radius: 50%;

  background: #43c47a;

  border: 3px solid var(--navy);
}

.identity-details {
  min-width: 0;
}

.identity-label {
  color: #ffb35c;

  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.12em;
}

.identity-name {
  margin: 4px 0;

  color: white;

  font-size: clamp(1.7rem, 3vw, 2.35rem);
  font-weight: 800;
}

.identity-email {
  display: flex;
  align-items: center;
  gap: 7px;

  color: rgba(255,255,255,.68);

  font-size: 0.9rem;
}

.identity-meta {
  display: flex;
  flex-wrap: wrap;

  gap: 18px;

  margin-top: 12px;

  color: rgba(255,255,255,.58);

  font-size: 0.78rem;
}

.identity-meta span {
  display: flex;
  align-items: center;
  gap: 6px;
}

.identity-action {
  margin-left: auto;
}

.edit-profile-btn {
  min-width: 145px;

  background: var(--orange) !important;

  color: white !important;

  font-weight: 700;

  box-shadow: 0 8px 20px rgba(242,140,40,.22);
}

.edit-profile-btn:hover {
  background: var(--orange-dark) !important;
}


/* =========================================================
   STATISTICS
========================================================= */

.stats-wrapper {
  position: relative;
  z-index: 5;

  width: min(1180px, calc(100% - 40px));

  margin: -35px auto 0;
}

.stats-row {
  margin: 0 -8px;
}

.stats-row > .v-col {
  padding: 8px;
}

.stat-card {
  display: flex;
  align-items: center;

  gap: 15px;

  min-height: 105px;

  padding: 20px;

  background: white;

  border: 1px solid var(--border);
  border-radius: 15px;

  box-shadow: 0 10px 30px rgba(11,31,58,.08);

  transition:
    transform .2s ease,
    box-shadow .2s ease;
}

.stat-card:hover {
  transform: translateY(-3px);

  box-shadow: 0 15px 35px rgba(11,31,58,.12);
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 47px;
  height: 47px;

  flex-shrink: 0;

  border-radius: 12px;

  background: #edf2f7;

  color: var(--navy);
}

.stat-wins .stat-icon {
  background: var(--orange-soft);
  color: var(--orange-dark);
}

.stat-content {
  min-width: 0;
}

.stat-value {
  color: var(--navy);

  font-size: 1.65rem;
  font-weight: 800;

  line-height: 1;
}

.stat-label {
  margin-top: 6px;

  color: var(--muted);

  font-size: 0.72rem;
  font-weight: 700;
}


/* =========================================================
   MAIN CONTENT
========================================================= */

.content-wrapper {
  width: min(1180px, calc(100% - 40px));

  margin: 35px auto 60px;
}

.dashboard-card {
  height: 100%;

  padding: 28px;

  background: white !important;

  border: 1px solid var(--border) !important;
  border-radius: 17px !important;

  box-shadow: 0 5px 20px rgba(11,31,58,.045) !important;
}

.card-heading {
  display: flex;
  align-items: center;

  gap: 13px;

  margin-bottom: 24px;
}

.heading-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 43px;
  height: 43px;

  flex-shrink: 0;

  border-radius: 11px;
}

.navy-icon {
  background: #edf2f7;
  color: var(--navy);
}

.orange-icon {
  background: var(--orange-soft);
  color: var(--orange-dark);
}

.card-heading h3 {
  margin: 0;

  color: var(--navy);

  font-size: 1.05rem;
  font-weight: 800;
}

.card-heading p {
  margin: 3px 0 0;

  color: var(--muted);

  font-size: 0.76rem;
}


/* =========================================================
   INFORMATION
========================================================= */

.information-list {
  display: flex;
  flex-direction: column;

  gap: 5px;
}

.information-item {
  display: flex;
  align-items: center;

  gap: 13px;

  padding: 13px 8px;

  border-radius: 11px;

  transition: background .2s ease;
}

.information-item:hover {
  background: #f7f9fb;
}

.information-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 38px;
  height: 38px;

  flex-shrink: 0;

  border-radius: 9px;

  background: #f1f4f8;

  color: var(--navy);
}

.information-content {
  display: flex;
  flex-direction: column;

  min-width: 0;
}

.information-content span {
  color: var(--muted);

  font-size: 0.68rem;
  font-weight: 700;

  text-transform: uppercase;
  letter-spacing: .04em;
}

.information-content strong {
  margin-top: 2px;

  color: var(--text);

  font-size: 0.88rem;
  font-weight: 700;

  overflow-wrap: anywhere;
}

.orange-icon {
  background: var(--orange-soft);
  color: var(--orange-dark);
}


/* =========================================================
   PLAYING STYLE
========================================================= */

.games-count {
  display: flex;
  flex-direction: column;

  align-items: flex-end;
}

.games-count strong {
  color: var(--navy);

  font-size: 1.25rem;
  font-weight: 800;
}

.games-count span {
  color: var(--muted);

  font-size: 0.65rem;
  font-weight: 700;

  text-transform: uppercase;
}

.style-distribution {
  display: flex;
  flex-direction: column;

  gap: 21px;
}

.style-row-top {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-bottom: 8px;

  font-size: 0.83rem;
  font-weight: 700;
}

.style-row-top strong {
  color: var(--navy);
}

.style-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.style-dot {
  width: 8px;
  height: 8px;

  border-radius: 50%;
}

.aggressive-dot {
  background: var(--orange);
}

.positional-dot {
  background: var(--navy);
}

.style-track {
  width: 100%;
  height: 8px;

  overflow: hidden;

  border-radius: 100px;

  background: #edf0f4;
}

.style-fill {
  height: 100%;

  border-radius: inherit;

  transition: width .6s ease;
}

.aggressive-fill {
  background: var(--orange);
}

.positional-fill {
  background: var(--navy);
}

.style-description-box {
  display: flex;
  gap: 12px;

  margin-top: 26px;
  padding: 15px;

  border-radius: 11px;

  background: #f7f9fb;

  border: 1px solid #edf0f3;
}

.description-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 34px;
  height: 34px;

  flex-shrink: 0;

  border-radius: 8px;

  background: var(--orange-soft);

  color: var(--orange-dark);
}

.style-description-box p {
  margin: 0;

  color: #697386;

  font-size: 0.78rem;
  line-height: 1.65;
}

.characteristics {
  margin-top: 25px;
}

.characteristics-title {
  margin-bottom: 11px;

  color: var(--navy);

  font-size: 0.75rem;
  font-weight: 800;

  text-transform: uppercase;
  letter-spacing: .05em;
}

.characteristics-list {
  display: flex;
  flex-wrap: wrap;

  gap: 8px;
}

.characteristic {
  display: flex;
  align-items: center;

  gap: 6px;

  padding: 7px 10px;

  border-radius: 8px;

  background: var(--orange-soft);

  color: #7a4a19;

  font-size: 0.7rem;
  font-weight: 700;
}

.characteristic .v-icon {
  color: var(--orange-dark);
}


/* =========================================================
   SECTIONS
========================================================= */

.section-block {
  margin-top: 38px;
}

.section-header {
  margin-bottom: 17px;
}

.section-eyebrow {
  margin-bottom: 4px;

  color: var(--orange-dark);

  font-size: 0.65rem;
  font-weight: 800;

  letter-spacing: .12em;
}

.section-header h2 {
  margin: 0;

  color: var(--navy);

  font-size: 1.35rem;
  font-weight: 800;
}

.section-header p {
  margin: 4px 0 0;

  color: var(--muted);

  font-size: 0.78rem;
}

.recent-games-wrapper {
  overflow: hidden;

  background: white;

  border: 1px solid var(--border);
  border-radius: 17px;

  box-shadow: 0 5px 20px rgba(11,31,58,.045);
}


/* =========================================================
   ACCOUNT
========================================================= */

.account-card {
  padding: 0 !important;
}

.account-item {
  display: flex;
  align-items: center;
  justify-content: space-between;

  padding: 18px 22px;

  cursor: pointer;

  transition: background .2s ease;
}

.account-item:hover {
  background: #f8fafc;
}

.account-left {
  display: flex;
  align-items: center;

  gap: 14px;
}

.account-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 42px;
  height: 42px;

  border-radius: 10px;

  background: #edf2f7;

  color: var(--navy);
}

.account-left > div:last-child {
  display: flex;
  flex-direction: column;
}

.account-left strong {
  color: var(--text);

  font-size: 0.85rem;
}

.account-left span {
  margin-top: 3px;

  color: var(--muted);

  font-size: 0.72rem;
}

.account-arrow {
  color: #a2aab7;
}

.account-divider {
  height: 1px;

  margin: 0 22px;

  background: var(--border);
}

.logout-icon {
  background: #fff1ed;
  color: #c75b45;
}


/* =========================================================
   EDIT DIALOG
========================================================= */

.edit-dialog {
  overflow: hidden;
}

.dialog-header {
  display: flex;
  align-items: center;

  gap: 13px;

  padding: 24px 24px 18px;

  background: var(--navy);

  color: white;
}

.dialog-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 42px;
  height: 42px;

  border-radius: 10px;

  background: rgba(242,140,40,.15);

  color: #ffad55;
}

.dialog-header h3 {
  margin: 0;

  font-size: 1.15rem;
  font-weight: 800;
}

.dialog-header p {
  margin: 3px 0 0;

  color: rgba(255,255,255,.6);

  font-size: 0.72rem;
}

.dialog-content {
  padding: 25px 24px 8px !important;
}

.dialog-field {
  margin-bottom: 8px;
}

.dialog-actions {
  justify-content: flex-end;

  gap: 8px;

  padding: 10px 24px 24px !important;
}

.cancel-btn {
  color: var(--muted);
}

.save-btn {
  background: var(--orange) !important;

  color: white !important;

  font-weight: 700;
}

.save-btn:hover {
  background: var(--orange-dark) !important;
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 960px) {

  .hero-content {
    padding: 38px 0 60px;
  }

  .profile-identity {
    align-items: flex-start;
    flex-wrap: wrap;
  }

  .identity-action {
    width: 100%;

    margin-left: 0;
  }

  .edit-profile-btn {
    width: 100%;
  }
}


@media (max-width: 600px) {

  .hero-content,
  .stats-wrapper,
  .content-wrapper {
    width: calc(100% - 24px);
  }

  .hero-content {
    padding: 30px 0 55px;
  }

  .hero-title {
    font-size: 2rem;
  }

  .profile-identity {
    gap: 16px;

    margin-top: 28px;
  }

  .profile-avatar {
    width: 82px !important;
    height: 82px !important;
  }

  .avatar-letter {
    font-size: 1.9rem;
  }

  .identity-name {
    font-size: 1.55rem;
  }

  .identity-meta {
    flex-direction: column;

    gap: 6px;
  }

  .stats-wrapper {
    margin-top: -25px;
  }

  .stat-card {
    min-height: 88px;

    padding: 14px;

    gap: 10px;
  }

  .stat-icon {
    width: 39px;
    height: 39px;
  }

  .stat-value {
    font-size: 1.35rem;
  }

  .stat-label {
    font-size: 0.63rem;
  }

  .content-wrapper {
    margin-top: 25px;
  }

  .dashboard-card {
    padding: 21px;
  }

  .card-heading {
    margin-bottom: 18px;
  }

  .games-count {
    display: none;
  }

  .section-block {
    margin-top: 30px;
  }

  .account-item {
    padding: 16px;
  }

  .account-divider {
    margin: 0 16px;
  }
}

</style>