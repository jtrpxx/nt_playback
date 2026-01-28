<template>
    <MainLayout>
        <div class="main-wrapper container-fluid py-3">
        <Breadcrumbs :items="[{ text: 'Home', to: '/' }, { text: 'User Logs' }]" />
        <div class="col-lg-12">
          <div class="card">
            <div class="card-body card-body-datatable">
              <div class="d-flex align-items-start justify-content-between" style="margin-bottom: 6px;">
                <div class="d-flex align-items-center">
                  <div class="d-flex align-items-center justify-content-center me-1"
                    style="width:35px;height:35px;background-color: #D9E2F6;border-radius: 10px !important;">
                    <i class="fas fa-clipboard-check" style="color:#2b6cb0;font-size:18px"></i>
                  </div>
                  <h5 class="card-title mb-2 mt-1">User Logs</h5>
                </div>
                <div class="d-flex align-items-center">
                  <div class="search-group" style="width:260px; position:relative;">
                    <i class="fa-solid fa-magnifying-glass search-icon"></i>
                    <input v-model="searchQuery" type="text" class="form-control form-control-sm search-input"
                      placeholder="Search..." @input="onTyping" @keyup.enter="onSearch" />
                  </div>
                  <div class="ms-2 export-group">
                    <button type="button" class="btn btn-primary btn-sm export-icon" data-bs-toggle="dropdown"
                      aria-expanded="false">
                      <i class="fa-solid fa-download" style="color: #fff;"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end">
                      <li><button class="dropdown-item" type="button" @click="onExportFormat('pdf')">PDF</button></li>
                      <li><button class="dropdown-item" type="button" @click="onExportFormat('excel')">Excel</button>
                      </li>
                      <li><button class="dropdown-item" type="button" @click="onExportFormat('csv')">CSV</button></li>
                    </ul>
                  </div>
                </div>
              </div>

              <TableTemplate
                    :columns="columns"
                    :rows="paginatedRecords"
                    :start-index="startIndex"
                    :loading="loading"
                    call-direction-key="call_direction"
                    :per-page="perPage"
                    :per-page-options="perPageOptions"
                    :current-page="currentPage"
                    :total-items="totalItems"
                    @edit="onRowEdit"
                    @delete="onRowDelete"
                    @page-change="changePage"
                    @per-change="setPerPage"
                  />

              <!-- Content Audio Records-->
            </div>
          </div>
        </div>
        </div>
    </MainLayout>
</template>

<script setup>
import {  ref, computed, onMounted } from 'vue'

import MainLayout from '../layouts/MainLayout.vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'
import TableTemplate from '../components/TableTemplate.vue'
import { registerRequest } from '../utils/pageLoad'
import { API_AUDIO_LIST } from '../api/paths'

const searchQuery = ref('')
let searchTimeout = null

onMounted(() => {
    registerRequest(fetchData())
    document.addEventListener('click', onDocClick)
})

const onTyping = () => {
    currentPage.value = 1
    if (searchTimeout) clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
        fetchData()
        searchTimeout = null
    }, 450)
}

const perPageOptions = [50, 100, 500, 1000]
const perPage = ref(50)
const currentPage = ref(1)
const totalPages = computed(() => Math.max(1, Math.ceil(totalItems.value / perPage.value)))
const startIndex = computed(() => (currentPage.value - 1) * perPage.value)
const paginatedRecords = computed(() => records.value)

const setPerPage = (opt) => {
    perPage.value = opt
    perDropdownOpen.value = false
}

const changePage = async (p) => {
    if (p < 1) p = 1
    if (p > totalPages.value) p = totalPages.value
    currentPage.value = p
    await fetchData()
}

const onDocClick = (e) => {
    if (!perWrap.value) return
    if (!perWrap.value.contains(e.target)) perDropdownOpen.value = false
}

const onRowEdit = (row) => { console.log('edit row', row) }
const onRowDelete = (row) => { console.log('delete row', row) }

const expanded = ref(new Set())

const columns = [
    { key: 'index', label: '#', isIndex: true },
    { key: 'username', label: 'Username' },
    { key: 'full_name', label: 'Full Name' },
    { key: 'role', label: 'Role' },
    { key: 'group_team', label: 'Group/Team' },
    { key: 'database_servers', label: 'Database Server' },
    { key: 'phone', label: 'Phone' },
    { key: 'status', label: 'Status' },
    { key: 'actions', label: 'Actions', isAction: true }
]

const records = ref([])
const totalItems = ref(0)
const loading = ref(false)

const fetchData = async () => {
    loading.value = true
    try {
        const start = (currentPage.value - 1) * perPage.value
        const params = new URLSearchParams()
        params.set('draw', 1)
        params.set('start', start)
        params.set('length', perPage.value)
        params.set('search[value]', searchQuery.value || '')

        const res = await fetch(`${API_AUDIO_LIST()}?${params.toString()}`, { credentials: 'include' })
        if (!res.ok) throw new Error('Failed to fetch')
        const json = await res.json()
        records.value = json.data || json.user_management || []
        totalItems.value = json.recordsFiltered ?? json.recordsTotal ?? (Array.isArray(records.value) ? records.value.length : 0)
    } catch (e) {
        console.error('fetchData error', e)
    } finally {
        loading.value = false
    }
}

</script>