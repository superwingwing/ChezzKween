<script>
import SideNavigation from '@/components/layout/SideNavigation.vue'
import StyleClassification from '@/components/layout/StyleClassification.vue'
import ChessboardView from '@/components/layout/ChessboardView.vue'
import EvaluationBarView from '@/components/layout/EvaluationBarView.vue'
import ChessCoach from '@/components/layout/ChessCoach.vue'
import { ref, computed } from 'vue'
import { useDisplay } from 'vuetify'

export default {
  components: {
    SideNavigation,
    StyleClassification,
    ChessboardView,
    EvaluationBarView,
    ChessCoach
  },

  setup() {
    const { mdAndUp } = useDisplay()

    const isLargeScreen = computed(() => mdAndUp.value)

    const navigationDrawer = ref(isLargeScreen.value)
    const STDrawer = ref(isLargeScreen.value)

    const evalScore = ref(0)
    const coachData = ref(null)

    return {
      navigationDrawer,
      STDrawer,
      isLargeScreen,
      evalScore,
      coachData
    }
  }
}
</script>

<template>
  <v-layout class="layout">

    <!-- App Bar -->
    <v-app-bar
      app
      flat
      height="64"
      color="transparent"
      class="app-bar"
    >
      <!-- Navigation Toggle -->
      <v-btn
        icon
        color="light-green-darken-3"
        @click="navigationDrawer = !navigationDrawer"
      >
        <v-icon>mdi-menu</v-icon>
      </v-btn>

      <!-- Logo -->
      <v-img
        src="/images/logo.png"
        max-width="120"
        contain
        class="mx-auto"
      />

      <!-- Right Side Toggle -->
      <v-btn
        icon
        color="light-green-darken-3"
        @click="STDrawer = !STDrawer"
      >
        <v-icon>mdi-newspaper-variant-outline</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- Side Navigation -->
    <SideNavigation
      v-model="navigationDrawer"
      :permanent="isLargeScreen"
    />

    <!-- Main Page Area -->
    <v-main class="main-content">
      <router-view />
    </v-main>

  </v-layout>
</template>

<style scoped>
.layout {
  min-height: 100vh;
}

.app-bar {
  z-index: 10;
}

.main-content {
  min-height: 100vh;
  width: 100%;
  padding-top: 64px;
}
</style>
