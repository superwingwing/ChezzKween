<script setup>
import { ref } from 'vue'
import StyleClassification from '@/components/layout/StyleClassification.vue'
import ChessboardView from '@/components/layout/ChessboardView.vue'
import ChessCoach from '@/components/layout/ChessCoach.vue'

const STDrawer = ref(true)
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
            @update-coach="coachData = $event"
          />

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
  padding: 4px !important;
}

.chess-wrap {
  display: flex;
  align-items: flex-start;
  gap: 0;
  width: 100%;
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
}

@media (max-width: 600px) {
  .dashboard {
    padding: 6px;
  }

  .chess-wrap {
    gap: 3px;
  }
}
</style>

