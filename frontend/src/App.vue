<template>
  <!-- จุดที่จะแสดงผลหน้า Login, Home, Dashboard ตาม URL -->
  <router-view :key="route.fullPath" />
</template>

<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
</script>
