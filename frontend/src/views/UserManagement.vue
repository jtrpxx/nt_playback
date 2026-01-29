<template>
    <MainLayout>
        <div class="main-wrapper container-fluid py-3">
            <Breadcrumbs :items="[{ text: 'Home', to: '/' }, { text: 'User Management' }]" />
            <div class="col-lg-12">
                <div class="card">
                    <div class="card-body card-body-datatable">
                        <div class="d-flex align-items-start justify-content-between" style="margin-bottom: 6px">
                            <div class="d-flex align-items-center">
                                <div class="d-flex align-items-center justify-content-center me-1"
                                    style="width: 35px; height: 35px; background-color: #d9e2f6; border-radius: 10px !important">
                                    <i class="fas fa-users" style="color: #2b6cb0; font-size: 18px"></i>
                                </div>
                                <h5 class="card-title mb-2 mt-1">User Management</h5>
                            </div>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div class="search-group" style="width:260px; position:relative;">
                                    <i class="fa-solid fa-magnifying-glass search-icon"></i>
                                    <input v-model="searchQuery" type="text"
                                        class="form-control form-control-sm search-input"
                                        placeholder="Search..." @input="onTyping" @keyup.enter="onSearch" />
                                </div>
                                <button class="btn-role btn-primary btn-sm" id="addGroupBtn"
                                    @click.stop="openCreateGroup">
                                    <i class="fas fa-plus"></i>
                                    Add User
                                </button>
                            </div>
                        </div>
                        <TableTemplate
                            :columns="columns"
                            :rows="paginatedRecords"
                            :start-index="startIndex"
                            :loading="loading"
                            :per-page="perPage"
                            :per-page-options="perPageOptions"
                            :current-page="currentPage"
                            :total-items="totalItems"
                            @edit="onRowEdit"
                            @delete="onRowDelete"
                            @page-change="changePage"
                            @per-change="setPerPage">

                            <template #cell-username="{ row }">
                                {{ row.user?.username || '' }}
                            </template>

                            <template #cell-full_name="{ row }">
                                {{ (row.user?.first_name || '') + ' ' + (row.user?.last_name || '') }}
                            </template>

                            <template #cell-role="{ row }">
                                <span
                                    :class="['role-badge', (['administrator', 'auditor', 'operator'].includes((row.permission || '').toLowerCase()) ? (row.permission || '').toLowerCase() : 'other')]">
                                    {{ row.permission || '-' }}
                                </span>
                            </template>

                            <template #cell-group_team="{ row }">
                                <div>
                                    <template v-if="getGroupTeamList(row).length === 0">
                                        -
                                    </template>
                                    <template v-else>
                                        <button class="collapsible-toggle" @click="toggleExpand(row.id, 'group')">
                                            <span v-if="!isExpanded(row.id, 'group')"><i class="fa-solid fa-caret-right"></i></span>
                                            <span v-else><i class="fa-solid fa-caret-down"></i></span>
                                            {{ getGroupTeamSummary(row) }}
                                        </button>
                                        <ul v-if="isExpanded(row.id, 'group')" class="collapsed-list">
                                            <li v-for="(g, gi) in getGroupTeamList(row)" :key="gi">- {{ g }}</li>
                                        </ul>
                                    </template>
                                </div>
                            </template>

                            <template #cell-database_servers="{ row }">
                                <div>
                                    <template v-if="getDbList(row).length <= 1">
                                        {{ getDbList(row)[0] || '-' }}
                                    </template>
                                    <template v-else>
                                        <button class="collapsible-toggle" @click="toggleExpand(row.id, 'db')">
                                            <span v-if="!isExpanded(row.id, 'db')"><i class="fa-solid fa-caret-right"></i></span>
                                            <span v-else><i class="fa-solid fa-caret-down"></i></span>
                                            DB ({{ getDbList(row).length }})
                                        </button>
                                        <ul v-if="isExpanded(row.id, 'db')" class="collapsed-list">
                                            <li v-for="(d, di) in getDbList(row)" :key="di">- {{ d }}</li>
                                        </ul>
                                    </template>
                                </div>
                            </template>

                            <template #cell-phone="{ row }">
                                {{ row.phone || '-' }}
                            </template>

                            <template #cell-status="{ row }">
                                <label class="switch_status">
                                    <input type="checkbox" :checked="row.is_active"
                                        @change="() => toggleUserStatus(row.user?.id, row)" />
                                    <span class="slider_status round"></span>
                                </label>
                            </template>

                        </TableTemplate>

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
import { API_GET_USER, API_USER_MANAGEMENT_CHANGE_STATUS } from '../api/paths'

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

function toggleExpand(rowId, key) {
    const id = `${rowId}-${key}`
    if (expanded.value.has(id)) expanded.value.delete(id)
    else expanded.value.add(id)
    // force update
    expanded.value = new Set(expanded.value)
}

function isExpanded(rowId, key) {
    return expanded.value.has(`${rowId}-${key}`)
}

function getGroupTeamPairs(row) {
    // returns array of { group, team }
    if (!row) return []
    const out = []
    if (Array.isArray(row.team) && row.team.length) {
        for (const t of row.team) {
            const group = (t.user_group && (t.user_group.group_name || t.user_group)) || t.user_group || ''
            const team = t.name || t.team_name || ''
            out.push({ group: group || '', team: team || '' })
        }
        return out.filter(p => p.group || p.team)
    }
    if (row.team && row.team.user_group) {
        const group = row.team.user_group.group_name || row.team.user_group || ''
        const team = row.team.name || ''
        return [{ group: group || '', team: team || '' }].filter(p => p.group || p.team)
    }
    if (row.group_team && typeof row.group_team === 'string') {
        return row.group_team.split(',').map(s => s.trim()).filter(Boolean).map(item => {
            if (item.includes(' / ')) {
                const parts = item.split(' / ')
                return { group: parts[0].trim(), team: parts[1].trim() }
            }
            // no explicit group; treat as team only
            return { group: '', team: item }
        }).filter(p => p.group || p.team)
    }
    return []
}

function getGroupTeamList(row) {
    // backward-compatible: return team names
    return getGroupTeamPairs(row).map(p => (p.team ? p.team : (p.group || '')))
}

function getGroupTeamSummary(row) {
    const pairs = getGroupTeamPairs(row)
    if (!pairs.length) return '-'
    const groups = [...new Set(pairs.map(p => (p.group || '').trim()).filter(Boolean))]
    const summary = groups.length ? groups[0] : (pairs[0].team || '-')
    // if only one pair, don't show count per request
    if (pairs.length === 1) return summary
    return `${summary} (${pairs.length})`
}

function getDbList(row) {
    if (!row) return []
    if (Array.isArray(row.database_servers)) return row.database_servers
    if (!row.database_servers) return []
    if (typeof row.database_servers === 'string') {
        // special ALL
        if (row.database_servers === 'ALL') return ['ALL']
        return row.database_servers.split(',').map(s => s.trim()).filter(Boolean)
    }
    return []
}

async function toggleUserStatus(userId, row) {
    if (!userId) return
    try {
        const rec = records.value.find(r => (r.user && r.user.id) === userId)
        if (!rec) return
        const current = !!rec.user.is_active
        // optimistic
        rec.user.is_active = !current
        try {
            const res = await fetch(API_USER_MANAGEMENT_CHANGE_STATUS(userId), { method: 'POST', credentials: 'include' })
            const json = await res.json()
            if (!res.ok || json.status === 'error') {
                rec.user.is_active = current
                console.error('change status failed', json)
            }
        } catch (e) {
            rec.user.is_active = current
            console.error('toggleUserStatus fetch error', e)
        }
    } catch (e) {
        console.error('toggleUserStatus error', e)
    }
}

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

        const res = await fetch(`${API_GET_USER()}?${params.toString()}`, { credentials: 'include' })
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

.role-badge {
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px
}

.role-badge.administrator {
    background: rgba(239, 68, 68, 0.1);
    color: #dc2626
}

.role-badge.auditor {
    background: rgba(16, 185, 129, 0.1);
    color: #059669;
}

.role-badge.operator {
    background: rgba(65, 111, 214, 0.1);
    color: #416fd6;
}

.role-badge.other {
    background: #e5e7eb;
    color: #374151
}

/* Table sizing + horizontal scroll */
.card-body-datatable {
    overflow-x: auto;
}
.card-body-datatable table {
    min-width: 800px; /* ensure horizontal scroll when many columns */
    width: auto;
    border-collapse: separate;
}
.card-body-datatable table th,
.card-body-datatable table td {
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
}

</style>