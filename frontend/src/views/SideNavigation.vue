<script setup>
import { defineProps, defineEmits, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '@/utils/supabase'
import { useAuthStore } from '@/stores/authUser'

defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  permanent: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

// Router and navigation logic
const router = useRouter()
const currentRoute = ref(router.currentRoute.value.name)

const navigateTo = (routeName) => {
  router.push({ name: routeName })
  currentRoute.value = routeName
}

const onLogout = async () => {
  await supabase.auth.signOut()
  const authStore = useAuthStore()
  authStore.logout()
  router.replace('/')
}
</script>


<template>
  <v-navigation-drawer
    class="bg-light-green-darken-3 rounded-e-xl pa-6"
    :width="350"
    elevation="16"
    :model-value="modelValue"
    :permanent="permanent"
    @update:modelValue="emit('update:modelValue', $event)"
  >
    <v-list color="transparent">
      <v-list class="text-center">
        <div class="profile-section">
          <v-avatar size="150" class="mx-auto" color="white">
            <!-- If profile_pic exists and is not null or empty, or if it's a file name -->
            <v-img
               v-if="profile_pic && typeof profile_pic === 'string' && profile_pic !== '' && profile_pic !== null"
                      :src="profile_pic.startsWith('http') ? profile_pic : profileUrl + profile_pic"
                      alt="User Avatar"
                      class="mx-auto"
                      height="200"
                      width="200"
                />
            <!-- Fallback image if profile_pic is not provided or is invalid -->
            <v-img
              v-else
              :src="'/images/pic1.jpg'"
              alt="User Avatar"
              class="mx-auto"
              height="200"
              width="200"
            />
          </v-avatar>
          <p class="text-center font-weight-bold mt-2">superwingwing</p>
        </div>
      </v-list>

      <v-list-item @click="navigateTo('search')">
        <v-btn class="rounded-pill text-light-green-darken-3" append-icon="mdi-magnify" block>
          Search
        </v-btn>
      </v-list-item>
      <v-list-item
        @click="navigateTo('dashboard')"
        :class="{ 'active-item': currentRoute === 'dashboard' }"
      >
        <v-list-item-title class="text-center">Home</v-list-item-title>
      </v-list-item>
      <v-list-item @click="navigateTo('save')" :class="{ 'active-item': currentRoute === 'save' }">
        <v-list-item-title class="text-center">Saved</v-list-item-title>
      </v-list-item>
      <v-list-item
        @click="navigateTo('profile')"
        :class="{ 'active-item': currentRoute === 'profile' }"
      >
        <v-list-item-title class="text-center">Profile</v-list-item-title>
      </v-list-item>
      <v-list-item
        @click="navigateTo('about')"
        :class="{ 'active-item': currentRoute === 'about' }"
      >
        <v-list-item-title class="text-center">About ChessKween</v-list-item-title>
      </v-list-item>
    </v-list>

    <template v-slot:append>
      <div class="pa-2">
        <v-btn
          class="rounded-pill text-light-green-darken-3 font-weight-black"
          block
          @click="onLogout"
        >
          Sign out
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>


<style scoped>
.active-item {
  background-color: rgba(255, 255, 255, 0.196);
  padding: 0.5rem 1rem;
  transition: background-color 0.3s ease;
}

.active-item:hover {
  background-color: rgba(255, 255, 255, 0.3);
}
</style>