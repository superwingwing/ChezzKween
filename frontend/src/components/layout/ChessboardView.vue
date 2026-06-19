<script setup>
import { ref, onMounted } from "vue"
import { Chess } from "chess.js"
import "chessboard-element"

import { supabase } from "@/utils/supabase"
import UploadPGNModal from "@/components/layout/UploadPgnModal.vue"

const boardRef = ref(null)

const chess = new Chess()
const moves = ref([])
const moveIndex = ref(0)

const games = ref([])
const currentGame = ref(null)

// =====================
// BOARD
// =====================
function updateBoard() {
  boardRef.value?.setPosition(chess.fen())
}

function resetBoard() {
  chess.reset()
  moveIndex.value = 0
  updateBoard()
}

function nextMove() {
  if (moveIndex.value < moves.value.length) {
    chess.move(moves.value[moveIndex.value])
    moveIndex.value++
    updateBoard()
  }
}

function prevMove() {
  if (moveIndex.value > 0) {
    moveIndex.value--
    chess.reset()

    for (let i = 0; i < moveIndex.value; i++) {
      chess.move(moves.value[i])
    }

    updateBoard()
  }
}

// =====================
// PGN HELPERS
// =====================
function extractResult(pgn) {
  return pgn.match(/\[Result "(.*?)"\]/)?.[1] || null
}

function extractGameInfo(pgn) {
  return {
    white_name: pgn.match(/\[White "(.*?)"\]/)?.[1] || "White",
    black_name: pgn.match(/\[Black "(.*?)"\]/)?.[1] || "Black",

    white_elo: Number(pgn.match(/\[WhiteElo "(.*?)"\]/)?.[1]) || null,
    black_elo: Number(pgn.match(/\[BlackElo "(.*?)"\]/)?.[1]) || null,

    white_country: pgn.match(/\[WhiteCountry "(.*?)"\]/)?.[1] || null,
    black_country: pgn.match(/\[BlackCountry "(.*?)"\]/)?.[1] || null
  }
}

// =====================
// FROM UPLOAD MODAL
// =====================
async function loadMoves(newMoves, rawPGN) {
  try {
    moves.value = newMoves || []
    resetBoard()

    const info = extractGameInfo(rawPGN)

    const {
      data: { user }
    } = await supabase.auth.getUser()

    // 1. INSERT GAME
    const { data: inserted, error } = await supabase
      .from("uploaded_games")
      .insert([
        {
          user_id: user.id,
          pgn: rawPGN,
          result: extractResult(rawPGN),
          ...info
        }
      ])
      .select()
      .single()

    if (error) throw error

    // 2. SET CURRENT GAME (IMPORTANT FIX)
    currentGame.value = inserted

    // 3. REFRESH LIST
    await fetchGames()
  } catch (err) {
    console.error("Upload error:", err)
  }
}

// =====================
// LOAD FROM DATABASE
// =====================
function loadFromGame(game) {
  currentGame.value = game

  chess.reset()

  // IMPORTANT: load PGN properly
  chess.loadPgn(game.pgn)

  moves.value = chess.history()
  resetBoard()
}

// =====================
// FETCH GAMES
// =====================
async function fetchGames() {
  const {
    data: { user }
  } = await supabase.auth.getUser()

  const { data, error } = await supabase
    .from("uploaded_games")
    .select("*")
    .eq("user_id", user.id)
    .order("created_at", { ascending: false })

  if (!error) games.value = data || []
}

onMounted(fetchGames)
</script>

<template>
  <div class="text-center">

    <!-- UPLOAD MODAL -->
    <div style="margin-bottom: 20px;">
      <UploadPGNModal @loaded="loadMoves" />
    </div>

    <!-- TOP PLAYER -->
    <div class="player">
      <div class="left">
        <div>
          <div class="name">
            {{ currentGame?.white_name || "White" }}
          </div>
          <div class="rating">
            {{ currentGame?.white_country }} {{ currentGame?.white_elo || "--" }}
          </div>
        </div>
      </div>
    </div>

    <!-- BOARD -->
    <div class="board-wrapper">
      <chess-board ref="boardRef" class="board" />

      <!-- BOTTOM PLAYER -->
      <div class="player bottom-player">
        <div class="left">
          <div>
            <div class="name">
              {{ currentGame?.black_name || "Black" }}
            </div>
            <div class="rating">
              {{ currentGame?.black_country }} {{ currentGame?.black_elo || "--" }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- CONTROLS -->
    <div class="mb-4">
      <v-btn @click="prevMove">⬅️ Back</v-btn>
      <v-btn @click="nextMove">Forward ➡️</v-btn>
    </div>

    <!-- GAME LIST -->
    <div class="mt-4">
      <h3>Your Games</h3>

      <div v-for="game in games" :key="game.id">
        <v-btn @click="loadFromGame(game)">
          {{ game.white_name }} vs {{ game.black_name }}
          ({{ game.result }})
        </v-btn>
      </div>
    </div>

  </div>
</template>

<style scoped>
/* BOARD WRAPPER */
.board-wrapper {
  position: relative;
  width: fit-content;
  margin: 20px auto;
}

/* BOARD */
.board {
  width: 600px;
  max-width: 95vw;
}

/* PLAYER (TOP NORMAL) */
.player {
  display: flex;
  justify-content: space-between;
  align-items: center;

  width: 600px;
  margin: 10px auto;

  background: #2c2c2c;
  padding: 10px;
  border-radius: 8px;
}

/* OVERLAY PLAYER (BOTTOM ONLY) */
.bottom-player {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;

  width: 100%;
  margin: 0;

  background: rgba(44, 44, 44, 0.9);
  backdrop-filter: blur(6px);

  border-radius: 0 0 8px 8px;
}

/* PLAYER LEFT */
.player .left {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* AVATAR */
.avatar {
  width: 36px;
  height: 36px;
  border-radius: 6px;
}

/* TEXT */
.name {
  font-weight: bold;
  font-size: 14px;
}

.rating {
  font-size: 12px;
  color: #aaa;
}

/* TIMER */
.timer {
  background: #3a3a3a;
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 13px;
}
</style>