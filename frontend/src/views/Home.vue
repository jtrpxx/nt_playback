<template>
  <div class="home">
    <div class="home__container">
      <h1 class="home__title">Welcome to NT Playback</h1>
      <p class="home__subtitle">ยินดีต้อนรับคุณ: {{ authStore.fullName() || 'Guest' }}</p>
      <button @click="logout" style="margin-top: 20px; padding: 10px 20px;">ออกจากระบบ</button>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth.store'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.clear()
  router.push('/login')
}
</script>

<style scoped>
.home {
	display: flex;
	align-items: center;
	justify-content: center;
	min-height: 60vh;
	padding: 6rem 2rem 2rem; /* top padding to account for navbar */
	box-sizing: border-box;
}
.home__container {
	text-align: center;
	max-width: 720px;
}
.home__title {
	font-size: 2rem;
	margin: 0 0 0.5rem 0;
}
.home__subtitle {
	color: #6b7280;
	margin: 0;
}
</style>
