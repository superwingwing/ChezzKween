<script setup>
import { defineProps, defineEmits, ref } from 'vue'
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
    class="side-navigation bg-light-green-darken-3"
    :width="350"
    elevation="16"
    :model-value="modelValue"
    :permanent="permanent"
    @update:modelValue="emit('update:modelValue', $event)"
  >
    <div class="navigation-content">

      <div class="profile-section">
        <v-avatar
          size="150"
          color="white"
        >
          <v-img
            v-if="profile_pic && typeof profile_pic === 'string' && profile_pic !== ''"
            :src="profile_pic.startsWith('http') ? profile_pic : profileUrl + profile_pic"
            alt="User Avatar"
            cover
          />

          <v-img
            v-else
            src="/images/pic1.jpg"
            alt="User Avatar"
            cover
          />
        </v-avatar>

        <p class="profile-name">
          superwingwing
        </p>
      </div>

      <v-list
        color="transparent"
        class="navigation-list"
      >
        <v-list-item @click="navigateTo('search')">
          <v-btn
            class="search-button rounded-pill text-light-green-darken-3"
            append-icon="mdi-magnify"
            block
          >
            Search
          </v-btn>
        </v-list-item>

        <v-list-item
          @click="navigateTo('dashboard')"
          :class="{ 'active-item': currentRoute === 'dashboard' }"
        >
          <v-list-item-title class="text-center">
            Home
          </v-list-item-title>
        </v-list-item>

        <v-list-item
          @click="navigateTo('save')"
          :class="{ 'active-item': currentRoute === 'save' }"
        >
          <v-list-item-title class="text-center">
            Saved
          </v-list-item-title>
        </v-list-item>

        <v-list-item
          @click="navigateTo('profile')"
          :class="{ 'active-item': currentRoute === 'profile' }"
        >
          <v-list-item-title class="text-center">
            Profile
          </v-list-item-title>
        </v-list-item>

        <v-list-item
          @click="navigateTo('about')"
          :class="{ 'active-item': currentRoute === 'about' }"
        >
          <v-list-item-title class="text-center">
            About ChessKween
          </v-list-item-title>
        </v-list-item>
      </v-list>

      <div class="logout-section">
        <v-btn
          class="rounded-pill text-light-green-darken-3 font-weight-black"
          block
          @click="onLogout"
        >
          Sign out
        </v-btn>
      </div>

    </div>
  </v-navigation-drawer>
</template>

<style scoped>
.side-navigation {
  height: 100vh !important;
  top: 0 !important;
  bottom: 0 !important;
  border-radius: 0 20px 20px 0 !important;
}

.navigation-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 24px;
}

.profile-section {
  text-align: center;
  padding-top: 10px;
}

.profile-name {
  margin: 12px 0 20px;
  font-weight: 700;
  color: white;
}

.navigation-list {
  flex: 1;
  padding: 0;
}

.search-button {
  margin-bottom: 8px;
}

.active-item {
  background-color: rgba(255, 255, 255, 0.196);
  padding: 8px 16px;
  margin-bottom: 4px;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.active-item:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.logout-section {
  margin-top: auto;
  padding-top: 20px;
}

@media (max-width: 600px) {
  .side-navigation {
    width: 280px !important;
  }

  .navigation-content {
    padding: 18px;
  }

  .profile-section {
    padding-top: 5px;
  }

  .profile-section .v-avatar {
    width: 110px !important;
    height: 110px !important;
  }
}
</style>

