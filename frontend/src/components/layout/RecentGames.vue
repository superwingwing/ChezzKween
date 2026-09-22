<script setup>
      import { ref, onMounted, nextTick } from "vue"
      import { supabase } from "@/utils/supabase"
      import ChessboardView from "@/components/layout/ChessboardView.vue"

      const recentGames = ref([])
      const showGame = ref(false)
      const selectedGame = ref(null)
      const chessboardRef = ref(null)
      const loadingGameId = ref(null)

      // Usernames that should be recognized as you
      const myUsernames = ref([
        "super-wingwing"
      ])

      /*
      * Get the currently logged-in user's username
      * from Supabase Auth.
      */
      const loadMyUsername = async () => {
        const {
          data: { user }
        } = await supabase.auth.getUser()

        if (!user) return

        const actualUsername = user.user_metadata?.username

        const usernames = [
          "super-wingwing"
        ]

        if (actualUsername) {
          usernames.push(actualUsername)
        }

        myUsernames.value = [
          ...new Set(
            usernames
              .filter(Boolean)
              .map(username =>
                String(username).trim().toLowerCase()
              )
          )
        ]

        console.log("Recognized usernames:", myUsernames.value)
      }


      /*
      * Load recent games belonging to the
      * currently authenticated user.
      */
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

        recentGames.value = data || []
      }


      /*
      * Determine the result from YOUR perspective.
      */
      const getMyResult = (game) => {

        const white = String(game.white_name || game.white || "")
          .trim()
          .toLowerCase()

        const black = String(game.black_name || game.black || "")
          .trim()
          .toLowerCase()

        const result = String(game.result || "").trim()

        const amWhite = myUsernames.value.includes(white)
        const amBlack = myUsernames.value.includes(black)

        /*
        * Draw is always a draw.
        */
        if (result === "1/2-1/2") {
          return "Draw"
        }

        /*
        * I am White.
        */
        if (amWhite) {

          if (result === "1-0") {
            return "Win"
          }

          if (result === "0-1") {
            return "Loss"
          }
        }

        /*
        * I am Black.
        */
        if (amBlack) {

          if (result === "0-1") {
            return "Win"
          }

          if (result === "1-0") {
            return "Loss"
          }
        }

        /*
        * Username wasn't found.
        */
        return "Unknown"
      }


      /*
      * Result chip color.
      */
      const resultColor = (game) => {

        const result = getMyResult(game)

        if (result === "Win") {
          return "success"
        }

        if (result === "Loss") {
          return "error"
        }

        if (result === "Draw") {
          return "warning"
        }

        return "grey"
      }


      /*
      * Result text.
      */
      const resultText = (game) => {
        return getMyResult(game)
      }


      const formatDate = (date) => {
        return new Date(date).toLocaleDateString("en-US", {
          month: "short",
          day: "numeric",
          year: "numeric"
        })
      }


      /*
      * Open selected game.
      */
      const viewGame = async (game) => {
        try {
          loadingGameId.value = game.id

          const { data, error } = await supabase
            .from("game_analysis")
            .select("analysis_json")
            .eq("game_id", game.id)
            .single()

          if (error) {
            console.error("Failed to load game analysis:", error)
            return
          }

          selectedGame.value = game

          // Open dialog
          showGame.value = true

          // Wait until the dialog and ChessboardView are rendered
          await nextTick()

          // Give Vuetify time to finish the dialog transition/layout
          setTimeout(() => {
            if (chessboardRef.value) {
              chessboardRef.value.loadMoves({
                game: game,
                analysis: data.analysis_json
              })
            }
          }, 100)

        } catch (error) {
          console.error("Failed to open game:", error)

        } finally {
          loadingGameId.value = null
        }
      }


      const closeGame = () => {
        showGame.value = false
        selectedGame.value = null
      }


      /*
      * Load username first,
      * then load games.
      */
      onMounted(async () => {

        await loadMyUsername()

        await loadRecentGames()

      })
</script>


<template>
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

          <th>
            Opponent
          </th>

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
                <v-icon size="18" class="me-2">
                  mdi-file-document
                </v-icon> 

              <span class="game-names">
                {{ game.white_name }}
                vs
                {{ game.black_name }}
              </span>

            </div>

          </td>

          <td class="d-none d-sm-table-cell">

            <v-chip
              :color="resultColor(game)"
              size="small"
              variant="tonal"
            >
              {{ resultText(game) }}
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
              :loading="loadingGameId === game.id"
              :disabled="loadingGameId !== null"
              @click="viewGame(game)"
            >
              View Game

              <v-icon end>
                mdi-arrow-right
              </v-icon>

            </v-btn>

          </td>

        </tr>

        <!-- EMPTY STATE -->

        <tr v-if="recentGames.length === 0">

          <td
            colspan="4"
            class="text-center py-6"
          >

            <v-icon
              size="30"
              class="mb-2"
            >
              mdi-chess-queen
            </v-icon>

            <div>
              No analyzed games yet.
            </div>

          </td>

        </tr>

      </tbody>

    </v-table>

  </v-card>

          <!-- /// GAME VIEWER MODAL -->  
      <div v-if="showGame" class="game-overlay">
        <div class="game-modal">

          <v-btn
            class="close-btn"
            icon="mdi-close"
            size="40"
            variant="flat"
            @click="closeGame"
          />

          <ChessboardView
            ref="chessboardRef"
          />

        </div>
      </div>

</template>

<style scoped>

    .game-overlay {
      position: fixed;
      inset: 0;

      z-index: 9999;

      display: flex;
      justify-content: center;
      align-items: center;

      padding: 16px;

      background: rgba(0, 0, 0, 0.55);

      overflow-y: auto;
    }

    .game-modal {
      position: relative;

      width: 660px;
      max-width: calc(100vw - 32px);

      max-height: calc(100vh - 32px);

      overflow-y: auto;
      overflow-x: hidden;

      background: #ffffff;

      border-radius: 18px;

      box-shadow:
        0 24px 70px rgba(0, 0, 0, 0.30);

      box-sizing: border-box;

      padding: 0 20px 16px;
    }

    .close-btn {
      position: absolute !important;

      top: 12px;
      right: 12px;

      width: 42px !important;
      height: 42px !important;

      z-index: 10;

      background: #ffffff !important;
      color: #222222 !important;

      box-shadow:
        0 3px 12px rgba(0, 0, 0, 0.22);
    }

    @media (max-width: 600px) {

      .game-overlay {
        padding: 8px;
      }

      .game-modal {
        width: 100%;
        max-width: calc(100vw - 16px);

        max-height: calc(100vh - 16px);

        padding-left: 8px;
        padding-right: 8px;
        padding-bottom: 10px;

        border-radius: 12px;
      }

      .close-btn {
        top: 7px;
        right: 7px;

        width: 38px !important;
        height: 38px !important;
      }
    }

</style>