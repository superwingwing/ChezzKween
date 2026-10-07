<script setup>
import { ref, reactive } from "vue"
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

// Come from authUser.js
if (authStore.user) {
  profile.username = authStore.user.user_metadata?.username || ""
}

const emit = defineEmits(["update:modelValue"])
const router = useRouter()
const currentRoute = ref(router.currentRoute.value.name)

const navigation = [
  {
    name: "dashboard",
    title: "Home",
    icon: "mdi-home-outline"
  },
  {
    name: "profile",
    title: "Profile",
    icon: "mdi-account-outline"
  },
  {
    name: "tips",
    title: "Tips",
    icon: "mdi-lightbulb-on-outline"
  },
  {
    name: "about",
    title: "About ChessKween",
    icon: "mdi-information-outline"
  }
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
    class="side-navigation"
    :width="270"
    elevation="0"
    :model-value="modelValue"
    :permanent="permanent"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <div class="navigation-content">

      <!-- ================= PROFILE ================= -->
      <div class="profile-section">

        <div class="avatar-wrapper">
          <v-avatar
            size="92"
            class="profile-avatar"
          >
            <v-img
              v-if="
                profile_pic &&
                typeof profile_pic === 'string' &&
                profile_pic !== ''
              "
              :src="
                profile_pic.startsWith('http')
                  ? profile_pic
                  : profileUrl + profile_pic
              "
              alt="User Avatar"
              cover
            />

            <span
              v-else
              class="avatar-letter"
            >
              {{
                authStore.user?.user_metadata?.username
                  ?.charAt(0)
                  ?.toUpperCase() || "?"
              }}
            </span>
          </v-avatar>

          <div class="online-indicator"></div>
        </div>

        <div class="profile-name">
          {{ authStore.user?.user_metadata?.username }}
        </div>

        <div class="profile-role">
          ChessKween Player
        </div>
      </div>

      <!-- ================= DIVIDER ================= -->
      <div class="section-divider"></div>

      <!-- ================= NAVIGATION ================= -->
      <div class="navigation-heading">
        MENU
      </div>

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
            <div class="navigation-icon">
              <v-icon :icon="item.icon" />
            </div>
          </template>

          <v-list-item-title>
            {{ item.title }}
          </v-list-item-title>

          <template #append>
            <v-icon
              v-if="currentRoute === item.name"
              icon="mdi-chevron-right"
              size="18"
              class="active-arrow"
            />
          </template>
        </v-list-item>
      </v-list>

      <!-- ================= BOTTOM AREA ================= -->
      <div class="bottom-section">

        <div class="chesskween-card">
          <div class="chesskween-icon">
            <v-icon
              icon="mdi-chess-queen"
              size="22"
            />
          </div>

          <div class="chesskween-text">
            <div class="chesskween-title">
              ChessKween
            </div>

            <div class="chesskween-subtitle">
              Improve your game
            </div>
          </div>
        </div>

        <!-- Logout -->
        <v-btn
          block
          rounded="lg"
          variant="text"
          class="logout-button"
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
/* =========================================================
   SIDEBAR
========================================================= */

.side-navigation {
  height: 100vh !important;
  top: 0 !important;
  bottom: 0 !important;

  background: #0d1b2a !important;

  border-radius: 0 20px 20px 0 !important;
  border-right: 1px solid rgba(255, 255, 255, 0.06);

  overflow: hidden;
}

/* =========================================================
   MAIN CONTAINER
========================================================= */

.navigation-content {
  display: flex;
  flex-direction: column;

  height: 100%;
  padding: 22px 16px;

  box-sizing: border-box;
}

/* =========================================================
   PROFILE
========================================================= */

.profile-section {
  display: flex;
  flex-direction: column;
  align-items: center;

  padding: 4px 4px 6px;

  text-align: center;
}

.avatar-wrapper {
  position: relative;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 100px;
  height: 100px;
}

.profile-avatar {
  background: #162b40 !important;

  border: 3px solid rgba(255, 255, 255, 0.95);

  box-shadow:
    0 8px 22px rgba(0, 0, 0, 0.25),
    0 0 0 5px rgba(255, 255, 255, 0.04);
}

.avatar-letter {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;

  color: #ffffff;

  font-family: Georgia, "Times New Roman", serif;
  font-size: 52px;
  font-weight: 900;

  line-height: 1;

  letter-spacing: -2px;
}

.online-indicator {
  position: absolute;

  right: 4px;
  bottom: 5px;

  width: 16px;
  height: 16px;

  background: #f28c28;

  border: 3px solid #0d1b2a;

  border-radius: 50%;
}

.profile-name {
  max-width: 210px;

  margin-top: 13px;

  overflow: hidden;

  color: #ffffff;

  font-size: 15px;
  font-weight: 700;

  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-role {
  margin-top: 3px;

  color: rgba(255, 255, 255, 0.5);

  font-size: 11px;
  font-weight: 500;

  letter-spacing: 0.02em;
}

/* =========================================================
   DIVIDER
========================================================= */

.section-divider {
  height: 1px;

  margin: 20px 4px 18px;

  background: rgba(255, 255, 255, 0.09);
}

/* =========================================================
   NAVIGATION HEADING
========================================================= */

.navigation-heading {
  padding: 0 12px 8px;

  color: rgba(255, 255, 255, 0.4);

  font-size: 10px;
  font-weight: 800;

  letter-spacing: 0.14em;
}

/* =========================================================
   NAVIGATION LIST
========================================================= */

.navigation-list {
  padding: 0;
}

.navigation-item {
  position: relative;

  min-height: 46px;

  margin: 4px 0;

  color: rgba(255, 255, 255, 0.68);

  transition:
    background 0.2s ease,
    color 0.2s ease,
    transform 0.2s ease;
}

.navigation-item:hover {
  background: rgba(255, 255, 255, 0.055);

  color: #ffffff;

  transform: translateX(2px);
}

.navigation-item :deep(.v-list-item__content) {
  padding: 2px 0;
}

.navigation-item :deep(.v-list-item-title) {
  font-size: 13.5px;
  font-weight: 600;
}

.navigation-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 34px;
  height: 34px;

  margin-right: 8px;

  border-radius: 9px;

  background: rgba(255, 255, 255, 0.045);

  transition:
    background 0.2s ease,
    color 0.2s ease;
}

.navigation-item :deep(.v-icon) {
  color: rgba(255, 255, 255, 0.62);

  font-size: 20px;
}

/* =========================================================
   ACTIVE NAVIGATION
========================================================= */

.active-item {
  background: #ffffff !important;

  color: #0d1b2a !important;

  box-shadow:
    0 6px 18px rgba(0, 0, 0, 0.14);
}

.active-item::before {
  content: "";

  position: absolute;

  left: 0;
  top: 8px;
  bottom: 8px;

  width: 3px;

  background: #f28c28;

  border-radius: 0 4px 4px 0;

  opacity: 1;
}

.active-item .navigation-icon {
  background: #f28c28;

  color: #ffffff;
}

.active-item :deep(.v-icon) {
  color: #ffffff !important;
}

.active-item :deep(.v-list-item-title) {
  color: #0d1b2a !important;

  font-weight: 700;
}

.active-arrow {
  color: #f28c28 !important;

  margin-right: 2px;
}

/* =========================================================
   BOTTOM SECTION
========================================================= */

.bottom-section {
  margin-top: auto;

  padding-top: 18px;
}

/* =========================================================
   CHESSKWEEN INFO CARD
========================================================= */

.chesskween-card {
  display: flex;
  align-items: center;

  gap: 11px;

  padding: 12px;

  margin-bottom: 12px;

  background: rgba(255, 255, 255, 0.055);

  border: 1px solid rgba(255, 255, 255, 0.07);

  border-radius: 12px;
}

.chesskween-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  flex: 0 0 auto;

  width: 38px;
  height: 38px;

  background: #f28c28;

  color: #ffffff;

  border-radius: 10px;
}

.chesskween-text {
  min-width: 0;
}

.chesskween-title {
  color: #ffffff;

  font-size: 12px;
  font-weight: 700;
}

.chesskween-subtitle {
  margin-top: 2px;

  color: rgba(255, 255, 255, 0.45);

  font-size: 10px;
}

/* =========================================================
   LOGOUT
========================================================= */

.logout-button {
  min-height: 43px;

  border: 1px solid rgba(255, 255, 255, 0.12);

  color: rgba(255, 255, 255, 0.7) !important;

  font-size: 13px;
  font-weight: 600;

  text-transform: none;

  transition:
    background 0.2s ease,
    border-color 0.2s ease,
    color 0.2s ease;
}

.logout-button:hover {
  background: rgba(242, 140, 40, 0.1);

  border-color: rgba(242, 140, 40, 0.45);

  color: #f28c28 !important;
}

/* =========================================================
   TABLET
========================================================= */

@media (max-width: 960px) {
  .navigation-content {
    padding: 18px 14px;
  }

  .avatar-wrapper {
    width: 90px;
    height: 90px;
  }

  .profile-avatar {
    width: 82px !important;
    height: 82px !important;
  }

  .avatar-letter {
    font-size: 46px;
  }
}

/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 600px) {
  .side-navigation {
    width: 250px !important;

    border-radius: 0 16px 16px 0 !important;
  }

  .navigation-content {
    padding: 16px 13px;
  }

  .avatar-wrapper {
    width: 84px;
    height: 84px;
  }

  .profile-avatar {
    width: 76px !important;
    height: 76px !important;
  }

  .avatar-letter {
    font-size: 42px;
  }

  .profile-name {
    font-size: 14px;
  }

  .navigation-item {
    min-height: 44px;
  }

  .navigation-item :deep(.v-list-item-title) {
    font-size: 13px;
  }

  .chesskween-card {
    padding: 10px;
  }
}
</style>