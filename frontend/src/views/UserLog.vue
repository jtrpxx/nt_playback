<template>
  <MainLayout>
    <div class="main-wrapper container-fluid py-3">
      <Breadcrumbs :items="[{ text: 'Home', to: '/' }, { text: 'User Logs' }]" />
      <div class="col-lg-12">
        <div class="card">
          <div class="card-body card-body-datatable" style="position: relative;">
            <div class="d-flex align-items-start justify-content-between" style="margin-bottom: 6px;">
              <div class="d-flex align-items-center">
                <div class="d-flex align-items-center justify-content-center me-1"
                  style="width:35px;height:35px;background-color: #D9E2F6;border-radius: 10px !important;">
                  <i class="fas fa-clipboard-check" style="color:#2b6cb0;font-size:18px"></i>
                </div>
                <h5 class="card-title mb-2 mt-1">{{ cardTitle }}</h5>
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

            <div>
              <form id="filterForm" class="filter-row">

                <div class="input-group" >
                  <CustomSelect class="select-search select-checkbox" v-model="filters.name"
                    :options="userOptions"
                    placeholder="Select User" name="name" />
                </div>


                <div class="input-group" >
                  <CustomSelect class="select-search select-checkbox" v-model="filters.action"
                    :options="actionOptions"
                    placeholder="Select Action" name="action" />
                </div>


                <div :class="['input-group', { 'has-value': !!filters.start_date }]">
                  <input ref="startInput" v-flatpickr="{ target: filters, key: 'start_date' }" required type="text"
                    name="start_date"
                    autocomplete="off" class="input">
                  <label class="floating-label">Start Date</label>
                  <span class="calendar-icon" @click="startInput && startInput.focus()"><i
                      class="fa-regular fa-calendar"></i></span>
                </div>
                <div :class="['input-group', { 'has-value': !!filters.end_date }]">
                  <input ref="endInput" v-flatpickr="{ target: filters, key: 'end_date' }" required type="text"
                    name="end_date"
                    autocomplete="off" class="input">
                  <label class="floating-label">End Date</label>
                  <span class="calendar-icon" @click="endInput && endInput.focus()"><i
                      class="fa-regular fa-calendar"></i></span>
                </div>


                <div class="input-group" style="flex: 0 0 auto;">
                  <button type="button" class="btn btn-light" id="resetFilterBtn"
                    style="height: 31px; border: 1px solid #e2e8f0;border-radius: 10px;font-size: 12px;margin-top: -7px;">
                    <i class="fas fa-undo"></i> Reset
                  </button>
                </div>

              </form>
            </div>

            <div class="table-area">
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
              @per-change="setPerPage" />
            </div>

            <!-- Content Audio Records-->
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

import MainLayout from '../layouts/MainLayout.vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'
import TableTemplate from '../components/TableTemplate.vue'
import CustomSelect from '../components/CustomSelect.vue'
import { registerRequest } from '../utils/pageLoad'
import {  API_GET_LOG_USER } from '../api/paths'

const searchQuery = ref('')
let searchTimeout = null

onMounted(() => {
  registerRequest(fetchData())
  document.addEventListener('click', onDocClick)
})

const type = computed(() => {
  const p = route.path || ''
  if (p === '/logs/system') return 'system'
  if (p === '/logs/audit') return 'audit'
  return 'user'
})

const route = useRoute()
const cardTitle = computed(() => {
  const p = route.path || ''
  if (p === '/logs/system') return 'System log'
  if (p === '/logs/audit') return 'Audit log'
  return 'User Logs'
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

// filter state
import { reactive } from 'vue'
const filters = reactive({ name: '', action: '', start_date: '', end_date: '' })
const userOptions = ref([])
const actionOptions = ref([
  { label: 'All Actions', value: '' },
  { label: 'Change User Status', value: 'Change User Status' },
  { label: 'Create Columns', value: 'Create Columns' },
  { label: 'Create Config Group', value: 'Create Config Group' },
  { label: 'Create Config Team', value: 'Create Config Team' },
  { label: 'Create Custom Role', value: 'Create Custom Role' },
  { label: 'Create Favorite', value: 'Create Favorite' },
  { label: 'Create Favorite Search', value: 'Create Favorite Search' },
  { label: 'Created User', value: 'Created User' },
  { label: 'Delete Config Group', value: 'Delete Config Group' },
  { label: 'Delete Config Team', value: 'Delete Config Team' },
  { label: 'Delete Custom Role', value: 'Delete Custom Role' },
  { label: 'Delete Favorite', value: 'Delete Favorite' },
  { label: 'Delete User', value: 'Delete User' },
  { label: 'Edit Favorite', value: 'Edit Favorite' },
  { label: 'Login', value: 'Login' },
  { label: 'Play audio', value: 'Play audio' },
  { label: 'Save file', value: 'Save file' },
  { label: 'Update Config Group', value: 'Update Config Group' },
  { label: 'Update Config Team', value: 'Update Config Team' },
  { label: 'Update Custom Role', value: 'Update Custom Role' },
  { label: 'Update Favorite Search', value: 'Update Favorite Search' },
  { label: 'Update User', value: 'Update User' }
])

// flatpickr refs
const startInput = ref(null)
const endInput = ref(null)

// small helpers for dropdown handling (prevent undefined errors)
const perWrap = ref(null)
const perDropdownOpen = ref(false)

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
  { key: 'index', label: '#', isIndex: true,width: '5%' },
  { key: 'username', label: 'Username',width: '15%'  },
  { key: 'full_name', label: 'Full Name' ,width: '15%' },
  { key: 'action', label: 'Action',width: '5%'  },
  { key: 'status', label: 'Status',width: '5%' },
  { key: 'detail', label: 'Description' , tooltip: true,width: '20%',},
  { key: 'ip_address', label: 'IP Address',width: '10%'},
  { key: 'timestamp', label: 'Timestamp',width: '10%', },
  { key: 'client_type', label: 'Client type',width: '15%' }
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
    if (filters.name) params.set('name', filters.name)
    if (filters.action) params.set('action', filters.action)
    if (filters.start_date) params.set('start_date', filters.start_date)
    if (filters.end_date) params.set('end_date', filters.end_date)

    const res = await fetch(`${API_GET_LOG_USER(type.value)}?${params.toString()}`, { credentials: 'include' })
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

<style scoped>

.filter-row {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: nowrap;
  width: 100%;
}

.input-group {
  display: flex;
  flex-direction: row;
  gap: 10px;
  align-items: center;
  flex: 1 1;
}


.form-input-modal {
  height: 38px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  padding: 0 12px;
  width: 100%;
}

.input-group .custom-select-container {
  width: 100%;
}

/* make floating-label behave like CustomSelect for inputs */
.input-group .floating-label {
  position: absolute;
  left: 16px;
  top: 16px;
  transform: translateY(-50%);
  font-size: clamp(12px, 1.2vw, 13px);
  color: #6c757d;
  pointer-events: none;
  transition: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  background: white;
  padding: 0 0.2em;
  transform-origin: left center;
}
.input:focus ~ .floating-label,
.input-group.has-value .floating-label {
  transform: translateY(-125%) scale(0.8);
  color: #416fd6;
}

@media (min-width: 1200px) {
    :deep(.card-body-datatable .table-container .table-scroll) {
        max-height: calc(100vh - 316px) !important;
    }
}
</style>