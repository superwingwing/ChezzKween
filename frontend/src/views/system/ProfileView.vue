<script setup>
    import { ref, reactive, onMounted, computed } from "vue"
    import { useAuthStore } from "@/stores/authUser"
    import { supabase } from "@/utils/supabase"
    import RecentGames from '@/components/layout/RecentGames.vue'

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

        //come from  the data in authuser.js
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

          const aggressive = data.filter(
            game => game.predicted_style === "Aggressive"
          ).length

          const positional = data.filter(
            game => game.predicted_style === "Positional"
          ).length

          totalGames.value = data.length

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

            data.forEach(game => {

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
        icon: "mdi-chess-pawn"
      },
      {
        label: "Wins",
        value: wins,
        icon: "mdi-trophy-outline"
      },
      {
        label: "Losses",
        value: losses,
        icon: "mdi-chart-line"
      },
      {
        label: "Draws",
        value: draws,
        icon: "mdi-equal"
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
  <v-container fluid class="profile-page py-8">
    <v-row justify="center">
      <v-col cols="12" xl="10">

        <!-- Profile Header -->
        <v-card rounded="xl" elevation="1" class="profile-header mb-6">
          <v-card-text class="pa-6 pa-md-8">
            <v-row align="center">

              <v-col cols="12" sm="auto" class="text-center">
                <v-avatar
                  size="120"
                  color="primary"
                  class="profile-avatar"
                >
                  <v-img
                    v-if="profile.avatar"
                    :src="profile.avatar"
                    cover
                  />
                  <span v-else class="avatar-letter">
                    {{ profile.username.charAt(0).toUpperCase() }}
                  </span>
                </v-avatar>
              </v-col>

              <v-col cols="12" sm>
                <div class="text-center text-sm-start">
                  <div class="profile-label">
                    CHESSKWEEN USER
                  </div>

                  <h1 class="profile-name">
                    {{ authStore.user?.user_metadata?.username }}
                  </h1>

                  <p class="profile-email">
                    {{ profile.email }}
                  </p>
                </div>
              </v-col>

              <v-col cols="12" sm="auto" class="text-center">
                <v-btn
                  variant="outlined"
                  color="primary"
                  rounded="lg"
                  @click="editProfile"
                >
                  <v-icon start>
                    mdi-pencil-outline
                  </v-icon>
                  Edit Profile
                </v-btn>
              </v-col>

            </v-row>
          </v-card-text>
        </v-card>

        <!-- Statistics -->
        <v-row class="mb-2">
          <v-col
            v-for="stat in statistics"
            :key="stat.label"
            cols="6"
            sm="3"
          >
            <v-card
              rounded="xl"
              elevation="1"
              class="stat-card h-100"
            >
              <v-card-text class="pa-5 text-center">
                <v-icon
                  size="30"
                  color="primary"
                  class="mb-3"
                >
                  {{ stat.icon }}
                </v-icon>

                <div class="stat-value">
                  {{ stat.value }}
                </div>

                <div class="stat-label">
                  {{ stat.label }}
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Main Content -->
        <v-row>

          <!-- User Information -->
          <v-col cols="12" md="6">
            <v-card
              rounded="xl"
              elevation="1"
              class="content-card h-100"
            >
              <v-card-item>
                <v-card-title class="card-title">
                  User Information
                </v-card-title>
              </v-card-item>

              <v-divider />

              <v-list lines="two">
                <v-list-item>
                  <template #prepend>
                    <v-avatar
                      color="primary"
                      variant="tonal"
                      size="42"
                    >
                      <v-icon>mdi-account-outline</v-icon>
                    </v-avatar>
                  </template>

                  <v-list-item-title>
                    Username
                  </v-list-item-title>

                  <v-list-item-subtitle>
                    {{ profile.username }}
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template #prepend>
                    <v-avatar
                      color="primary"
                      variant="tonal"
                      size="42"
                    >
                      <v-icon>mdi-email-outline</v-icon>
                    </v-avatar>
                  </template>

                  <v-list-item-title>
                    Email
                  </v-list-item-title>

                  <v-list-item-subtitle>
                    {{ profile.email }}
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template #prepend>
                    <v-avatar
                      color="primary"
                      variant="tonal"
                      size="42"
                    >
                      <v-icon>mdi-calendar-outline</v-icon>
                    </v-avatar>
                  </template>

                  <v-list-item-title>
                    Member Since
                  </v-list-item-title>

                  <v-list-item-subtitle>
                    {{ profile.memberSince }}
                  </v-list-item-subtitle>
                </v-list-item>

                <v-list-item>
                  <template #prepend>
                    <v-avatar
                      color="primary"
                      variant="tonal"
                      size="42"
                    >
                      <v-icon>mdi-chess-pawn</v-icon>
                    </v-avatar>
                  </template>

                  <v-list-item-title>
                    Preferred Style
                  </v-list-item-title>

                  <v-list-item-subtitle>
                    {{ aggressivePercentage }}% Aggressive, {{ positionalPercentage }}% Positional
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>

          <!-- Playing Style -->
          <v-col cols="12" md="6">
            <v-card
              rounded="xl"
              elevation="1"
              class="content-card h-100"
            >
              <v-card-item>
                <v-card-title class="card-title">
                  Playing Style
                </v-card-title>
              </v-card-item>

              <v-divider />

              <v-card-text class="pa-6">

                
        <div class="style-header">
  <v-avatar
    color="primary"
    variant="tonal"
    size="58"
  >
    <v-icon size="30">
      mdi-chess-queen
    </v-icon>
  </v-avatar>

  <div>
    <div class="style-name">
      Playing Style Distribution
    </div>

    <div class="style-confidence">
      Based on {{ totalGames }} games
    </div>
  </div>
</div>

<!-- Aggressive -->
<div class="mt-6">
  <div class="d-flex justify-space-between mb-2">
    <span>Aggressive</span>
    <strong>{{ aggressivePercentage }}%</strong>
  </div>

  <v-progress-linear
    :model-value="aggressivePercentage"
    color="primary"
    height="8"
    rounded
  />
</div>

<!-- Positional -->
<div class="mt-5">
  <div class="d-flex justify-space-between mb-2">
    <span>Positional</span>
    <strong>{{ positionalPercentage }}%</strong>
  </div>

  <v-progress-linear
    :model-value="positionalPercentage"
    color="primary"
    height="8"
    rounded
  />
</div>
                
              <br>  
                <p class="style-description">
                  {{ styleDescription }}
                </p>

                <div class="mt-5">
                  <div class="feature-heading mb-3">
                    Dominant Characteristics
                  </div>

                  <div class="d-flex flex-wrap ga-2">
                    <v-chip
                      v-for="feature in styleFeatures"
                      :key="feature"
                      size="small"
                      variant="tonal"
                      color="primary"
                    >
                      {{ feature }}
                    </v-chip>
                  </div>
                </div>

              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

     <!-- Other profile content -->
          <RecentGames />

        <!-- Account Actions -->
        <v-card
          rounded="xl"
          elevation="1"
          class="content-card mt-6"
        >
          <v-card-item>
            <v-card-title class="card-title">
              Account
            </v-card-title>
          </v-card-item>

          <v-divider />

          <v-list>
            <v-list-item
              prepend-icon="mdi-lock-outline"
              title="Change Password"
              subtitle="Update your account password"
              @click="changePassword"
            >
              <template #append>
                <v-icon>
                  mdi-chevron-right
                </v-icon>
              </template>
            </v-list-item>

            <v-list-item
              prepend-icon="mdi-logout"
              title="Sign Out"
              subtitle="Sign out of your ChessKween account"
              @click="signOut"
            >
              <template #append>
                <v-icon>
                  mdi-chevron-right
                </v-icon>
              </template>
            </v-list-item>
          </v-list>
        </v-card>

      </v-col>
    </v-row>

    <!-- Edit Profile Dialog -->
    <v-dialog
      v-model="editDialog"
      max-width="500"
    >
      <v-card rounded="xl">
        <v-card-title class="pa-6">
          Edit Profile
        </v-card-title>

        <v-card-text class="px-6">
          <v-text-field
            v-model="editForm.username"
            label="Username"
            variant="outlined"
            rounded="lg"
            class="mb-2"
          />

          <v-text-field
            v-model="editForm.email"
            label="Email"
            variant="outlined"
            rounded="lg"
            type="email"
          />
        </v-card-text>

        <v-card-actions class="pa-6 pt-0">
          <v-spacer />

          <v-btn
            variant="text"
            @click="editDialog = false"
          >
            Cancel
          </v-btn>

          <v-btn
            color="primary"
            variant="flat"
            rounded="lg"
            @click="saveProfile"
          >
            Save Changes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>



<style scoped>
.profile-page {
  min-height: 100vh;
}

.profile-header,
.content-card,
.stat-card {
  border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

.profile-header {
  background: linear-gradient(
    135deg,
    rgba(var(--v-theme-primary), 0.08),
    rgba(var(--v-theme-primary), 0.02)
  );
}

.profile-avatar {
  border: 4px solid rgba(var(--v-theme-primary), 0.15);
}

.avatar-letter {
  color: white;
  font-size: 2.5rem;
  font-weight: 700;
}

.profile-label {
  color: rgb(var(--v-theme-primary));
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
}

.profile-name {
  margin: 4px 0;
  font-size: clamp(1.8rem, 4vw, 2.5rem);
  font-weight: 800;
}

.profile-email {
  margin: 0;
  color: rgba(var(--v-theme-on-surface), 0.6);
}

.stat-card {
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-value {
  font-size: 1.6rem;
  font-weight: 800;
}

.stat-label {
  margin-top: 3px;
  font-size: 0.78rem;
  color: rgba(var(--v-theme-on-surface), 0.6);
}

.card-title {
  font-size: 1.2rem;
  font-weight: 700;
}

.style-header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.style-name {
  font-size: 1.25rem;
  font-weight: 700;
}

.style-confidence {
  margin-top: 3px;
  font-size: 0.85rem;
  color: rgba(var(--v-theme-on-surface), 0.6);
}

.style-description {
  line-height: 1.7;
  color: rgba(var(--v-theme-on-surface), 0.65);
}

.feature-heading {
  font-size: 0.85rem;
  font-weight: 700;
}

.opponent-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.rating-positive {
  color: rgb(var(--v-theme-success));
  font-weight: 700;
}

.rating-negative {
  color: rgb(var(--v-theme-error));
  font-weight: 700;
}

.rating-neutral {
  color: rgba(var(--v-theme-on-surface), 0.6);
  font-weight: 700;
}

.games-table th {
  font-size: 0.78rem !important;
  font-weight: 700 !important;
}

.games-table td {
  height: 64px !important;
}

@media (max-width: 600px) {
  .profile-page {
    padding: 24px 12px !important;
  }

  .profile-name {
    font-size: 1.8rem;
  }

  .profile-header .v-btn {
    width: 100%;
  }

  .stat-value {
    font-size: 1.35rem;
  }

  .stat-label {
    font-size: 0.7rem;
  }

  .style-header {
    align-items: flex-start;
  }
}
</style>

