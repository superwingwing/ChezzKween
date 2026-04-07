<template>
  <div class="side-nav" :class="{ open: modelValue }">
    <div class="profile">
      <img :src="profile_pic || avatar_url" class="avatar" />
      <p>{{ firstName ? firstName + ' ' + lastName : full_name }}</p>
    </div>

    <button @click="navigateTo('search')">Search</button>
    <button @click="navigateTo('dashboard')">Home</button>
    <button @click="navigateTo('save')">Saved</button>
    <button @click="navigateTo('profile')">Profile</button>
    <button @click="navigateTo('about')">About ChessKween</button>

    <button class="signout" @click="onLogout">Sign out</button>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue"

const props = defineProps({
  modelValue: Boolean,
  profile_pic: String,
  avatar_url: { type: String, default: "default-avatar.png" },
  firstName: String,
  lastName: String,
  full_name: String,
})
const emit = defineEmits(["update:modelValue"])

function navigateTo(page) {
  alert("Navigate to " + page)
}
function onLogout() {
  alert("Logout clicked")
}
</script>

<style scoped>
.side-nav {
  width: 250px;
  background-color: #2e7d32;
  color: white;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
}
.side-nav button {
  margin: 0.5rem 0;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  cursor: pointer;
}
.side-nav .signout {
  margin-top: auto;
  background: rgba(255, 0, 0, 0.7);
}
.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: block;
  margin: 0 auto 1rem;
}
</style>