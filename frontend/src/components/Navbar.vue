<template>
  <header class="nt-navbar">
    <div class="nt-navbar__inner">
      <router-link class="nt-navbar__brand" to="/">
        <img class="nt-navbar__logo" src="/logo.png" alt="logo" />
        <div class="nt-navbar__title">NT Audio Search</div>
        <div class="nt-navbar__subtitle">Centralized Search and Playback System</div>
      </router-link>

      <nav class="nt-navbar__nav">
        <ul class="nt-navbar__links">
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/users">Users</router-link></li>
          <li><router-link to="/dashboard">Dashboard</router-link></li>
        </ul>

        <div class="nt-navbar__user" @click="toggleMenu">
          <div class="nt-navbar__avatar">{{ initials }}</div>
          <span class="nt-navbar__name">{{ displayName }}</span>
          <i class="caret">▾</i>
        </div>
      </nav>
    </div>

    <div v-if="menuOpen" class="nt-navbar__menu">
      <router-link to="/profile">Profile</router-link>
      <router-link to="/settings">Settings</router-link>
      <a href="#/logout">Logout</a>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth.store'
import '../assets/css/navbar.css'
import { useRouter } from 'vue-router'

const store = useAuthStore()
const router = useRouter()

const menuOpen = ref(false)
function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

const displayName = computed(() => store.user?.fullName ?? 'Guest User')
const initials = computed(() => {
  const name = store.user?.fullName || 'U'
  return name
    .split(' ')
    .map(s => s[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
})
</script>

<style scoped>
/* small fallback if navbar.css not loaded */
.nt-navbar { background: #fff; border-bottom: 1px solid #e5e7eb; position: sticky; top: 0; z-index: 50; }
.nt-navbar__inner { display:flex; align-items:center; justify-content:space-between; padding:12px 20px; max-width:1200px; margin:0 auto; }
.nt-navbar__brand { display:flex; align-items:center; gap:12px; text-decoration:none; color:inherit }
.nt-navbar__logo { width:36px; height:36px; object-fit:cover; border-radius:6px }
.nt-navbar__title { font-weight:600 }
.nt-navbar__subtitle { font-size:12px; color:#6b7280 }
.nt-navbar__links { list-style:none; display:flex; gap:12px; margin:0; padding:0 }
.nt-navbar__links a { text-decoration:none; color:#111827 }
.nt-navbar__user { display:flex; align-items:center; gap:8px; cursor:pointer }
.nt-navbar__avatar { width:32px; height:32px; background:#3F6ACF; color:#fff; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700 }
.nt-navbar__menu { position:absolute; right:20px; top:64px; background:#fff; box-shadow:0 6px 20px rgba(0,0,0,0.08); border-radius:8px; padding:8px; display:flex; flex-direction:column; gap:6px }
</style>