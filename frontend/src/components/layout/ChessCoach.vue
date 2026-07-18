<script setup>
    defineProps({
      analysis:{
        type:Object,
        default:null
      }
    })
</script>

<template>
    <div class="coach-card">
      <h3>🧠 Chess Kween</h3>
      <div v-if="analysis">
        <p class="move">
          Move: <strong>{{ analysis.move }}</strong>
        </p>
        <p class="quality">
          {{ analysis.quality }}
        </p>
        <div class="section">
          <h4>Explanation</h4>
          <p>{{ analysis.explanation }}</p>
        </div>

        <div class="section">
          <h4>Recommendation</h4>
          <p>{{ analysis.recommendation }}</p>
        </div>
      </div>
      <p v-else>
          Upload a game to receive coaching feedback.
      </p>
    </div>
</template>

<style scoped>
    .coach-card{
      width:320px;
      padding:20px;
      border-radius:15px;
      background:#1f2937;
      color:white;
    }
    h3{
      text-align:center;
      margin-bottom:15px;
    }
    .move{
      font-size:18px;
    }
    .quality{
      padding:8px;
      border-radius:10px;
      background:#374151;
      text-align:center;
    }
    .section{
      margin-top:15px;
    }
    .section h4{
      color:#4ade80;
    }
</style>