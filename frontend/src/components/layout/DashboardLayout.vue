<script>
import SideNavigation from '@/components/layout/SideNavigation.vue'
import StyleClassification from '@/components/layout/StyleClassification.vue'
import ChessboardView from '@/components/layout/ChessboardView.vue'
import EvaluationBarView from '@/components/layout/EvaluationBarView.vue'
import { ref, computed } from 'vue'
import { useDisplay } from 'vuetify'

export default {
  components: {
    SideNavigation,
    StyleClassification,
    ChessboardView,
    EvaluationBarView
  },
  setup() {
    const { mdAndUp } = useDisplay() // Vuetify breakpoint utility
    const isLargeScreen = computed(() => mdAndUp.value) // True if the screen size is medium or larger
    // Separate drawer states for SideNavigation and StyleClassification
    const navigationDrawer = ref(isLargeScreen.value) // SideNavigation drawer state
    const STDrawer = ref(isLargeScreen.value) // STYLE CLASSIFICATION drawer state
    const evalScore = ref(0)
    return { navigationDrawer, STDrawer, isLargeScreen, evalScore }
  }
}
</script>

<template>
  <v-layout>
    <!-- App Bar -->
    <v-app-bar app flat height="64" class="transparent-bar text-center" color="transparent">
      <!-- Toggle Button for SideNavigation -->
      <v-btn
        icon
        color="light-green-darken-3"
        @click="navigationDrawer = !navigationDrawer"
        class="pa-4"
      >
        <v-icon>mdi-menu</v-icon>
      </v-btn>

      <v-img src="/images/logo.png" class="pa-6 mx-auto" max-width="120" contain />

      <!-- Toggle Button for StyleClassification -->
      <v-btn icon color="light-green-darken-3" @click="STDrawer = !STDrawer" class="pa-4">
        <v-icon>mdi-newspaper-variant-outline</v-icon>
      </v-btn>
    </v-app-bar>

    <v-container fluid>
      <v-row>
        <!-- Side Navigation -->
        <v-col cols="12" sm="3" md="3" class="pa-2">
          <SideNavigation
            :model-value="navigationDrawer"
            :permanent="isLargeScreen"
            @update:model-value="navigationDrawer = $event"
          />
        </v-col>

        <!-- Main Content -->
        <v-col cols="12" sm="6" md="6" class="pa-2">
          <v-container>
               <div class="chess-wrap">
              <ChessboardView @update-eval="evalScore = $event" />
              <EvaluationBarView :score="evalScore" />
            </div>
          </v-container>
        </v-col>

        <!-- Style Classification -->
        <v-col cols="12" sm="3" md="3" class="pa-2">
          <StyleClassification
            :model-value="STDrawer"
            :permanent="isLargeScreen"
            @update:model-value="STDrawer = $event"
          />
        </v-col>
      </v-row>
    </v-container>
  </v-layout>
</template>

<style scoped>
  .chess-wrap {
    display: flex;
    align-items: stretch;
    gap: 10px;
  }
</style>