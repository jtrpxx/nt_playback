<template>
    <MainLayout>
        <div class="main-wrapper container-fluid py-3">
            <Breadcrumbs :items="[{ text: 'Home', to: '/' }, { text: 'Setting Column Audio Records' }]" />
            <div class="col-lg-12">
                <div class="card">
                    <div class="card-body card-body-datatable" style="position: relative;">
                        <div class="d-flex align-items-start justify-content-between" style="margin-bottom: 6px;">
                            <div class="d-flex align-items-center">
                                <div class="d-flex align-items-center justify-content-center me-1"
                                    style="width:35px;height:35px;background-color: #D9E2F6;border-radius: 10px !important;">
                                    <i class="fa-solid fa-gear" style="color:#2b6cb0;font-size:18px"></i>
                                </div>
                                <h5 class="card-title mb-2 mt-1">Setting Column Audio Records</h5>
                            </div>
                            <div class="d-flex align-items-center">
                                <div style="width:260px;">
                                    <SearchInput ref="searchInputRef" v-model="searchQuery" :placeholder="'Search...'" @typing="onSearch" @clear="clearSearchQuery" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'

import MainLayout from '../layouts/MainLayout.vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'
import TableTemplate from '../components/TableTemplate.vue'


const onSearch = () => {
  currentPage.value = 1
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchData()
    searchTimeout = null
  }, 450)
}
function clearSearchQuery() {
  searchQuery.value = ''
  if (searchTimeout) { clearTimeout(searchTimeout); searchTimeout = null }
  currentPage.value = 1
  fetchData()
  nextTick(() => {
    if (searchInputRef.value && typeof searchInputRef.value.focus === 'function') searchInputRef.value.focus()
  })
}
</script>