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
    title: "Tips & Tactics",
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
    :width="282"
    elevation="0"
    :model-value="modelValue"
    :permanent="permanent"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <div class="navigation-content">

      <!-- =====================================================
           BRAND
      ====================================================== -->
      <div class="brand-section">
        <div class="brand-logo">
          <v-icon size="28">
            mdi-chess-queen
          </v-icon>
        </div>

        <div class="brand-text">
          <div class="brand-name">
            Chess<span>Kween</span>
          </div>

          <div class="brand-subtitle">
            ANALYTICS HUB
          </div>
        </div>
      </div>

      <div class="brand-divider"></div>


      <!-- =====================================================
           USER PROFILE CARD
      ====================================================== -->
      <div class="user-card">

        <div class="user-avatar-wrapper">
          <v-avatar
            size="46"
            class="user-avatar"
          >
            <span class="avatar-letter">
              {{
                authStore.user?.user_metadata?.username
                  ?.charAt(0)
                  ?.toUpperCase() || "?"
              }}
            </span>
          </v-avatar>

          <span class="online-indicator"></span>
        </div>

        <div class="user-details">
          <div class="user-name">
            {{ authStore.user?.user_metadata?.username || "ChessKween User" }}
          </div>

          <div class="user-role">
            Premium Member
          </div>
        </div>
      </div>


      <!-- =====================================================
           NAVIGATION
      ====================================================== -->
      <div class="navigation-section">

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
            class="navigation-item"
            rounded="lg"
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
                size="17"
                class="active-arrow"
              />
            </template>

          </v-list-item>

        </v-list>

      </div>


      <!-- =====================================================
           BOTTOM SECTION
      ====================================================== -->
      <div class="bottom-section">

        <!-- ChessKween information -->
        <div class="chesskween-card">

          <div class="chesskween-icon">
            <v-icon
              icon="mdi-chess-queen"
              size="20"
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
   COLOR SYSTEM
========================================================= */

.side-navigation {
  --navy: #0b142d;
  --navy-light: #151f3b;
  --navy-card: #151f3a;
  --navy-hover: #1b2746;

  --orange: #ff7900;
  --orange-dark: #ed6c00;

  --white: #ffffff;
  --muted: #91a4c2;

  height: 100vh !important;
  top: 0 !important;
  bottom: 0 !important;

  background: var(--navy) !important;

  border-right: 1px solid rgba(255, 255, 255, 0.05);

  border-radius: 0 !important;

  overflow: hidden;
}


/* =========================================================
   MAIN CONTAINER
========================================================= */

.navigation-content {
  display: flex;
  flex-direction: column;

  height: 100%;

  padding: 0 17px;

  box-sizing: border-box;
}


/* =========================================================
   BRAND
========================================================= */

.brand-section {
  display: flex;
  align-items: center;

  min-height: 89px;

  gap: 13px;

  padding: 0 9px;
}

.brand-logo {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 44px;
  height: 44px;

  flex-shrink: 0;

  background: var(--orange);

  border-radius: 12px;

  color: white;

  box-shadow:
    0 8px 20px rgba(255, 121, 0, 0.25);
}

.brand-text {
  min-width: 0;
}

.brand-name {
  color: white;

  font-size: 18px;
  font-weight: 800;

  line-height: 1.1;

  letter-spacing: -0.03em;
}

.brand-name span {
  color: var(--orange);
}

.brand-subtitle {
  margin-top: 5px;

  color: #8ea1bf;

  font-size: 9px;
  font-weight: 800;

  letter-spacing: 0.12em;
}


/* =========================================================
   BRAND DIVIDER
========================================================= */

.brand-divider {
  height: 1px;

  margin: 0 -17px;

  background: rgba(255, 255, 255, 0.07);
}


/* =========================================================
   USER PROFILE CARD
========================================================= */

.user-card {
  display: flex;
  align-items: center;

  gap: 12px;

  margin-top: 18px;

  padding: 12px;

  background: var(--navy-card);

  border: 1px solid rgba(255, 255, 255, 0.07);

  border-radius: 12px;

  transition:
    background 0.2s ease,
    border-color 0.2s ease;
}

.user-card:hover {
  background: #192541;

  border-color: rgba(255, 121, 0, 0.18);
}


/* Avatar */

.user-avatar-wrapper {
  position: relative;

  flex-shrink: 0;
}

.user-avatar {
  background: #253452 !important;

  border: 2px solid var(--orange);

  color: white;
}

.avatar-letter {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;

  color: white;

  font-size: 19px;
  font-weight: 800;
}


/* Online indicator */

.online-indicator {
  position: absolute;

  right: -1px;
  bottom: 1px;

  width: 10px;
  height: 10px;

  background: #27c98a;

  border: 2px solid var(--navy-card);

  border-radius: 50%;
}


/* User information */

.user-details {
  min-width: 0;
}

.user-name {
  overflow: hidden;

  color: white;

  font-size: 13px;
  font-weight: 700;

  line-height: 1.3;

  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-role {
  margin-top: 3px;

  color: #8fa3c1;

  font-size: 10px;
  font-weight: 500;
}


/* =========================================================
   NAVIGATION
========================================================= */

.navigation-section {
  margin-top: 25px;
}

.navigation-heading {
  padding: 0 12px 9px;

  color: #647695;

  font-size: 10px;
  font-weight: 800;

  letter-spacing: 0.13em;
}

.navigation-list {
  padding: 0;
}


/* Individual item */

.navigation-item {
  position: relative;

  min-height: 45px;

  margin: 5px 0;

  padding-left: 9px;

  color: #92a6c5;

  transition:
    background 0.2s ease,
    color 0.2s ease,
    transform 0.2s ease;
}

.navigation-item:hover {
  background: rgba(255, 255, 255, 0.055);

  color: white;

  transform: translateX(2px);
}

.navigation-item :deep(.v-list-item__content) {
  padding: 0;
}

.navigation-item :deep(.v-list-item-title) {
  font-size: 13.5px;

  font-weight: 600;
}


/* Navigation icon */

.navigation-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 35px;
  height: 35px;

  margin-right: 8px;

  border-radius: 9px;

  background: transparent;

  color: #91a6c5;

  transition:
    background 0.2s ease,
    color 0.2s ease;
}

.navigation-item :deep(.v-icon) {
  color: #91a6c5;

  font-size: 20px;
}


/* =========================================================
   ACTIVE NAVIGATION
========================================================= */

.active-item {
  background: #1c2948 !important;

  color: white !important;

  box-shadow: none !important;
}


/* Orange vertical indicator */

.active-item::before {
  content: "";

  position: absolute;

  left: 0;

  top: 7px;
  bottom: 7px;

  width: 3px;

  background: var(--orange);

  border-radius: 0 4px 4px 0;
}


/* Active icon */

.active-item .navigation-icon {
  background: transparent;

  color: var(--orange);
}

.active-item :deep(.v-icon) {
  color: var(--orange) !important;
}

.active-item :deep(.v-list-item-title) {
  color: white !important;

  font-weight: 700;
}


/* Active arrow */

.active-arrow {
  margin-right: 3px;

  color: var(--orange) !important;
}


/* =========================================================
   BOTTOM SECTION
========================================================= */

.bottom-section {
  margin-top: auto;

  padding: 18px 0 16px;
}


/* =========================================================
   CHESSKWEEN CARD
========================================================= */

.chesskween-card {
  display: flex;
  align-items: center;

  gap: 11px;

  padding: 11px;

  margin-bottom: 10px;

  background: rgba(255, 255, 255, 0.045);

  border: 1px solid rgba(255, 255, 255, 0.06);

  border-radius: 11px;
}

.chesskween-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 37px;
  height: 37px;

  flex-shrink: 0;

  background: var(--orange);

  color: white;

  border-radius: 9px;
}

.chesskween-text {
  min-width: 0;
}

.chesskween-title {
  color: white;

  font-size: 11.5px;
  font-weight: 700;
}

.chesskween-subtitle {
  margin-top: 2px;

  color: #7184a1;

  font-size: 9.5px;
}


/* =========================================================
   LOGOUT
========================================================= */

.logout-button {
  min-height: 42px;

  color: #8ea1be !important;

  border: 1px solid rgba(255, 255, 255, 0.08);

  font-size: 12.5px;
  font-weight: 600;

  text-transform: none;

  transition:
    background 0.2s ease,
    color 0.2s ease,
    border-color 0.2s ease;
}

.logout-button:hover {
  background: rgba(255, 121, 0, 0.08);

  color: var(--orange) !important;

  border-color: rgba(255, 121, 0, 0.3);
}


/* =========================================================
   TABLET
========================================================= */

@media (max-width: 960px) {

  .side-navigation {
    width: 270px !important;
  }

  .navigation-content {
    padding-left: 15px;
    padding-right: 15px;
  }

  .brand-divider {
    margin-left: -15px;
    margin-right: -15px;
  }
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 600px) {

  .side-navigation {
    width: 250px !important;
  }

  .navigation-content {
    padding-left: 13px;
    padding-right: 13px;
  }

  .brand-divider {
    margin-left: -13px;
    margin-right: -13px;
  }

  .brand-section {
    min-height: 82px;
  }

  .brand-logo {
    width: 40px;
    height: 40px;
  }

  .brand-name {
    font-size: 16px;
  }

  .navigation-item {
    min-height: 43px;
  }

  .navigation-item :deep(.v-list-item-title) {
    font-size: 13px;
  }

  .user-card {
    padding: 10px;
  }

  .chesskween-card {
    padding: 10px;
  }
}
</style>