<script setup>
import { ref } from "vue"
import UploadPGNModal from "@/components/layout/UploadPGNModal.vue"
import StyleClassification from "@/components/layout/StyleClassification.vue"
import ChessboardView from "@/components/layout/ChessboardView.vue"
import ChessCoach from "@/components/layout/ChessCoach.vue"

const chessboardRef = ref(null)
const coachData = ref(null)

/*
|--------------------------------------------------------------------------
| LOAD SINGLE PGN INTO CHESSBOARD
|--------------------------------------------------------------------------
| UploadPGNModal handles the PGN upload.
| ChessboardView handles the actual chess analysis.
*/
const handleGameLoaded = (response) => {
  if (chessboardRef.value?.loadMoves) {
    chessboardRef.value.loadMoves(response)
  }
}
</script>


<template>
  <v-container
    fluid
    class="dashboard"
  >

    <!-- =====================================================
         HEADER
    ====================================================== -->
    <div class="dashboard-header">
      <div class="header-left">
        <div class="eyebrow">
          CHESSKWEEN WORKSPACE
        </div>
        <h1>
          Interactive Engine Dashboard
        </h1>
      </div>
      <div class="header-actions">

        <!-- SINGLE GAME PGN UPLOAD -->
        <UploadPGNModal
          @loaded="handleGameLoaded"
        />

        <v-btn
          class="notification-btn"
          icon
          variant="outlined"
        >
          <v-icon size="19">
            mdi-bell-outline
          </v-icon>
          <span class="notification-dot"></span>
        </v-btn>
      </div>
    </div>


    <!-- =====================================================
         ENGINE STATUS
    ====================================================== -->
    <!-- <div class="engine-status">
      <div class="engine-info">
        <div class="engine-status-dot"></div>
        <div class="engine-text">
          <div class="engine-title">
            STOCKFISH 16.1 NEURAL ENGINE
          </div>
          <div class="engine-subtitle">
            Italian Game: Two Knights Defense, Fried Liver Attack
          </div>
        </div>
      </div>
      <div class="engine-stats">

        <div class="engine-stat">
          <span>Depth:</span>
          <strong>24 / 99</strong>
        </div>

        <div class="engine-stat eval">
          <span>Eval:</span>
          <strong>+1.4</strong>
        </div>
      </div>
    </div> -->


    <!-- =====================================================
         MAIN DASHBOARD
    ====================================================== -->
    <div class="dashboard-grid">
      <!-- ===================================================
           LEFT: CHESSBOARD
      ==================================================== -->
      <section class="board-column">
        <ChessboardView
          ref="chessboardRef"
          @update-coach="coachData = $event"
        />
      </section>


      <!-- ===================================================
           RIGHT: COACH + CLASSIFIER
      ==================================================== -->
      <aside class="right-column">
        <!-- AI COACH -->
        <ChessCoach
          :analysis="coachData"
        />
        <!-- STYLE CLASSIFIER -->
        <StyleClassification />
      </aside>

    </div>

  </v-container>
</template>


<style scoped>

/* =========================================================
   DASHBOARD
========================================================= */

.dashboard {
  width: 100%;
  max-width: 1250px;

  height: 100dvh;

  margin: 0 auto;

  padding: 12px 18px !important;

  box-sizing: border-box;

  overflow: hidden;
}


/* =========================================================
   HEADER
========================================================= */

.dashboard-header {
  width: 100%;

  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 20px;

  margin-bottom: 12px;

  box-sizing: border-box;
}


.header-left {
  min-width: 0;
}


.eyebrow {
  margin-bottom: 3px;

  color: #F28C28;

  font-size: 11px;
  font-weight: 800;

  letter-spacing: 0.8px;
}


.dashboard-header h1 {
  margin: 0;

  color: #0B1F3A;

  font-size: clamp(24px, 2.4vw, 32px);

  line-height: 1.05;

  font-weight: 800;

  letter-spacing: -0.8px;
}


/* =========================================================
   HEADER ACTIONS
========================================================= */

.header-actions {
  display: flex;
  align-items: center;

  gap: 9px;

  flex-shrink: 0;
}


.header-actions :deep(.v-btn) {
  min-height: 38px;

  border-radius: 10px;

  font-weight: 700;

  text-transform: none;
}


/* =========================================================
   NOTIFICATION
========================================================= */

.notification-btn {
  position: relative;

  width: 38px;
  height: 38px;

  min-width: 38px !important;

  color: #0B1F3A !important;

  border-color: #DDE4EC !important;

  background: #ffffff !important;
}


.notification-dot {
  position: absolute;

  top: 6px;
  right: 6px;

  width: 7px;
  height: 7px;

  border-radius: 50%;

  background: #F28C28;

  border: 2px solid white;
}


/* =========================================================
   ENGINE STATUS
========================================================= */

.engine-status {
  width: 100%;

  min-height: 64px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 20px;

  padding: 11px 18px;

  box-sizing: border-box;

  border-radius: 14px;

  background:
    linear-gradient(
      135deg,
      #0B1F3A,
      #07172D
    );

  box-shadow:
    0 8px 20px
    rgba(7, 23, 45, 0.14);

  margin-bottom: 12px;
}


/* =========================================================
   ENGINE INFO
========================================================= */

.engine-info {
  display: flex;
  align-items: center;

  gap: 10px;

  min-width: 0;
}


.engine-status-dot {
  width: 10px;
  height: 10px;

  flex-shrink: 0;

  border-radius: 50%;

  background: #2DB58A;
}


.engine-text {
  min-width: 0;
}


.engine-title {
  color: #F28C28;

  font-size: 11px;
  font-weight: 800;

  letter-spacing: 0.4px;
}


.engine-subtitle {
  margin-top: 2px;

  color: #ffffff;

  font-size: 12px;
  font-weight: 600;

  white-space: nowrap;

  overflow: hidden;

  text-overflow: ellipsis;
}


/* =========================================================
   ENGINE STATS
========================================================= */

.engine-stats {
  display: flex;
  align-items: center;

  gap: 8px;

  flex-shrink: 0;
}


.engine-stat {
  display: flex;
  align-items: center;

  gap: 5px;

  padding: 5px 9px;

  border-radius: 7px;

  background: rgba(255, 255, 255, 0.07);

  border: 1px solid rgba(255, 255, 255, 0.10);

  color: #AEBED2;

  font-size: 10px;
}


.engine-stat strong {
  color: #ffffff;

  font-size: 10px;
}


.engine-stat.eval strong {
  color: #2DB58A;
}


/* =========================================================
   MAIN GRID
========================================================= */

.dashboard-grid {
  width: 100%;

  /*
    Header uses approximately 55-65px.
    We intentionally do NOT reserve 114px because
    engine-status is currently not displayed.
  */
  height: calc(100% - 62px);

  min-height: 0;

  display: grid;

  grid-template-columns:
    minmax(0, 1.08fr)
    minmax(360px, 0.92fr);

  gap: 24px;

  align-items: stretch;

  box-sizing: border-box;
}


/* =========================================================
   LEFT BOARD COLUMN
========================================================= */

.board-column {
  width: 100%;
  height: 100%;

  min-width: 0;
  min-height: 0;

  display: flex;

  align-items: center;
  justify-content: center;

  overflow: hidden;

  box-sizing: border-box;
}


/* =========================================================
   CHESSBOARD CONTAINER
========================================================= */

.board-column :deep(.chessboard-container) {

  width: min(
    100%,
    calc(100dvh - 255px)
  );

  max-width: 620px;

  margin: 0 auto;

  padding: 0;

  box-sizing: border-box;
}


/* =========================================================
   BOARD ROW
========================================================= */

.board-column :deep(.board-row) {

  width: 100%;

  max-width: 100%;

  margin: 0 auto;

  box-sizing: border-box;
}


/* =========================================================
   CHESS BOARD
========================================================= */

.board-column :deep(.board) {

  width: min(
    600px,
    calc(100dvh - 255px)
  );

  max-width: 100%;

  flex: 1 1 auto;

  margin: 0;

  border-radius: 8px;

  box-sizing: border-box;
}


/* =========================================================
   EVALUATION BAR
========================================================= */

.board-column :deep(.evaluation-bar) {

  width: 16px;

  min-width: 16px;

  flex: 0 0 16px;
}


/* =========================================================
   PLAYER CARDS
========================================================= */

.board-column :deep(.player-card) {

  width: 100%;

  max-width: 100%;

  min-height: 44px;

  margin-bottom: 6px;

  padding: 6px 10px;

  border-radius: 9px;

  box-sizing: border-box;
}


/* =========================================================
   BOARD CONTROLS
========================================================= */

.board-column :deep(.controls) {

  margin-top: 8px;

  gap: 6px;

  box-sizing: border-box;
}


.board-column :deep(.control-btn) {

  height: 31px !important;

  min-width: 76px;

  padding: 0 11px !important;

  font-size: 11px;
}


/* =========================================================
   RIGHT COLUMN
========================================================= */

.right-column {
  width: 100%;
  height: 100%;

  min-width: 0;
  min-height: 0;

  display: flex;

  flex-direction: column;

  justify-content: flex-start;

  gap: 12px;

  /*
    Only the right side can scroll.
    The entire dashboard will not scroll on desktop.
  */
  overflow-y: auto;
  overflow-x: hidden;

  padding-right: 4px;

  box-sizing: border-box;

  scrollbar-width: thin;
}


/* =========================================================
   CHESS COACH
========================================================= */

.right-column > :first-child {

  width: 100%;

  min-width: 0;

  flex: 0 0 auto;
}


/*
  Keep ChessCoach from becoming excessively tall.
  Its own content can scroll internally.
*/

.right-column :deep(.coach-card) {

  width: 100%;

  height: clamp(
    350px,
    52vh,
    420px
  );

  min-height: 0;

  box-sizing: border-box;
}


/* =========================================================
   STYLE CLASSIFIER
========================================================= */

.right-column > :last-child {

  width: 100%;

  min-width: 0;

  flex: 0 0 auto;
}


.right-column :deep(.classifier-card) {
 width: 100%;
  max-width: none;

  height: 270px;
  min-height: 270px;

  flex: 0 0 270px;

  box-sizing: border-box;

  overflow: hidden;
}


/* =========================================================
   RIGHT COLUMN SCROLLBAR
========================================================= */

.right-column::-webkit-scrollbar {
  width: 5px;
}


.right-column::-webkit-scrollbar-track {
  background: transparent;
}


.right-column::-webkit-scrollbar-thumb {
  background: #D8DEE7;

  border-radius: 10px;
}


.right-column::-webkit-scrollbar-thumb:hover {
  background: #B9C3D0;
}


/* =========================================================
   SHORT LAPTOP
========================================================= */

@media (
  max-height: 820px
) and (
  min-width: 1001px
) {

  .dashboard {

    padding-top: 7px !important;

    padding-bottom: 7px !important;
  }


  .dashboard-header {

    margin-bottom: 8px;
  }


  .dashboard-header h1 {

    font-size: 25px;
  }


  .eyebrow {

    font-size: 10px;
  }


  /* -------------------------------------------------------
     BOARD
  ------------------------------------------------------- */

  .board-column :deep(.chessboard-container) {

    width: min(
      100%,
      calc(100dvh - 225px)
    );
  }


  .board-column :deep(.board) {

    width: min(
      100%,
      calc(100dvh - 225px)
    );
  }


  .board-column :deep(.player-card) {

    min-height: 40px;

    margin-bottom: 5px;

    padding: 5px 9px;
  }


  .board-column :deep(.player-avatar) {

    width: 28px;

    height: 28px;
  }


  .board-column :deep(.player-name) {

    font-size: 11px;
  }


  .board-column :deep(.player-side) {

    font-size: 9px;
  }


  .board-column :deep(.controls) {

    margin-top: 6px;
  }


  .board-column :deep(.control-btn) {

    height: 29px !important;

    min-width: 70px;

    font-size: 10px;
  }


  /* -------------------------------------------------------
     RIGHT COLUMN
  ------------------------------------------------------- */

  .right-column {

    gap: 9px;
  }


  .right-column :deep(.coach-card) {

    height: 370px;

    flex-basis: 370px;
  }


  .right-column :deep(.classifier-card) {

     height: 255px;

  min-height: 255px;

  flex-basis: 255px;
  }
}


/* =========================================================
   VERY SHORT LAPTOP
========================================================= */

@media (
  max-height: 720px
) and (
  min-width: 1001px
) {

  .dashboard {

    padding: 4px 12px !important;
  }


  .dashboard-header {

    margin-bottom: 5px;
  }


  .dashboard-header h1 {

    font-size: 22px;
  }


  /* -------------------------------------------------------
     BOARD
  ------------------------------------------------------- */

  .board-column :deep(.chessboard-container) {

    width: min(
      100%,
      calc(100dvh - 195px)
    );
  }


  .board-column :deep(.board) {

    width: min(
      100%,
      calc(100dvh - 195px)
    );
  }


  .board-column :deep(.player-card) {

    min-height: 35px;

    padding: 4px 7px;

    margin-bottom: 3px;
  }


  .board-column :deep(.player-avatar) {

    width: 25px;

    height: 25px;
  }


  .board-column :deep(.player-name) {

    font-size: 10px;
  }


  .board-column :deep(.player-side) {

    font-size: 8px;
  }


  .board-column :deep(.controls) {

    margin-top: 4px;

    gap: 4px;
  }


  .board-column :deep(.control-btn) {

    height: 26px !important;

    min-width: 62px;

    padding: 0 7px !important;

    font-size: 9px;
  }


  /* -------------------------------------------------------
     RIGHT COLUMN
  ------------------------------------------------------- */

  .right-column {

    gap: 7px;
  }


  .right-column :deep(.coach-card) {

    height: 330px;

    flex-basis: 330px;
  }


  .right-column :deep(.classifier-card) {

     height: 235px;

  min-height: 235px;

  flex-basis: 235px;
  }
}


/* =========================================================
   TABLET
========================================================= */

@media (max-width: 1000px) {

  .dashboard {

    height: auto;

    min-height: 100dvh;

    overflow: visible;

    max-width: 900px;

    padding: 14px 14px 25px !important;
  }


  .dashboard-grid {

    height: auto;

    display: grid;

    grid-template-columns: 1fr;

    gap: 18px;

    align-items: start;
  }


  /* -------------------------------------------------------
     BOARD
  ------------------------------------------------------- */

  .board-column {

    height: auto;

    overflow: visible;
  }


  .board-column :deep(.chessboard-container) {

    width: 100%;

    max-width: 620px;
  }


  .board-column :deep(.board) {

    width: min(
      600px,
      100%
    );
  }


  /* -------------------------------------------------------
     RIGHT COLUMN
  ------------------------------------------------------- */

  .right-column {

    height: auto;

    overflow: visible;

    padding-right: 0;
  }


  .right-column :deep(.coach-card) {

    height: 420px;

    min-height: 420px;

    flex-basis: auto;
  }


  .right-column :deep(.classifier-card) {

    width: 100%;

    height: auto;

    min-height: 220px;

    flex-basis: auto;
  }
}


/* =========================================================
   SMALL TABLET
========================================================= */

@media (max-width: 700px) {

  .dashboard {

    padding: 12px 10px 22px !important;
  }


  .dashboard-header {

    align-items: flex-start;

    margin-bottom: 14px;
  }


  .dashboard-header h1 {

    font-size: 24px;
  }


  /* -------------------------------------------------------
     ENGINE
  ------------------------------------------------------- */

  .engine-status {

    flex-direction: column;

    align-items: flex-start;

    padding: 12px;

    margin-bottom: 14px;
  }


  .engine-stats {

    width: 100%;
  }


  .engine-stat {

    flex: 1;

    justify-content: center;
  }


  /* -------------------------------------------------------
     GRID
  ------------------------------------------------------- */

  .dashboard-grid {

    gap: 16px;
  }


  .right-column {

    gap: 12px;
  }


  .right-column :deep(.coach-card) {

    height: 400px;

    min-height: 400px;
  }
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 500px) {

  .dashboard {

    padding: 9px 7px 18px !important;
  }


  .dashboard-header {

    flex-direction: column;

    gap: 10px;
  }


  .header-actions {

    width: 100%;
  }


  .header-actions :deep(.v-btn:first-child) {

    flex: 1;
  }


  .dashboard-header h1 {

    font-size: 22px;
  }


  .eyebrow {

    font-size: 10px;
  }


  /* -------------------------------------------------------
     ENGINE
  ------------------------------------------------------- */

  .engine-status {

    border-radius: 10px;
  }


  .engine-subtitle {

    max-width: 250px;

    white-space: normal;
  }


  /* -------------------------------------------------------
     GRID
  ------------------------------------------------------- */

  .dashboard-grid {

    gap: 14px;
  }


  .right-column {

    gap: 12px;
  }


  .right-column :deep(.coach-card) {

    height: 380px;

    min-height: 380px;
  }


.right-column :deep(.classifier-header) {
  padding: 12px 16px 8px !important;
}

.right-column :deep(.classifier-content) {
  padding: 6px 16px 14px !important;
}

.right-column :deep(.drop-zone) {
  padding: 18px 12px;
}

.right-column :deep(.upload-btn) {
  margin-top: 10px;
  min-height: 44px;
}
}

</style>