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
                <div class="filter-group">
                  <label for="name">Name: </label>
                  <select class="form-input-modal custom-select-modal" id="name" name="name" placeholder="Select User">
                    <option value>All Users</option>
                    <!-- {% for u in users %} -->
                    <option value="">sdsd</option>
                    <!-- {% endfor %} -->
                  </select>
                </div>

                <div class="filter-group">
                  <label for="action">Action: </label>
                  <select class="form-input-modal custom-select-modal" id="action" name="action"
                    placeholder="Select Action" data-searchable="true">
                    <option value>All Actions</option>
                    <option value="Change User Status">Change User Status</option>
                    <option value="Create Columns">Create Columns</option>
                    <option value="Create Config Group">Create Config Group</option>
                    <option value="Create Config Team">Create Config Team</option>
                    <option value="Create Custom Role">Create Custom Role</option>
                    <option value="Create Favorite">Create Favorite</option>
                    <option value="Create Favorite Search">Create Favorite Search</option>
                    <option value="Created User">Created User</option>
                    <option value="Delete Config Group">Delete Config Group</option>
                    <option value="Delete Config Team">Delete Config Team</option>
                    <option value="Delete Custom Role">Delete Custom Role</option>
                    <option value="Delete Favorite">Delete Favorite</option>
                    <option value="Delete User">Delete User</option>
                    <option value="Edit Favorite">Edit Favorite</option>
                    <option value="Login">Login</option>
                    <option value="Play audio">Play audio</option>
                    <option value="Save file">Save file</option>
                    <option value="Update Config Group">Update Config Group</option>
                    <option value="Update Config Team">Update Config Team</option>
                    <option value="Update Custom Role">Update Custom Role</option>
                    <option value="Update Favorite Search">Update Favorite Search</option>
                    <option value="Update User">Update User</option>
                  </select>
                </div>

                <div class="filter-group">
                  <label for="start_date">Start Date: </label>
                  <input type="text" class="form-input-modal datetimepicker" id="start_date" name="start_date"
                    autocomplete="off" placeholder="Start Date" />
                </div>
                <div class="filter-group">
                  <label for="end_date">End Date: </label>
                  <input type="text" class="form-input-modal datetimepicker" id="end_date" name="end_date"
                    autocomplete="off" placeholder="End Date" />
                </div>

                <div class="filter-group" style="flex: 0 0 auto;">
                  <button type="button" class="btn btn-light" id="resetFilterBtn"
                    style="height: 35px; border: 1px solid #e2e8f0;border-radius: 10px; ">
                    <i class="fas fa-undo"></i> Reset
                  </button>
                </div>

              </form>
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
              @per-change="setPerPage" />

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
import { API_AUDIO_LIST } from '../api/paths'

const searchQuery = ref('')
let searchTimeout = null

onMounted(() => {
  registerRequest(fetchData())
  document.addEventListener('click', onDocClick)
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

<style scoped>
  .filter-row { display: flex; gap: 15px; margin-bottom: 6px; align-items: center; flex-wrap: nowrap; width: 100%; }
  .filter-group { display: flex; flex-direction: row; gap: 10px; align-items: center; flex: 1; }
  .filter-group label { font-weight: 600; font-size: 14px; color: #64748b; margin-bottom: 0; white-space: nowrap; }
  .form-input-modal { height: 38px; border-radius: 8px; border: 1px solid #e2e8f0; padding: 0 12px; width: 100%; }
  .filter-group .custom-select-container { width: 100%; }
</style>