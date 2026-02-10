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
                                <div style="width:260px;">
                                    <SearchInput ref="searchInputRef" v-model="searchQuery" :placeholder="'Search...'" @typing="onTyping" @enter="onSearch" @clear="clearSearchQuery" />
                                </div>
                                <router-link to="/user-management/add">
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
                                <template v-if="getGroupTeamList(row).length === 0">
                                    -
                                </template>
                                <template v-else>
                                    <span class="group-summary" @mouseenter="showGroupTooltip($event, row)"
                                        @mouseleave="hideGroupTooltip">
                                        {{ getGroupTeamSummary(row) }}
                                    </span>
                                </template>
                            </template>

                            <template #cell-database_servers="{ row }">
                                <template v-if="getDbList(row).length <= 1">
                                    {{ getDbList(row)[0] || '-' }}
                                </template>
                                <template v-else>
                                    <span class="group-summary" @mouseenter="showDbTooltip($event, row)"
                                        @mouseleave="hideDbTooltip">
                                        Database Server ({{ getDbList(row).length }})
                                    </span>
                                </template>
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

                        <teleport to="body">
                            <div v-if="groupTooltip.visible" ref="groupTooltipEl"
                                class="file-name-tooltip tooltip bs-tooltip-top show"
                                :class="groupTooltipPlacement === 'top' ? 'tooltip-top' : 'tooltip-bottom'"
                                :style="groupTooltip.style"
                                @mouseenter="cancelHideGroup" @mouseleave="hideGroupTooltip">
                                <div class="tooltip-arrow"></div>
                                <div class="tooltip-inner d-flex flex-column">
                                    <div class="tooltip-after">Team</div>
                                    <ul class="tooltip-after-list">
                                        <li v-for="(g, gi) in groupTooltip.items" :key="gi" style="margin:2px 0">- {{ g
                                        }}</li>
                                    </ul>
                                </div>
                            </div>

                            <div v-if="dbTooltip.visible" ref="dbTooltipEl"
                                class="file-name-tooltip tooltip bs-tooltip-top show"
                                :class="dbTooltipPlacement === 'top' ? 'tooltip-top' : 'tooltip-bottom'"
                                :style="dbTooltip.style"
                                @mouseenter="cancelHideDb" @mouseleave="hideDbTooltip">
                                <div class="tooltip-arrow"></div>
                                <div class="tooltip-inner d-flex flex-column">
                                    <div class="tooltip-after">Database Server</div>
                                    <ul class="tooltip-after-list">
                                        <li v-for="(d, di) in dbTooltip.items" :key="di" style="margin:2px 0">- {{ d }}
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </teleport>

                    </div>
                </div>
            </div>
        </div>
    </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import SearchInput from '../components/SearchInput.vue'
import MainLayout from '../layouts/MainLayout.vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'
import TableTemplate from '../components/TableTemplate.vue'
import { registerRequest } from '../utils/pageLoad'
import { API_GET_USER, API_USER_MANAGEMENT_CHANGE_STATUS } from '../api/paths'
import { showToast } from '../assets/js/function-all'
import { ensureCsrf, getCsrfToken } from '../api/csrf'

const searchQuery = ref('')
const searchInputRef = ref(null)
let searchTimeout = null

// dropdown state used by the table per-page control


onMounted(() => {
    registerRequest(fetchData())
    // show pending toast (if any) persisted by previous page
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

const router = useRouter()

const onRowEdit = (row, actionId) => {
    const id = actionId ?? (row && row.user && row.user.id)
    if (!id) {
        console.warn('onRowEdit: no id available for row', row)
        return
    }
    router.push(`/user-management/edit/${id}`)
}

const onRowDelete = (row, actionId) => { console.log('delete row', row, actionId) }

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

// tooltip state for group/team
const groupTooltip = ref({ visible: false, items: [], style: null })
const groupTooltipEl = ref(null)
const groupTooltipPlacement = ref('top')
let groupHideTimer = null
const groupActiveEl = ref(null)

// tooltip state for database servers
const dbTooltip = ref({ visible: false, items: [], style: null })
const dbTooltipEl = ref(null)
const dbTooltipPlacement = ref('top')
let dbHideTimer = null
const dbActiveEl = ref(null)

function showGroupTooltip(e, row) {
    try {
        const items = getGroupTeamList(row)
        if (!items || items.length === 0) return
        if (groupHideTimer) { clearTimeout(groupHideTimer); groupHideTimer = null }
        // mark the trigger element so it can be styled while tooltip is visible
        try {
            const currentTarget = e.currentTarget
            if (groupActiveEl.value && groupActiveEl.value !== currentTarget) {
                groupActiveEl.value.classList.remove('is-active-tooltip')
            }
            groupActiveEl.value = currentTarget
            if (groupActiveEl.value && groupActiveEl.value.classList) groupActiveEl.value.classList.add('is-active-tooltip')
        } catch (err) { /* ignore if element unavailable */ }
        groupTooltip.value.items = items
        groupTooltip.value.visible = true
        const rect = e.currentTarget.getBoundingClientRect()
        nextTick(() => {
            try {
                const el = groupTooltipEl.value
                if (!el) return
                const tRect = el.getBoundingClientRect()
                const spaceAbove = rect.top
                const left = rect.left + rect.width / 2
                let top
                let transform
                if (spaceAbove > tRect.height + 8) {
                    top = rect.top - 8
                    transform = 'translate(-50%, -100%)'
                    groupTooltipPlacement.value = 'top'
                } else {
                    top = rect.bottom + 8
                    transform = 'translate(-50%, 0)'
                    groupTooltipPlacement.value = 'bottom'
                }
                groupTooltip.value.style = {
                    position: 'fixed',
                    left: `${left}px`,
                    top: `${top}px`,
                    transform,
                    zIndex: 9999,
                    maxWidth: '420px',
                    whiteSpace: 'normal'
                }
            } catch (err) { console.error('group tooltip pos err', err) }
        })
    } catch (e) {
        console.error('showGroupTooltip error', e)
    }
}

function hideGroupTooltip() {
    if (groupHideTimer) clearTimeout(groupHideTimer)
    groupHideTimer = setTimeout(() => {
        groupTooltip.value.visible = false
        groupTooltip.value.items = []
        groupTooltip.value.style = null
        // remove active styling from the trigger element
        try {
            if (groupActiveEl.value && groupActiveEl.value.classList) groupActiveEl.value.classList.remove('is-active-tooltip')
        } catch (err) { }
        groupActiveEl.value = null
        groupHideTimer = null
    }, 120)
}

function cancelHideGroup() { if (groupHideTimer) { clearTimeout(groupHideTimer); groupHideTimer = null } }

function showDbTooltip(e, row) {
    try {
        const items = getDbList(row)
        if (!items || items.length === 0) return
        if (dbHideTimer) { clearTimeout(dbHideTimer); dbHideTimer = null }
        // mark the trigger element so it can be styled while tooltip is visible
        try {
            const currentTarget = e.currentTarget
            if (dbActiveEl.value && dbActiveEl.value !== currentTarget) {
                dbActiveEl.value.classList.remove('is-active-tooltip')
            }
            dbActiveEl.value = currentTarget
            if (dbActiveEl.value && dbActiveEl.value.classList) dbActiveEl.value.classList.add('is-active-tooltip')
        } catch (err) { /* ignore if element unavailable */ }
        dbTooltip.value.items = items
        dbTooltip.value.visible = true
        const rect = e.currentTarget.getBoundingClientRect()
        nextTick(() => {
            try {
                const el = dbTooltipEl.value
                if (!el) return
                const tRect = el.getBoundingClientRect()
                const spaceAbove = rect.top
                const left = rect.left + rect.width / 2
                let top
                let transform
                if (spaceAbove > tRect.height + 8) {
                    top = rect.top - 8
                    transform = 'translate(-50%, -100%)'
                    dbTooltipPlacement.value = 'top'
                } else {
                    top = rect.bottom + 8
                    transform = 'translate(-50%, 0)'
                    dbTooltipPlacement.value = 'bottom'
                }
                dbTooltip.value.style = {
                    position: 'fixed',
                    left: `${left}px`,
                    top: `${top}px`,
                    transform,
                    zIndex: 9999,
                    maxWidth: '420px',
                    whiteSpace: 'normal'
                }
            } catch (err) { console.error('db tooltip pos err', err) }
        })
    } catch (e) {
        console.error('showDbTooltip error', e)
    }
}

function hideDbTooltip() {
    if (dbHideTimer) clearTimeout(dbHideTimer)
    dbHideTimer = setTimeout(() => {
        dbTooltip.value.visible = false
        dbTooltip.value.items = []
        dbTooltip.value.style = null
        // remove active styling from the trigger element
        try {
            if (dbActiveEl.value && dbActiveEl.value.classList) dbActiveEl.value.classList.remove('is-active-tooltip')
        } catch (err) { }
        dbActiveEl.value = null
        dbHideTimer = null
    }, 120)
}

function cancelHideDb() { if (dbHideTimer) { clearTimeout(dbHideTimer); dbHideTimer = null } }

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
            // include CSRF token for Django POST
            await ensureCsrf()
            const csrfToken = getCsrfToken()
            const res = await fetch(API_USER_MANAGEMENT_CHANGE_STATUS(userId), {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken || '',
                    'Accept': 'application/json'
                }
            })
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

// helper to read cookie by name (used for CSRF)
function getCookie(name) {
    if (!name || typeof document === 'undefined') return null
    const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')
    return v ? v.pop() : null
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
