<template>
  <div class="page-title text-primary-d2 text-140" style="font-size: 12px; margin-bottom: 12px">
    <template v-for="(crumb, idx) in items" :key="idx">
      <small v-if="idx === 0" :style="{ color: idx === activeIndex ? '#416FD6' : '#6c757d', marginRight: '-4px' }">
        <router-link :to="crumb.to || '/'" class="no-link"><i class="fa-solid fa-house" :style="{ color: idx === activeIndex ? '#416FD6' : '#6c757d' }"></i> {{ crumb.text }}</router-link>
      </small>

      <small v-else-if="crumb.to" :style="{ color: idx === activeIndex ? '#416FD6' : '#6c757d', marginRight: '-4px' }">
        <router-link :to="crumb.to" class="no-link"><i class="fa-solid fa-angle-right" :style="{ color: idx === activeIndex ? '#416FD6' : '#6c757d' }"></i> {{ crumb.text }}</router-link>
      </small>

      <small v-else :style="{ color: idx === activeIndex ? '#416FD6' : '#6c757d' }" class="page-info text-dark-m3"> <i class="fa-solid fa-angle-right" :style="{ color: idx === activeIndex ? '#416FD6' : '#6c757d' }"></i> {{ crumb.text }}</small>
    </template>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => [{ text: 'Home', to: '/' }]
  }
})

const items = props.items
const activeIndex = computed(() => Math.max(0, (items && items.length ? items.length - 1 : 0)))
</script>

<style scoped>
.no-link { text-decoration: none; color: inherit }
</style>
