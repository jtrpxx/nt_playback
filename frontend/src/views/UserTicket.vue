<template>
    <MainLayout>
        <div class="main-wrapper container-fluid py-3">
            <Breadcrumbs :items="[{ text: 'Home', to: '/' }, { text: 'User Ticket' }]" />
            <div class="col-lg-12">
                <div class="card">
                    <div class="card-body card-body-datatable">
                        <div class="d-flex align-items-start justify-content-between" style="margin-bottom: 6px">
                            <div class="d-flex align-items-center">
                                <div class="d-flex align-items-center justify-content-center me-1"
                                    style="width: 35px; height: 35px; background-color: #d9e2f6; border-radius: 10px !important">
                                    <i class="fa-solid fa-user-clock" style="color: #2b6cb0; font-size: 18px"></i>
                                </div>
                                <h5 class="card-title mb-2 mt-1">User Ticket</h5>
                            </div>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div style="width:260px;">
                                    <SearchInput ref="searchInputRef" v-model="searchQuery" :placeholder="'Search...'" @typing="onTyping" @enter="onSearch" @clear="clearSearchQuery" />
                                </div>
                                <router-link v-if="authStore.hasPermission('Add User')" to="/user-management/add">
                                <button class="btn-role btn-primary btn-sm" id="addGroupBtn"
                                    @click.stop="openCreateGroup">
                                    <i class="fas fa-plus"></i>
                                    Add User
                                </button>
                                </router-link>
                            </div>
                        </div>
                        <TableTemplate
                            :columns="columns"
                            :rows="paginatedRecords"
                            :start-index="startIndex"
                            :loading="loading"
                            action-id-key="user.id"
                            :per-page="perPage"
                            :per-page-options="perPageOptions"
                            :current-page="currentPage"
                            :total-items="totalItems"
                            :sort-column="sortColumn"
                            :sort-direction="sortDirection"
                            @sort-change="onSortChange"
                            @page-change="changePage"
                            @per-change="setPerPage">

                            <template #cell-username="{ row }">
                                {{ row.user?.username || '' }}
                            </template>

                            <template #cell-full_name="{ row }">
                                {{ (row.user?.first_name || '') + ' ' + (row.user?.last_name || '') }}
                            </template>

                            <template #cell-role="{ row }">
                                <span class="role-badge other" >
                                    {{ row.permission }}
                                </span>
                            </template>                           

                            <template #cell-start_at="{ row }">
                                {{ row.start_at ? row.start_at.split('T')[0] : '-' }}
                            </template>

                            <template #cell-expire_at="{ row }">
                                {{ row.expire_at ? row.expire_at.split('T')[0] : '-' }}
                            </template>

                            <template #cell-phone="{ row }">
                                {{ row.phone || '-' }}
                            </template>

                            <template #cell-status="{ row }">
                                <span class="badge" :class="(row.is_active === true || row.is_active === 't') ? 'badge-success' : 'badge-danger'">
                                    {{ (row.is_active === true || row.is_active === 't') ? 'Active' : 'Expire' }}
                                </span>
                            </template>

                        </TableTemplate>

                    </div>
                </div>
            </div>
        </div>
    </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useAuthStore } from '../stores/auth.store'
import SearchInput from '../components/SearchInput.vue'
import MainLayout from '../layouts/MainLayout.vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'
import TableTemplate from '../components/TableTemplate.vue'
import { registerRequest } from '../utils/pageLoad'
import { API_GET_USER_TICKET } from '../api/paths'
import { showToast } from '../assets/js/function-all'

const searchQuery = ref('')
const searchInputRef = ref(null)
let searchTimeout = null

const perWrap = ref(null)
const perDropdownOpen = ref(false)

onMounted(() => {
    registerRequest(fetchData())
    try {
        const raw = localStorage.getItem('pending_toast')
        if (raw) {
            try {
                const t = JSON.parse(raw)
                if (t && t.message) showToast(t.message, t.type || 'success')
            } catch (e) { console.error('invalid pending_toast', e) }
            try { localStorage.removeItem('pending_toast') } catch (e) {}
        }
    } catch (e) { }

    try {
        const rawUser = localStorage.getItem('pending_user')
        if (rawUser) {
            try {
                const pu = JSON.parse(rawUser)
                try { window.__pending_user_for_user_management = pu } catch (e) { /* ignore */ }
            } catch (e) { console.error('invalid pending_user', e) }
            try { localStorage.removeItem('pending_user') } catch (e) {}
        }
    } catch (e) { }
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

function onSearch() {
    currentPage.value = 1
    if (searchTimeout) { clearTimeout(searchTimeout); searchTimeout = null }
    fetchData()
}

const perPageOptions = [50, 100, 500, 1000]
const perPage = ref(50)
const currentPage = ref(1)
const totalPages = computed(() => Math.max(1, Math.ceil(totalItems.value / perPage.value)))
const startIndex = computed(() => (currentPage.value - 1) * perPage.value)
const paginatedRecords = computed(() => records.value)

const sortColumn = ref('')
const sortDirection = ref('')

const onSortChange = ({ column, direction }) => {
  sortColumn.value = column
  sortDirection.value = direction
  fetchData()
}

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

const authStore = useAuthStore()

const columns = [
    { key: 'index', label: '#', isIndex: true, sortable: false },
    { key: 'username', label: 'Username' },
    { key: 'full_name', label: 'Full Name' },
    { key: 'role', label: 'Role' },
    { key: 'start_at', label: 'Start Date' },
    { key: 'expire_at', label: 'Expire Date' },
    { key: 'phone', label: 'Phone' },
    { key: 'status', label: 'Status' },
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

        if (sortColumn.value && sortDirection.value) {
            params.set('sort[0][field]', sortColumn.value)
            params.set('sort[0][dir]', sortDirection.value)
        }

        const res = await fetch(`${API_GET_USER_TICKET()}?${params.toString()}`, { credentials: 'include' })
        if (!res.ok) throw new Error('Failed to fetch')
        const json = await res.json()
        records.value = json.data || json.user_management || []
        totalItems.value = json.recordsFiltered ?? json.recordsTotal ?? (Array.isArray(records.value) ? records.value.length : 0)
        try {
            const pu = (typeof window !== 'undefined' && window.__pending_user_for_user_management) || null
            if (pu) {
                try {
                    // try to find by id first, then username
                    const findIdx = (records.value || []).findIndex(r => {
                        const rid = r && r.user && r.user.id
                        const rname = r && (r.user ? r.user.username : r.username)
                        if (pu.id && rid) return String(rid) === String(pu.id)
                        return String(rname || '').toLowerCase() === String(pu.username || '').toLowerCase()
                    })
                    let entry = null
                    if (findIdx !== -1) {
                        entry = records.value.splice(findIdx, 1)[0]
                    } else {
                        entry = {
                            id: pu.id || null,
                            user: {
                                id: pu.id || null,
                                username: pu.username || '',
                                first_name: pu.first_name || '',
                                last_name: pu.last_name || '',
                                email: pu.email || ''
                            },
                            phone: '',
                            start_at: null,
                            expire_at: null,
                            update_at: null,
                            is_active: true,
                            permission: pu.permission || '-',
                        }
                        if (pu.mode === 'add' && typeof totalItems.value === 'number') totalItems.value = totalItems.value + 1
                    }
                    records.value = [entry].concat(records.value || [])
                } catch (e) { console.error('apply pending user error', e) }
                try { delete window.__pending_user_for_user_management } catch (e) {}
            }
        } catch (e) { console.error('pending user apply top-level error', e) }
    } catch (e) {
        console.error('fetchData error', e)
    } finally {
        loading.value = false
    }
}

function clearSearchQuery() {
    searchQuery.value = ''
    sortColumn.value = ''
    sortDirection.value = ''
    if (searchTimeout) { clearTimeout(searchTimeout); searchTimeout = null }
    currentPage.value = 1
    fetchData()
    nextTick(() => {
        if (searchInputRef.value && typeof searchInputRef.value.focus === 'function') searchInputRef.value.focus()
    })
}


</script>

<style scoped>
div.dataTables_wrapper div.dataTables_length label {
    display: none;
}

.dataTables_scroll {
    border-bottom: 1px solid #e2e8f0;
}

.dataTables_filter {
    display: none !important;
}

/* switch_status CSS */
.switch_status {
    position: relative;
    display: inline-block;
    width: 80px;
    height: 23px
}

.switch_status input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider_status {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    background-color: #e6f4eeff;
    transition: 0.4s;
    border-radius: 34px;
}

.slider_status:before {
    position: absolute;
    content: "";
    height: 16px;
    width: 16px;
    left: 2px;
    bottom: 3px;
    left: 2px;
    bottom: 3.5px;
    background-color: white;
    transition: 0.4s;
    border-radius: 50%;
    z-index: 2;
}

.slider_status:after {
    content: "Inactive";
    color: #64748b;
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 11px;
    font-weight: 600;
    font-family: sans-serif;
}

input:checked+.slider_status {
    background-color: #2ecc71;
}

input:checked+.slider_status:before {
    transform: translateX(18px);
    transform: translateX(60px);
}

input:checked+.slider_status:after {
    content: "Active";
    left: 12px;
    right: auto;
    color: white;
}

.table-container {
    margin-top: 133px !important;
    margin-bottom: 20px !important;
}

.main-content {
    padding: 0px 16px 0px 11px;
}

div.dataTables_wrapper div.dataTables_info {
    padding-top: 5px !important;
}

div.dataTables_wrapper div.dataTables_paginate ul.pagination {
    margin: -5px 0;
}

.collapsible-toggle {
    background: transparent;
    border: none;
    /* color: #1e3a8a; */
    /* font-weight: 600; */
    cursor: pointer;
    padding: 0;
}

.collapsed-list {
    margin: 6px 0 0 12px;
    padding: 0;
    list-style: none;
    color: #374151;
}

.collapsed-list li {
    margin: 4px 0
}

/* Table sizing + horizontal scroll */
.card-body-datatable {
    overflow-x: auto;
}

.card-body-datatable table {
    min-width: 800px;
    /* ensure horizontal scroll when many columns */
    width: auto;
    border-collapse: separate;
}

.card-body-datatable table th,
.card-body-datatable table td {
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
}


/* Floating tooltip theme (match TableTemplate.vue) */
.group-summary {
    cursor: pointer;
}

.file-name-tooltip {
    position: fixed;
    display: inline-block;
    z-index: 9999;
    pointer-events: auto;
}

.file-name-tooltip .tooltip-inner {
    max-width: 760px;
    white-space: normal;
    overflow: visible;
    text-overflow: clip;
    color: #fff;
    font-size: 10px;
    background: rgba(0, 0, 0, 0.85);
    padding: 6px 8px;
    border-radius: 6px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
}

.file-name-tooltip .tooltip-arrow {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
}

.file-name-tooltip.tooltip-top .tooltip-arrow {
    bottom: -5px;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 6px solid rgba(0, 0, 0, 0.85);
}

.file-name-tooltip.tooltip-bottom .tooltip-arrow {
    top: -5px;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-bottom: 6px solid rgba(0, 0, 0, 0.85);
}

/* Hide Bootstrap's pseudo-element arrow to avoid a double-arrow effect */
.file-name-tooltip .tooltip-arrow::before {
    display: none !important;
}

.tooltip-after {
    font-weight: 600;
    margin-bottom: 6px;
    font-size: 12px;
    text-align: left;
}

.tooltip-after-list {
    margin: 0;
    padding: 0;
    list-style: none;
    color: inherit;
    text-align: left;
}

.group-summary.is-active-tooltip {
    background: rgba(0, 0, 0, 0.04);
    box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.06);
    border-radius: 3px;
}
</style>
