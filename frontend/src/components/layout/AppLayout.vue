<template>
  <v-responsive class="border rounded">
    <v-app>
      <!-- Background image container -->
      <div class="background-image">
        <v-main class="d-flex align-center justify-center fill-height" transition="fade-transition">
          <v-container>
            <slot name="content"></slot>
          </v-container>
        </v-main>
      </div>

      <v-footer border app class="footer-container text-center d-flex flex-column">
        <div>© ChessKween - Improve your games in chess</div>
        <v-divider></v-divider>
        <div>All Rights Reserved</div>
      </v-footer>
    </v-app>
  </v-responsive>
</template>

<style scoped>
.fill-height {
  min-height: 100vh;
}

.background-image {
  min-height: 100vh;
  background-image: url('/images/chess_background.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #4c7ae5;
}

.footer-container {
  background-color: #01579B;
  padding: 8px 16px;
  font-size: 0.85rem;
  color: white;
}
</style>
