<template>
  <div class="layout-wrapper">
    <Navbar />
    
    <main class="main-content">
      <slot />
    </main>

    <footer class="footer">
      <div class="container-fluid text-center justify-content-center">
        <span class="text-muted">© 2026 <a href="https://nichetelcomm.com/" target="_blabk">Nichetel Co., Ltd.</a> All rights reserved.</span>
      </div>
    </footer>

    
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
</script>

<style scoped>

</style>
