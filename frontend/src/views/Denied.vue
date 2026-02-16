<template>
  <MainLayout>
    <div class="main-wrapper-container">
      <Breadcrumbs :items="[{ text: 'Home', to: '/' }, { text: 'Access Denied' }]" />

      <div class="error-container">
        <div class="error-content">
          <div class="icon-wrapper">
            <img src="/src/assets/images/denied.png" alt="Access Denied" style="max-width: 100%; height: auto; max-height: 300px;">
          </div>
          
          <p class="error-text">
            Sorry, this page is for authorized ears only! You don't have the required<br>
            permisions to access to the page. 
          </p>

          <router-link to="/" class="btn btn-outline-primary">
            <i class="fa-solid fa-house"></i>
            Return to Home
          </router-link>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import MainLayout from '../layouts/MainLayout.vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'
</script>

<style scoped>
.main-wrapper-container {
    padding: 16px 12px;
    display: flex;
    flex-direction: column;
    margin-bottom: -18px;
    min-height: calc(100vh - 109px);
}
.error-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 240px;
}

.error-content {
  text-align: center;
  max-width: 600px;
}

.icon-wrapper {
  position: relative;
  display: inline-block;
  margin-bottom: 1.5rem;
}

.error-code {
  font-size: 5rem;
  font-weight: 800;
  color: #416FD6;
  line-height: 1;
  margin: 0;
  letter-spacing: -2px;
}

.error-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3748;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
}

.error-text {
  color: #718096;
  margin-bottom: 2rem;
  line-height: 1.6;
}


</style>
