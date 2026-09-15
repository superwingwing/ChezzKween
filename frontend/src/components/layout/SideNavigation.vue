<script setup>
    import { ref,reactive } from "vue"
    import { useRouter } from "vue-router"
    import { supabase } from "@/utils/supabase"
    import { useAuthStore } from "@/stores/authUser"

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

        const authStore = useAuthStore()
        
        const profile = reactive({
          username: ""
        })

            //come from  the data in authuser.js
          if (authStore.user) {
          profile.username = authStore.user.user_metadata?.username || ""
        }

    const emit = defineEmits(["update:modelValue"])

    const router = useRouter()
    const currentRoute = ref(router.currentRoute.value.name)

    const navigation = [
      { name: "dashboard", title: "Home", icon: "mdi-home-outline" },
      { name: "save", title: "Saved", icon: "mdi-bookmark-outline" },
      { name: "profile", title: "Profile", icon: "mdi-account-outline" },
      { name: "about", title: "About ChessKween", icon: "mdi-information-outline" }
    ]

    const navigateTo = (routeName) => {
      router.push({ name: routeName })
      currentRoute.value = routeName
    }

    const onLogout = async () => {
      await supabase.auth.signOut()

      const authStore = useAuthStore()
      authStore.logout()

      router.replace("/")
    }
</script>

<template>
    <v-navigation-drawer
      class="side-navigation bg-light-blue-darken-4"
      :width="270"
      elevation="12"
      :model-value="modelValue"
      :permanent="permanent"
      @update:model-value="emit('update:modelValue', $event)"
    >
      <div class="navigation-content">

        <!-- Profile -->
        <div class="profile-section">
          <v-avatar
            size="105"
            color="white"
            class="profile-avatar"
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

          <div class="profile-name">
              {{ authStore.user?.user_metadata?.username }}
          </div>

          <div class="profile-label">
            ChessKween User
          </div>
        </div>

        <v-divider class="my-4" color="white" opacity="0.15" />

        <!-- Navigation -->
        <v-list
          nav
          bg-color="transparent"
          class="navigation-list"
        >
          <v-list-item
            v-for="item in navigation"
            :key="item.name"
            :active="currentRoute === item.name"
            active-class="active-item"
            rounded="lg"
            class="navigation-item"
            @click="navigateTo(item.name)"
          >
            <template #prepend>
              <v-icon :icon="item.icon" />
            </template>

            <v-list-item-title>
              {{ item.title }}
            </v-list-item-title>
          </v-list-item>
        </v-list>

        <!-- Logout -->
        <div class="logout-section">
          <v-btn
            block
            rounded="lg"
            variant="outlined"
            color="white"
            prepend-icon="mdi-logout"
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
  border-radius: 0 18px 18px 0 !important;
}

.navigation-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 18px;
  box-sizing: border-box;
}

.profile-section {
  text-align: center;
  padding-top: 4px;
}

.profile-avatar {
  border: 3px solid rgba(255, 255, 255, 0.9);
}

.profile-name {
  margin-top: 10px;
  color: white;
  font-size: 15px;
  font-weight: 700;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-label {
  margin-top: 2px;
  color: rgba(255, 255, 255, 0.65);
  font-size: 11px;
}

.search-button {
  min-height: 42px;
  text-transform: none;
  font-weight: 600;
}

.navigation-list {
  padding: 10px 0;
}

.navigation-item {
  min-height: 44px;
  margin-bottom: 4px;
  color: rgba(255, 255, 255, 0.85);
  transition: 0.2s ease;
}

.navigation-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.navigation-item :deep(.v-icon) {
  color: rgba(255, 255, 255, 0.75);
}

.active-item {
  background: rgba(255, 255, 255, 0.18) !important;
  color: white !important;
}

.active-item :deep(.v-icon) {
  color: white !important;
}

.logout-section {
  margin-top: auto;
  padding-top: 12px;
}

.logout-section .v-btn {
  min-height: 42px;
  text-transform: none;
  font-weight: 600;
}

@media (max-width: 960px) {
  .navigation-content {
    padding: 16px;
  }

  .profile-avatar {
    width: 90px !important;
    height: 90px !important;
  }
}

@media (max-width: 600px) {
  .side-navigation {
    width: 250px !important;
  }

  .navigation-content {
    padding: 14px;
  }

  .profile-avatar {
    width: 82px !important;
    height: 82px !important;
  }

  .profile-name {
    font-size: 14px;
  }

  .navigation-item {
    min-height: 42px;
  }
}
</style>

