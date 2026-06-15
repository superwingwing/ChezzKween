<script setup>
import DashboardLayout from "@/components/layout/DashboardLayout.vue"
import StyleClassification from "../components/layout/StyleClassification.vue"
import ChessboardView from '@/views/ChessboardView.vue'
</script>

<template>
  <DashboardLayout>
    <v-container fluid>
      <v-row>

        <!-- CENTER -->
        <v-col cols="9" class="d-flex justify-center">
          <ChessboardView />
        </v-col>

        <!-- RIGHT -->
        <v-col cols="3">
          <StyleClassification />
        </v-col>

      </v-row>
    </v-container>
  </DashboardLayout>
</template>