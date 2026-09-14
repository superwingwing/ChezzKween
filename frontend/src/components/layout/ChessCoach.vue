<script setup>
defineProps({
  analysis: {
    type: Object,
    default: null
  }
})
</script>

<template>
  <v-card class="coach-card" elevation="4">
    <v-card-title class="coach-header">
      <v-icon icon="mdi-brain" />
      <span>ChessKween</span>
    </v-card-title>

    <v-divider />

    <v-card-text class="coach-content">
      <template v-if="analysis">
        <div class="move-row">
          <span class="label">Move</span>
          <strong>{{ analysis.move }}</strong>
        </div>

        <div class="quality">
          <span>{{ analysis.quality }}</span>
        </div>

        <section class="section">
          <h4>
            <v-icon icon="mdi-lightbulb-outline" />
            Explanation
          </h4>
          <p>{{ analysis.explanation }}</p>
        </section>

        <section class="section">
          <h4>
            <v-icon icon="mdi-chess-queen" />
            Recommendation
          </h4>
          <p>{{ analysis.recommendation }}</p>
        </section>
      </template>

      <div v-else class="empty-state">
        <!-- <v-icon icon="mdi-brain" size="42" /> -->
        <p>Upload a game to receive coaching feedback.</p>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.coach-card {
  width: 100%;
  max-width: 320px;
  height: 420px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-radius: 16px;
  background: #ffffff;
  color: #17212b;
  border: 1px solid #dce7f2;
}

.coach-header {
  min-height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  color: #12395b;
  font-size: 18px;
  font-weight: 700;
}

.coach-header .v-icon {
  color: #2878c8;
}

.coach-content {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 16px;
}

.move-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
  padding: 10px 12px;
  border-radius: 10px;
  background: #f3f7fb;
  color: #12395b;
}

.label {
  color: #64748b;
  font-size: 13px;
}

.move-row strong {
  font-size: 17px;
  color: #12395b;
}

.quality {
  padding: 9px 12px;
  border-radius: 10px;
  background: #2878c8;
  color: white;
  text-align: center;
  font-size: 14px;
  font-weight: 700;
}

.section {
  margin-top: 18px;
}

.section h4 {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0 0 7px;
  color: #2878c8;
  font-size: 14px;
  font-weight: 700;
}

.section p {
  margin: 0;
  color: #4b5f73;
  font-size: 13px;
  line-height: 1.6;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.empty-state {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  text-align: center;
  color: #64748b;
}

.empty-state .v-icon {
  color: #2878c8;
}

.empty-state p {
  max-width: 220px;
  margin: 0;
  font-size: 13px;
  line-height: 1.5;
}

@media (max-width: 960px) {
  .coach-card {
    max-width: 100%;
    height: 380px;
  }
}

@media (max-width: 600px) {
  .coach-card {
    width: 100%;
    max-width: none;
    height: 360px;
    border-radius: 14px;
  }

  .coach-header {
    font-size: 16px;
  }

  .coach-content {
    padding: 14px;
  }

  .section p {
    font-size: 12.5px;
  }
}
</style>