<script setup>
import { ref, watch, onBeforeUnmount } from 'vue'

const props = defineProps({
  formSuccessMessage: {
    type: String,
    default: '',
  },
  formErrorMessage: {
    type: String,
    default: '',
  },
})

const showSuccessAlert = ref(false)
const showErrorAlert = ref(false)

let successTimer = null
let errorTimer = null

const showSuccess = () => {
  clearTimeout(successTimer)
  clearTimeout(errorTimer)

  showErrorAlert.value = false
  showSuccessAlert.value = true

  successTimer = setTimeout(() => {
    showSuccessAlert.value = false
  }, 3000)
}

const showError = () => {
  clearTimeout(successTimer)
  clearTimeout(errorTimer)

  showSuccessAlert.value = false
  showErrorAlert.value = true

  errorTimer = setTimeout(() => {
    showErrorAlert.value = false
  }, 3000)
}

watch(
  () => props.formSuccessMessage,
  (message) => {
    if (message) {
      showSuccess()
    }
  },
)

watch(
  () => props.formErrorMessage,
  (message) => {
    if (message) {
      showError()
    }
  },
)

const closeSuccess = () => {
  showSuccessAlert.value = false
  clearTimeout(successTimer)
}

const closeError = () => {
  showErrorAlert.value = false
  clearTimeout(errorTimer)
}

onBeforeUnmount(() => {
  clearTimeout(successTimer)
  clearTimeout(errorTimer)
})
</script>

<template>
  <div class="notification-container">
    <v-alert
      v-if="showSuccessAlert && formSuccessMessage"
      type="success"
      variant="elevated"
      closable
      class="top-notification"
      @click:close="closeSuccess"
    >
      {{ formSuccessMessage }}
    </v-alert>

    <v-alert
      v-if="showErrorAlert && formErrorMessage"
      type="error"
      variant="elevated"
      closable
      class="top-notification"
      @click:close="closeError"
    >
      {{ formErrorMessage }}
    </v-alert>
  </div>
</template>

<style scoped>
.notification-container {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: min(500px, calc(100vw - 32px));
  z-index: 99999;
  pointer-events: none;
}

.top-notification {
  width: 100%;
  border-radius: 12px;
  pointer-events: auto;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.22);
}
</style>

