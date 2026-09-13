<script setup>
import { ref } from 'vue'
import StyleClassification from '@/components/layout/StyleClassification.vue'
import ChessboardView from '@/components/layout/ChessboardView.vue'
import EvaluationBarView from '@/components/layout/EvaluationBarView.vue'
import ChessCoach from '@/components/layout/ChessCoach.vue'

const STDrawer = ref(true)
const evalScore = ref(0)
const coachData = ref(null)
</script>

<template>
  <v-container
    fluid
    class="dashboard"
  >
    <v-row>

      <!-- Chessboard -->
      <v-col
        cols="12"
        md="8"
        class="pa-2"
      >
        <div class="chess-wrap">

          <ChessboardView
            @update-eval="evalScore = $event"
            @update-coach="coachData = $event"
          />

          <div class="eval-wrapper">
            <EvaluationBarView
              :score="evalScore"
            />
          </div>

        </div>
      </v-col>

      <!-- Right Panel -->
      <v-col
        cols="12"
        md="4"
        class="pa-2"
      >
        <ChessCoach
          :analysis="coachData"
        />

        <div class="panel-spacing"></div>

        <StyleClassification
          v-model="STDrawer"
        />
      </v-col>

    </v-row>
  </v-container>
</template>

<style scoped>
.dashboard {
  width: 100%;
  max-width: 1800px;
  margin: 0 auto;
  padding: 16px;
}

.chess-wrap {
  display: flex;
  align-items: stretch;
  gap: 10px;
  width: 100%;
}

.eval-wrapper {
  margin-top: 105px;
}

.panel-spacing {
  height: 20px;
}

@media (max-width: 960px) {
  .dashboard {
    padding: 10px;
  }

  .chess-wrap {
    gap: 5px;
  }

  .eval-wrapper {
    margin-top: 50px;
  }
}

@media (max-width: 600px) {
  .dashboard {
    padding: 6px;
  }

  .chess-wrap {
    gap: 3px;
  }

  .eval-wrapper {
    margin-top: 30px;
  }
}
</style>

