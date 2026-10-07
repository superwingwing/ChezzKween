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
    ChessCoach,
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
      coachData,
    }
  },
}
</script>

<template>
  <v-layout class="layout">

    <!-- Side Navigation -->
    <SideNavigation v-model="navigationDrawer" :permanent="isLargeScreen" />

    <!-- Main Page Area -->
    <v-main class="main-content">
      <router-view v-slot="{ Component }">
        <KeepAlive>
          <component :is="Component" />
        </KeepAlive>
      </router-view>
    </v-main>
  </v-layout>
</template>

<style scoped>
.layout {
  min-height: 100vh;
}

.app-bar {
  z-index: 10 !important;
  pointer-events: none;
}

.app-bar :deep(.v-btn) {
  pointer-events: auto;
}

.main-content {
  min-height: 100vh;
  width: 100%;
  position: relative;
  z-index: 1;
}
</style>
