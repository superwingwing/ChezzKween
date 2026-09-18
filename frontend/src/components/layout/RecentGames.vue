<script setup>
import { ref, onMounted } from "vue"
import { supabase } from "@/utils/supabase"

const recentGames = ref([])

const loadRecentGames = async () => {
  const {
    data: { user }
  } = await supabase.auth.getUser()

  if (!user) return

  const { data, error } = await supabase
    .from("review_games")
    .select("*")
    .eq("user_id", user.id)
    .order("created_at", { ascending: false })
    .limit(4)

  if (error) {
    console.error("Failed to load recent games:", error)
    return
  }

  recentGames.value = data
}

const resultColor = (result) => {
  if (result === "1-0") return "success"
  if (result === "0-1") return "error"
  if (result === "1/2-1/2") return "warning"

  return "grey"
}

const resultText = (result) => {
  if (result === "1-0") return "Win"
  if (result === "0-1") return "Loss"
  if (result === "1/2-1/2") return "Draw"

  return result
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric"
  })
}

const viewGame = (game) => {
  console.log("View game:", game.id)

  // We can connect this to your game analysis page next.
}

onMounted(() => {
  loadRecentGames()
})
</script>

<template>
  <!-- Recent Games -->
  <v-card
    rounded="xl"
    elevation="1"
    class="content-card mt-6"
  >
    <v-card-item>
      <v-card-title class="card-title">
        Recent Games
      </v-card-title>

      <v-card-subtitle>
        Your recently analyzed chess games
      </v-card-subtitle>
    </v-card-item>

    <v-divider />

    <v-table class="games-table">
      <thead>
        <tr>
          <th>Opponent</th>

          <th class="d-none d-sm-table-cell">
            Result
          </th>

          <th class="d-none d-md-table-cell">
            Date
          </th>

          <th class="text-end">
            Action
          </th>
        </tr>
      </thead>

      <tbody>

        <tr
          v-for="game in recentGames"
          :key="game.id"
        >
          <td>
            <div class="opponent-cell">

              <v-avatar
                size="34"
                color="surface-variant"
              >
                <v-icon size="18">
                  mdi-account
                </v-icon>
              </v-avatar>

              <span>
                {{ game.white_name }} vs {{ game.black_name }}
              </span>

            </div>
          </td>

          <td class="d-none d-sm-table-cell">
            <v-chip
              :color="resultColor(game.result)"
              size="small"
              variant="tonal"
            >
              {{ resultText(game.result) }}
            </v-chip>
          </td>

          <td class="d-none d-md-table-cell">
            {{ formatDate(game.created_at) }}
          </td>

          <td class="text-end">

            <v-btn
              variant="text"
              size="small"
              color="primary"
              @click="viewGame(game)"
            >
              View Game

              <v-icon end>
                mdi-arrow-right
              </v-icon>
            </v-btn>

          </td>
        </tr>

        <tr v-if="recentGames.length === 0">
          <td
            colspan="4"
            class="text-center py-6"
          >
            No analyzed games yet.
          </td>
        </tr>

      </tbody>
    </v-table>

    <v-card-actions class="pa-4">
      <v-spacer />

      <v-btn
        variant="text"
        color="primary"
      >
        View All Games

        <v-icon end>
          mdi-arrow-right
        </v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>