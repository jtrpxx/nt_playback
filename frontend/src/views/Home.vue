<template>
  <MainLayout>
    <div class="main-wrapper container-fluid-home py-3">
      <Breadcrumbs :items="[{ text: 'Home', to: '/' }]" />
      
      <div class="row col-lg-12">
        <div class="col-lg-2">
          <div class="card">
            <div class="card-body">
              <div class="d-flex align-items-start justify-content-between" style="margin-bottom: 6px;">
                <div class="d-flex align-items-center">
                  <div class="d-flex align-items-center justify-content-center me-1"
                    style="width:35px;height:35px;background-color: #D9E2F6;border-radius: 10px !important;">
                    <i class="fa-solid fa-filter" style="color:#2b6cb0;font-size:18px"></i>
                  </div>
                  <h5 class="card-title mb-2 mt-1">Filters</h5>
                </div>
              </div>
              <!-- Content Filters-->
              <div class="filter-card">

                <div class="input-group" style="margin-top: 6px;">
                  <CustomSelect class="select-checkbox" v-model="filters.databaseServer"
                    :options="mainDbOptions"
                    placeholder="Database Server" name="databaseServer" />
                </div>

                <div class="input-group" v-has-value>
                  <input ref="fromInput" v-flatpickr="{ target: filters, key: 'from' }" required type="text" name="from"
                    autocomplete="off" class="input">
                  <label class="floating-label">From</label>
                  <span class="calendar-icon" @click="fromInput && fromInput.focus()"><i
                      class="fa-regular fa-calendar"></i></span>
                </div>

                <div class="input-group" v-has-value>
                  <input ref="toInput" v-flatpickr="{ target: filters, key: 'to' }" required type="text" name="to"
                    autocomplete="off" class="input">
                  <label class="floating-label">To</label>
                  <span class="calendar-icon" @click="toInput && toInput.focus()"><i
                      class="fa-regular fa-calendar"></i></span>
                </div>

                <div class="input-group" v-has-value>
                  <input ref="durationInput" v-model="filters.duration" v-flatpickr="{ target: filters, key: 'duration', mode: 'duration_range', options: { enableTime: true, noCalendar: true, enableSeconds: true, time_24hr: true, dateFormat: 'H:i:S', defaultHour: 0, defaultMinute: 0 } }" required type="text" name="duration" autocomplete="off" class="input">
                  <label class="floating-label">Duration</label>
                </div>

                <div class="input-group" v-has-value>
                  <input v-model="filters.fileName" required type="text" name="fileName" autocomplete="off" class="input">
                  <label class="floating-label">File Name</label>
                </div>

                <div class="input-group">
                  <CustomSelect class="select-checkbox"  v-model="filters.callDirection"
                    :options="callDirectionOptions"
                    placeholder="Call Direction" name="callDirection" />
                </div>

                <div class="input-group" v-has-value>
                  <input v-model="filters.customerNumber" required type="text" name="customerNumber" autocomplete="off" class="input">
                  <label class="floating-label">Customer Number</label>
                </div>

                <div class="input-group" v-has-value>
                  <input v-model="filters.extension" required type="text" name="extension" autocomplete="off" class="input">
                  <label class="floating-label">Extension</label>
                </div>

                <div class="input-group" >
                  <CustomSelect class="select-search select-checkbox" :class="{ up: 'up' }" v-model="filters.agent"
                    :options="agentOptions"
                    placeholder="Agent" name="agent" />
                </div>

                <div class="input-group" v-has-value>
                  <input v-model="filters.fullName" required type="text" name="fullName" autocomplete="off" class="input">
                  <label class="floating-label">Full Name</label>
                </div>

                <div class="input-group" v-has-value>
                  <input v-model="filters.customField" required type="text" name="customField" autocomplete="off" class="input">
                  <label class="floating-label">Custom Field</label>
                </div>

              </div>

              <div class="my-favorite-search">
                <div class="card">
                  <div class="card-body" style="padding: 8px;">

                    <div class="d-flex justify-content-center">
                      <button class="btn btn-light" type="button" id="addFavorite" @click="showFavoriteModal = true"
                        style="width: 100%;text-align: left;font-size: 12px;margin-bottom: 4px;">
                        <i class="fa-regular fa-bookmark"></i> My Favorite Search
                      </button>
                    </div>

                    <div class="dropup d-flex justify-content-center" ref="recentWrap">
                      <button class="btn btn-light" type="button" @click.stop="toggleRecent" :aria-expanded="recentOpen" style="width: 100%;font-size: 12px;margin-bottom: 4px;">
                        <div style="text-align: left;"><i class="fa-regular fa-clock"></i> <span>Recent</span></div>
                      </button>
                      <ul v-show="recentOpen" class="recent-dropdown">
                        <li><button class="dropdown-item" type="button" @click="applyLatestRecent">Latest</button></li>
                        <li><button class="dropdown-item" type="button" @click="applyRecentRange('1h')">1 hour</button></li>
                        <li><button class="dropdown-item" type="button" @click="applyRecentRange('1d')">1 day</button></li>
                        <li><button class="dropdown-item" type="button" @click="applyRecentRange('1w')">1 week</button></li>
                        <li><button class="dropdown-item" type="button" @click="applyRecentRange('1m')">1 month</button></li>
                        <li><button class="dropdown-item" type="button" @click="applyRecentRange('1y')">1 year</button></li>
                        <!-- dynamic recent entries hidden (only static range menu shown) -->
                      </ul>
                      <label for="recentDropdown"></label>
                    </div>

                    <div class="col-lg-12">
                      <div class="row g-0-3">
                        <div class="col-lg-6">
                          <button class="btn btn-primary w-97" type="button" id="search_audio" style="font-size: 12px;"
                            @click="onSearch"><span>Search</span></button>
                        </div>
                        <div class="col-lg-6">
                          <button class="btn btn-light w-97" type="button" id="reset_audio"
                            style="border-color: #f2e1e1;font-size: 12px;" @click="onReset"><span>Reset</span></button>
                        </div>
                      </div>
                    </div>

                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
        <div class="col-lg-10">
          <div class="card">
            <div class="card-body card-body-datatable">
              <div class="d-flex align-items-start justify-content-between" style="margin-bottom: 6px;">
                <div class="d-flex align-items-center">
                  <div class="d-flex align-items-center justify-content-center me-1"
                    style="width:35px;height:35px;background-color: #D9E2F6;border-radius: 10px !important;">
                    <i class="fa-solid fa-file-audio" style="color:#2b6cb0;font-size:18px"></i>
                  </div>
                  <h5 class="card-title mb-2 mt-1">Audio Records</h5>
                </div>
                <div class="d-flex align-items-center">
                  <div style="width:260px;">
                    <SearchInput ref="searchInputRef" v-model="searchQuery" :placeholder="'Search...'"
                      @typing="onTyping" @enter="onSearch" @clear="clearSearchQuery" />
                  </div>
                  <div class="ms-2 export-group" ref="exportWrap">
                    <button type="button" class="btn btn-primary btn-sm export-icon" @click.stop="toggleExport" :aria-expanded="exportOpen">
                      <i class="fa-solid fa-download" style="color: #fff;"></i>
                    </button>
                    <ul v-show="exportOpen" class="export-dropdown">
                      <li><button class="dropdown-item" type="button" @click="onExportFormat('pdf')">PDF</button></li>
                      <li><button class="dropdown-item" type="button" @click="onExportFormat('excel')">Excel</button></li>
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
                    show-selection
                    call-direction-key="call_direction"
                    :per-page="perPage"
                    :per-page-options="perPageOptions"
                    :current-page="currentPage"
                    :total-items="totalItems"
                        @edit="onRowEdit"
                        @delete="onRowDelete"
                        @row-dblclick="onRowDblClick"
                    @page-change="changePage"
                    @per-change="setPerPage"
                  />

              <!-- Content Audio Records-->
            </div>
          </div>
        </div>

      </div>
    </div>
  </MainLayout>
    <ModalHome v-model="showFavoriteModal" :favorites="favoriteSearchAll" :mainDbOptions="mainDbOptions" :agentOptions="agentOptions" @apply="applyFavorite" @edit="editFavorite" @delete="deleteFavorite" />
</template>

<script setup>
import MainLayout from '../layouts/MainLayout.vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'
import CustomSelect from '../components/CustomSelect.vue'
import ModalHome from '../components/ModalHome.vue'
import TableTemplate from '../components/TableTemplate.vue'
import SearchInput from '../components/SearchInput.vue'
import { reactive, ref, computed, watch, onMounted } from 'vue'
import { registerRequest } from '../utils/pageLoad'

import { onBeforeUnmount } from 'vue'
import { nextTick } from 'vue'
import { API_AUDIO_LIST, API_HOME_INDEX, API_LOG_PLAY_AUDIO, API_GET_CREDENTIALS, API_LOG_SAVE_FILE } from '../api/paths'
import { ensureCsrf, getCsrfToken } from '../api/csrf'

import '../assets/js/jspdf.umd.min.js'
import '../assets/js/jspdf.plugin.autotable.min.js'

import { exportTableToFormat,getCookie, showToast } from '../assets/js/function-all'


const filters = reactive({
  databaseServer: '',
  from: '',
  to: '',
  duration: '',
  fileName: '',
  callDirection: '',
  customerNumber: '',
  agent: ''
})

const searchQuery = ref('')
const searchInputRef = ref(null)
let searchTimeout = null

const onTyping = () => {
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

const perPageOptions = [50, 100, 500, 1000]
const perPage = ref(50)
const currentPage = ref(1)
const perDropdownOpen = ref(false)
const perDropdownUp = ref(false)
const mainDbOptions = ref([])
const favoriteSearchAll = ref([])
const agentOptions = ref([{ label: 'All', value: 'all' }])
const callDirectionOptions = [
  { label: 'All', value: 'All' },
  { label: 'Internal', value: 'Internal' },
  { label: 'Inbound', value: 'Inbound' },
  { label: 'Outbound', value: 'Outbound' }
]


const fetchIndexHome = async () => {
  const task = (async () => {
    try {
      const res = await fetch(API_HOME_INDEX(), { credentials: 'include' })
      if (!res.ok) return
      const json = await res.json()
      const mdb = json.main_db || []
      const mopts = []

      for (const m of mdb) {
        const mlabal = m.database_name
        const mvalue = m.id
        mopts.push({ label: mlabal, value: mvalue })
      }
      mainDbOptions.value = mopts

      const agents = json.agent || []
      const aopts = [{ label: 'All', value: 'all' }]
      for (const a of agents) {
        const name = `${a.first_name || ''} ${a.last_name || ''}`.trim()
        const alabel = a.agent_code ? `${a.agent_code} - ${name}` : name
        const avalue = a.id
        aopts.push({ label: alabel, value: avalue })
      }
      agentOptions.value = aopts
      
      favoriteSearchAll.value = json.favorite_search_all || []
    } catch (err) {
      console.error('fetchIndexHome error', err)
    }
  })()
  registerRequest(task)
  await task
}

const setPerPage = (opt) => {
  perPage.value = opt
  perDropdownOpen.value = false
}

const perWrap = ref(null)
const fromInput = ref(null)
const toInput = ref(null)
const durationInput = ref(null)
const exportWrap = ref(null)
const exportOpen = ref(false)
const recentWrap = ref(null)
const recentOpen = ref(false)
const recentList = ref([])
const showFavoriteModal = ref(false)
// save-log polling state
const processedSaveLogs = new Set()
let saveLogsInterval = null

const onDocClick = (e) => {
  if (perWrap.value && !perWrap.value.contains(e.target)) perDropdownOpen.value = false
  if (exportWrap.value && !exportWrap.value.contains(e.target)) exportOpen.value = false
  if (recentWrap.value && !recentWrap.value.contains(e.target)) recentOpen.value = false
}

const toggleRecent = () => {
  recentOpen.value = !recentOpen.value
}

const applyRecent = async (r) => {
  try {
    console.log('apply recent', r)
    // If recent item contains raw_data similar to favorites, apply filters
    const raw = typeof r.raw_data === 'string' ? JSON.parse(r.raw_data || '{}') : (r.raw_data || null)
    if (raw) {
      const keyMap = {
        database_name: 'databaseServer',
        start_date: 'from',
        end_date: 'to',
        file_name: 'fileName',
        duration: 'duration',
        customer: 'customerNumber',
        agent: 'agent',
        call_direction: 'callDirection',
        extension: 'extension',
        full_name: 'fullName',
        custom_field: 'customField'
      }
      for (const [rawKey, val] of Object.entries(raw)){
        const target = keyMap[rawKey]
        if (target && Object.prototype.hasOwnProperty.call(filters, target)){
          filters[target] = val
        }
      }

      // normalize call direction to match option values (case-insensitive)
      try {
        if (filters.callDirection) {
          const v = String(filters.callDirection)
          const found = callDirectionOptions.find(o => String(o.value).toLowerCase() === v.toLowerCase() || String(o.label).toLowerCase() === v.toLowerCase())
          if (found) filters.callDirection = found.value
        }
      } catch (e) {}

      // ensure flatpickr inputs reflect the loaded from/to
      try {
        const parseDate = (s) => {
          if (!s) return null
          // convert 'YYYY-MM-DD HH:mm' to 'YYYY-MM-DDTHH:mm' for reliable Date parsing
          const t = String(s).replace(' ', 'T')
          const d = new Date(t)
          return isNaN(d.getTime()) ? null : d
        }
        const fromDate = parseDate(filters.from)
        const toDate = parseDate(filters.to)

        if (fromInput.value) {
          const inst = fromInput.value._flatpickrInstance
          if (inst && typeof inst.setDate === 'function') {
            if (fromDate) inst.setDate(fromDate, true)
            else inst.clear()
          } else {
            fromInput.value.value = filters.from || ''
          }
        }
        if (toInput.value) {
          const inst2 = toInput.value._flatpickrInstance
          if (inst2 && typeof inst2.setDate === 'function') {
            if (toDate) inst2.setDate(toDate, true)
            else inst2.clear()
          } else {
            toInput.value.value = filters.to || ''
          }
        }
      } catch (e) { console.warn('applyRecent update inputs failed', e) }

      await fetchData()
    }
  } catch (err) {
    console.error('applyRecent error', err)
  } finally {
    recentOpen.value = false
  }
}

const applyRecentRange = async (rangeKey) => {
  try {
    const now = new Date()
    let fromDate = null
    let toDate = null
    if (rangeKey === 'latest') {
      fromDate = null
      toDate = null
    } else if (rangeKey === '1h') {
      fromDate = new Date(now.getTime() - 1 * 60 * 60 * 1000)
      toDate = now
    } else if (rangeKey === '1d') {
      fromDate = new Date(now.getTime() - 1 * 24 * 60 * 60 * 1000)
      toDate = now
    } else if (rangeKey === '1w') {
      fromDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
      toDate = now
    } else if (rangeKey === '1m') {
      fromDate = new Date(now)
      fromDate.setMonth(fromDate.getMonth() - 1)
      toDate = now
    } else if (rangeKey === '1y') {
      fromDate = new Date(now)
      fromDate.setFullYear(fromDate.getFullYear() - 1)
      toDate = now
    }

    const pad = (n) => String(n).padStart(2, '0')
    const fmt = (d) => {
      if (!d) return ''
      // format as 'YYYY-MM-DD HH:mm' (flatpickr default in directive)
      return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
    }

    filters.from = fromDate ? fmt(fromDate) : ''
    filters.to = toDate ? fmt(toDate) : ''

    // update flatpickr inputs/instances so UI reflects the change
    try {
      if (fromInput.value) {
        const inst = fromInput.value._flatpickrInstance
        if (inst && typeof inst.setDate === 'function') {
          if (fromDate) inst.setDate(fromDate, true)
          else inst.clear()
        } else {
          fromInput.value.value = filters.from
        }
      }
    } catch (e) { console.warn('update fromInput failed', e) }
    try {
      if (toInput.value) {
        const inst = toInput.value._flatpickrInstance
        if (inst && typeof inst.setDate === 'function') {
          if (toDate) inst.setDate(toDate, true)
          else inst.clear()
        } else {
          toInput.value.value = filters.to
        }
      }
    } catch (e) { console.warn('update toInput failed', e) }
    recentOpen.value = false
    await fetchData()

    // save this range as the latest recent selection so 'Latest' will apply it
    try {
      const raw = {
        database_name: filters.databaseServer,
        start_date: filters.from,
        end_date: filters.to,
        file_name: filters.fileName,
        duration: filters.duration,
        customer: filters.customerNumber,
        agent_id: filters.agent,
        agent: filters.agent,
        call_direction: filters.callDirection,
        extension: filters.extension,
        full_name: filters.fullName,
        custom_field: filters.customField,
        search: searchQuery.value
      }
      pushRecent({ raw_data: raw, created_at: new Date().toISOString() })
    } catch (e) {
      console.warn('save recent range failed', e)
    }
  } catch (err) {
    console.error('applyRecentRange error', err)
    recentOpen.value = false
  }
}

const applyLatestRecent = async () => {
  try {
    if (!recentList.value || recentList.value.length === 0) return
    const latest = recentList.value[0]
    await applyRecent(latest)
  } catch (err) {
    console.error('applyLatestRecent error', err)
  }
}

const toggleExport = () => {
  exportOpen.value = !exportOpen.value
}

onMounted(() => {
  // fetchIndexHome registers itself with pageLoad; ensure the initial data fetch is registered too
  fetchIndexHome()
  registerRequest(fetchData())
  loadRecentFromStorage()
  document.addEventListener('click', onDocClick)
  // start polling local wrapper for save-file logs every 3 seconds
  try {
    // start immediately and then every 3s
    pollSaveLogs()
    saveLogsInterval = setInterval(pollSaveLogs, 3000)
  } catch (e) { console.warn('start pollSaveLogs failed', e) }
})

onBeforeUnmount(() => {
  document.removeEventListener('click', onDocClick)
  try { if (saveLogsInterval) clearInterval(saveLogsInterval) } catch (e) {}
})

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

    if (Array.isArray(filters.databaseServer)) {
      const vals = filters.databaseServer.filter(v => String(v).toLowerCase() !== 'all')
      if (vals.length) params.set('database_name', vals.join(','))
    } else if (filters.databaseServer && String(filters.databaseServer) !== 'all') {
      params.set('database_name', filters.databaseServer)
    }

    if (Array.isArray(filters.callDirection)) {
      const vals = filters.callDirection.filter(v => String(v).toLowerCase() !== 'all')
      if (vals.length) params.set('call_direction', vals.join(','))
    } else if (filters.callDirection && String(filters.callDirection).toLowerCase() !== 'all') {
      params.set('call_direction', filters.callDirection)
    }

    if (Array.isArray(filters.agent)) {
      const vals = filters.agent.filter(v => String(v).toLowerCase() !== 'all')
      if (vals.length) params.set('agent_id', vals.join(','))
    } else if (filters.agent && String(filters.agent) !== 'all') {
      params.set('agent_id', filters.agent)
    }
    if (filters.from) params.set('start_date', filters.from)
    if (filters.to) params.set('end_date', filters.to)

    function norm(v){
      if (Array.isArray(v)) return v.join(',')
      if (v == null) return ''
      const s = String(v).trim()
      if (s.indexOf(',') === -1) return s
      return s.split(',').map(x => x.trim()).filter(Boolean).join(',')
    }

    const fn = norm(filters.fileName)
    if (fn) params.set('file_name', fn)
    const dur = norm(filters.duration)
    if (dur) params.set('duration', dur)
    const cust = norm(filters.customerNumber)
    if (cust) params.set('customer_number', cust)
    const ext = norm(filters.extension)
    if (ext) params.set('extension', ext)
    const full = norm(filters.fullName)
    if (full) params.set('full_name', full)
    const cf = norm(filters.customField)
    if (cf) params.set('custom_field', cf)

    const res = await fetch(`${API_AUDIO_LIST()}?${params.toString()}`, { credentials: 'include' })
    if (!res.ok) throw new Error('Failed to fetch')
    const json = await res.json()
    records.value = json.data || []
    totalItems.value = json.recordsFiltered ?? json.recordsTotal ?? records.value.length
  } catch (e) {
    console.error('fetchData error', e)
  } finally {
    loading.value = false
  }
}

const totalPages = computed(() => Math.max(1, Math.ceil(totalItems.value / perPage.value)))
const startIndex = computed(() => (currentPage.value - 1) * perPage.value)
const paginatedRecords = computed(() => records.value)
const startItem = computed(() => totalItems.value === 0 ? 0 : startIndex.value + 1)
const endItem = computed(() => Math.min(totalItems.value, startIndex.value + (records.value.length || 0)))

const pagesToShow = computed(() => {
  const pages = []
  const total = totalPages.value
  if (total <= 6) {
    for (let i = 1; i <= total; i++) pages.push(i)
    return pages
  }

  // Show first 1..5, ellipsis, last
  const end = Math.min(5, total)
  for (let i = 1; i <= end; i++) pages.push(i)
  if (total > end + 1) pages.push('...')
  pages.push(total)
  return pages
})

const changePage = async (p) => { 
  if (p < 1) p = 1
  if (p > totalPages.value) p = totalPages.value
  currentPage.value = p
  await fetchData()
}

watch(perPage, () => {
  currentPage.value = 1
  fetchData()
})

const RECENT_KEY = 'home_recent_searches'

const loadRecentFromStorage = () => {
  try {
    const raw = localStorage.getItem(RECENT_KEY)
    if (!raw) return
    const arr = JSON.parse(raw)
    if (Array.isArray(arr)) recentList.value = arr
  } catch (e) {
    console.error('loadRecentFromStorage error', e)
  }
}

const saveRecentToStorage = () => {
  try {
    localStorage.setItem(RECENT_KEY, JSON.stringify(recentList.value.slice(0, 10)))
  } catch (e) {
    console.error('saveRecentToStorage error', e)
  }
}

const pushRecent = (item) => {
  try {
    // dedupe by raw_data JSON
    const key = JSON.stringify(item.raw_data || {})
    recentList.value = recentList.value.filter(r => JSON.stringify(r.raw_data || {}) !== key)
    recentList.value.unshift(item)
    // keep max 10
    if (recentList.value.length > 10) recentList.value.pop()
    saveRecentToStorage()
  } catch (e) {
    console.error('pushRecent error', e)
  }
}

const onSearch = async () => {
  currentPage.value = 1
  if (searchTimeout) { clearTimeout(searchTimeout); searchTimeout = null }
  await fetchData()
  try {
    // save current filters + searchQuery as a recent item using backend-style keys
    const raw = {
      database_name: filters.databaseServer,
      start_date: filters.from,
      end_date: filters.to,
      file_name: filters.fileName,
      duration: filters.duration,
      customer: filters.customerNumber,
      agent_id: filters.agent,
      agent: filters.agent,
      call_direction: filters.callDirection,
      extension: filters.extension,
      full_name: filters.fullName,
      custom_field: filters.customField,
      search: searchQuery.value
    }
    const item = { raw_data: raw, created_at: new Date().toISOString() }
    pushRecent(item)
  } catch (e) {
    console.error('onSearch save recent error', e)
  }
}

const onReset = async () => {
  try {
    // clear all filter fields
    // reset multi-selects to empty arrays so CustomSelect checkbox mode clears
    filters.databaseServer = []
    filters.from = ''
    filters.to = ''
    filters.duration = ''
    filters.fileName = ''
    filters.callDirection = []
    filters.customerNumber = ''
    filters.agent = []
    filters.fullName = ''
    filters.customField = ''
    filters.extension = ''
    // clear search and pagination
    searchQuery.value = ''
    currentPage.value = 1
    // ensure flatpickr inputs are cleared in the DOM too
    await nextTick()
    try {
      if (fromInput.value) {
        if (fromInput.value._flatpickr && typeof fromInput.value._flatpickr.clear === 'function') {
          fromInput.value._flatpickr.clear()
        } else {
          fromInput.value.value = ''
        }
      }
    } catch (e) { console.warn('clear fromInput failed', e) }
    try {
      if (toInput.value) {
        if (toInput.value._flatpickr && typeof toInput.value._flatpickr.clear === 'function') {
          toInput.value._flatpickr.clear()
        } else {
          toInput.value.value = ''
        }
      }
    } catch (e) { console.warn('clear toInput failed', e) }

    // Remove has-value classes and clear any remaining input values inside filter-card
    try {
      const wrap = document.querySelector('.filter-card')
      if (wrap) {
        const groups = wrap.querySelectorAll('.input-group')
        groups.forEach(g => {
          try {
            g.classList.remove('has-value')
            const input = g.querySelector('input, textarea, select')
            if (input) input.value = ''
          } catch (ign) {}
        })
      }
    } catch (e) { console.warn('clear filter-card values failed', e) }
    // fetch default data
    await fetchData()
  } catch (e) {
    console.error('onReset error', e)
  }
}

async function applyFavorite(fav){
  try{
    const raw = typeof fav.raw_data === 'string' ? JSON.parse(fav.raw_data || '{}') : (fav.raw_data || {})
      // map raw_data keys to local `filters` keys and normalize multi-selects
      const keyMap = {
        database_name: 'databaseServer',
        start_date: 'from',
        end_date: 'to',
        file_name: 'fileName',
        duration: 'duration',
        customer: 'customerNumber',
        agent: 'agent',
        call_direction: 'callDirection',
        extension: 'extension',
        full_name: 'fullName',
        custom_field: 'customField'
      }
      for (const [rawKey, val] of Object.entries(raw)){
        const target = keyMap[rawKey]
        if (target && Object.prototype.hasOwnProperty.call(filters, target)){
          filters[target] = val
        }
      }

      // Normalize multi-select fields so CustomSelect (checkbox mode) receives arrays
      try {
        const multiFields = ['databaseServer', 'agent', 'callDirection']
        for (const mf of multiFields) {
          if (!Object.prototype.hasOwnProperty.call(filters, mf)) continue
          const cur = filters[mf]
          let vals = []
          if (cur == null || cur === '') vals = []
          else if (Array.isArray(cur)) vals = cur.slice()
          else if (typeof cur === 'string') {
            if (cur.indexOf(',') !== -1) vals = cur.split(',').map(x => x.trim()).filter(Boolean)
            else vals = [cur]
          } else {
            vals = [cur]
          }

          if (mf === 'databaseServer' || mf === 'agent') {
            vals = vals.map(x => { const s = String(x).trim(); return /^\d+$/.test(s) ? Number(s) : s })
          }
          if (mf === 'callDirection') {
            vals = vals.map(x => { const s = String(x || '').trim(); return s ? (s.charAt(0).toUpperCase() + s.slice(1).toLowerCase()) : s })
          }
          filters[mf] = vals
        }

        // Also normalize callDirection values to match option values if possible
        if (Array.isArray(filters.callDirection)) {
          filters.callDirection = filters.callDirection.map(v => {
            const s = String(v || '')
            const found = callDirectionOptions.find(o => String(o.value).toLowerCase() === s.toLowerCase() || String(o.label).toLowerCase() === s.toLowerCase())
            return found ? found.value : v
          }).filter(Boolean)
        }
      } catch (e) {}

    // ensure DOM inputs and flatpickr reflect the loaded values so labels float correctly
    showFavoriteModal.value = false
    await nextTick()

    const parseDate = (s) => {
      if (!s) return null
      const t = String(s).replace(' ', 'T')
      const d = new Date(t)
      return isNaN(d.getTime()) ? null : d
    }

    try {
      if (fromInput.value) {
        const inst = fromInput.value._flatpickrInstance || fromInput.value._flatpickr
        const d = parseDate(filters.from)
        if (inst && typeof inst.setDate === 'function') {
          if (d) inst.setDate(d, true)
          else inst.clear()
        } else {
          fromInput.value.value = filters.from || ''
        }
      }
    } catch (e) { console.warn('applyFavorite update fromInput failed', e) }
    try {
      if (toInput.value) {
        const inst2 = toInput.value._flatpickrInstance || toInput.value._flatpickr
        const d2 = parseDate(filters.to)
        if (inst2 && typeof inst2.setDate === 'function') {
          if (d2) inst2.setDate(d2, true)
          else inst2.clear()
        } else {
          toInput.value.value = filters.to || ''
        }
      }
    } catch (e) { console.warn('applyFavorite update toInput failed', e) }

    try {
      if (durationInput.value) {
        const inst3 = durationInput.value._flatpickrInstance || durationInput.value._flatpickr
        const dstr = filters.duration
        if (inst3 && typeof inst3.setDate === 'function') {
          if (dstr && dstr.indexOf(':') !== -1) {
            const parts = String(dstr).split(':').map(x => parseInt(x, 10) || 0)
            const now = new Date()
            now.setHours(parts[0] || 0, parts[1] || 0, parts[2] || 0, 0)
            inst3.setDate(now, true)
          } else if (!dstr) {
            inst3.clear()
          } else {
            durationInput.value.value = dstr || ''
          }
        } else {
          durationInput.value.value = filters.duration || ''
        }
      }
    } catch (e) { console.warn('applyFavorite update durationInput failed', e) }

    // sync has-value classes for inputs inside the filter-card
    try {
      const wrap = document.querySelector('.filter-card')
      if (wrap) {
        const groups = wrap.querySelectorAll('.input-group')
        groups.forEach(g => {
          try {
            const input = g.querySelector('input, textarea, select')
            if (!input) return
            const val = input.value
            const has = val !== null && String(val).trim() !== ''
            g.classList.toggle('has-value', has)
          } catch (ign) {}
        })
      }
    } catch (e) { console.warn('applyFavorite sync has-value failed', e) }

    fetchData()
  }catch(e){
    console.error('applyFavorite parse error', e)
  }
}

function editFavorite(fav){
  try {
    if (!fav || !fav.id) return
    const idx = favoriteSearchAll.value.findIndex(x => String(x.id) === String(fav.id))
    if (idx === -1) {
      // new favorite created -> add to front
      favoriteSearchAll.value.unshift(fav)
    } else {
      // update existing in-place
      favoriteSearchAll.value[idx] = fav
    }
  } catch (e) {
    console.error('editFavorite update error', e)
  }
}

function deleteFavorite(id){
  try {
    if (!id) return
    favoriteSearchAll.value = favoriteSearchAll.value.filter(x => String(x.id) !== String(id))
  } catch (e) {
    console.error('deleteFavorite update error', e)
  }
}

function truncate(s, max) {
  if (!s) return ''
  const str = String(s)
  if (str.length <= max) return str
  return str.slice(0, max - 3) + '...'
}

onMounted(() => {
})

const onExport = () => console.log('Export triggered')

const onExportFormat = (format) => {
  exportTableToFormat(format, 'audio', {
    rows: paginatedRecords.value || [],
    columns: columns || [],
    startIndex: startIndex.value || 0,
    fileNamePrefix: 'audio-records'
  })
}

const callDirectionClass = (dir) => {
  if (!dir) return 'bg-secondary'
  const key = String(dir).toLowerCase()
  if (key === 'internal') return 'badge-warning'
  if (key === 'inbound') return 'badge-success'
  if (key === 'outbound') return 'badge-primary'
  return 'bg-secondary'
}

const columns = [
  { key: 'index', label: '#', isIndex: true },
  { key: 'main_db', label: 'Database Server' },
  { key: 'start_datetime', label: 'Start Date & Time' },
  { key: 'end_datetime', label: 'End Date & Time' },
  { key: 'duration', label: 'Duration' },
  { key: 'file_name', label: 'File Name', tooltip: true },
  { key: 'call_direction', label: 'Call Direction' },
  { key: 'customer_number', label: 'Customer Number' },
  { key: 'extension', label: 'Extension' },
  { key: 'agent', label: 'Agent' },
  { key: 'full_name', label: 'Full Name' },
  { key: 'custom_field_1', label: 'Custom Field' }
]


const onRowDblClick = async (row) => {
  if (!row) return
  const fileName = row.file_name || row.fileName || ''
  if (!fileName) return

  const uncPath = `\\\\nichetel-niceplayer\\Users\\Administrator\\Desktop\\Music\\${fileName}`
  const url_check_local_server = 'http://127.0.0.1:54321/check'
  const url_get_credentials = API_GET_CREDENTIALS()
  const url_log_playback = API_LOG_PLAY_AUDIO()

  const sendLog = async (status, detail) => {
    try { await ensureCsrf() } catch (e) {}
    const csrfToken = getCsrfToken()
    fetch(url_log_playback, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken || '' },
      body: JSON.stringify({ status, detail })
    }).catch(err => console.error('Failed to send log:', err))
  }

  loading.value = true

  try {
    const checkResponse = await fetch(url_check_local_server)
    if (!checkResponse.ok) throw new Error('Local server responded with an error.')
    const checkData = await checkResponse.json()

    if (!checkData.installed) {
      try {
        Swal.fire({ icon: 'warning', title: 'แจ้งเตือน', html: `ไม่สามารถเล่นไฟล์เสียงได้ กรุณาติดตั้งโปรแกรม <a href="set-audio-launcher://" style="color:#3085d6; text-decoration: underline;">Nice Player</a>`, confirmButtonText: 'OK' })
      } catch (e) {}
      sendLog('error', `FAIL_NOT_INSTALLED | NICE Player executable not found. File: ${uncPath}`)
      showAudioLoading(false)
      return
    }

    const credsResponse = await fetch(url_get_credentials, { credentials: 'include' })
    if (!credsResponse.ok) throw new Error(`Failed to get credentials from server. Status: ${credsResponse.status}`)
    const credentials = await credsResponse.json()
    if (credentials.error) throw new Error(`Server returned an error: ${credentials.error}`)

    const encodedPath = encodeURIComponent(uncPath)
    const encodedUser = encodeURIComponent(credentials.username || '')
    const encodedPass = encodeURIComponent(credentials.password || '')
    const protocolLink = `niceplayer://?path=${encodedPath}&user=${encodedUser}&pass=${encodedPass}`

    try {
      window.location.href = protocolLink

      let checkCount = 0
      const maxChecks = 60
      const pollInterval = setInterval(async () => {
        checkCount++
        try {
          const res = await fetch(url_check_local_server)
          const data = await res.json()
          if (data.running || checkCount >= maxChecks) {
            clearInterval(pollInterval)
            loading.value = false
            if (data.running) sendLog('success', `Playback file: ${uncPath}`)
            else {
              sendLog('warning', `Playback initiated but process not detected: ${uncPath}`)
              try { Swal.fire('แจ้งเตือน', 'ไม่สามารถเปิด NICE Player ได้ อาจเกิดข้อผิดพลาดบางอย่าง', 'warning') } catch (e) {}
            }
          }
        } catch (err) {
          if (checkCount >= maxChecks) {
            clearInterval(pollInterval)
            loading.value = false
          }
        }
      }, 500)
    } catch (e) {
      console.error('Error launching protocol:', e)
      try { Swal.fire('แจ้งเตือน', 'ไม่สามารถเปิด NICE Player ได้ อาจเกิดข้อผิดพลาดบางอย่าง', 'warning') } catch (er) {}
      sendLog('error', `FAIL_PLAYER_ERROR | Error launching protocol for file: ${uncPath}. Error: ${e.message}`)
            loading.value = false
    }

  } catch (error) {
    console.error('Playback process failed:', error)
    try {
      Swal.fire({ icon: 'warning', title: 'แจ้งเตือน', html: `ไม่สามารถเล่นไฟล์เสียงได้ กรุณาติดตั้งโปรแกรม<br><a href="/set-audio-launcher" style="color:#3085d6; text-decoration: underline;"> NT Player Connect</a> หรือ ตรวจสอบว่าโปรแกรมกำลังทำงานอยู่<br> โดยไปที่ Task Manager > Details ><br> ค้นหา NT Player Connect.exe`, confirmButtonText: 'OK' })
    } catch (e) {}
    sendLog('error', `FAIL_NT_Player_Connect_RUNNING | Could not connect to local NT Player Connect or another error occurred: ${error.message}. File: ${uncPath}`)
    loading.value = false
  }
}

async function pollSaveLogs() {
  const localUrl = 'http://127.0.0.1:54321/get_save_logs'
  const url_log_save_file = API_LOG_SAVE_FILE()
  try { await ensureCsrf() } catch (e) {}
  try {
    const res = await fetch(localUrl)
    if (!res.ok) return
    const data = await res.json()
    if (!data || !Array.isArray(data.logs) || data.logs.length === 0) return

    for (const log of data.logs) {
      try {
        const key = `${log.timestamp || ''}|${log.file_path || log.path || ''}`
        if (processedSaveLogs.has(key)) continue
        processedSaveLogs.add(key)
        const detail = `Time: ${log.timestamp} | Path name: ${log.file_path || log.path || ''}`
        const csrfToken = getCsrfToken()
        fetch(url_log_save_file, {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken || '' },
          body: JSON.stringify({ detail })
        }).catch(err => console.warn('Failed to forward save-log', err))
      } catch (e) { console.warn('process log failed', e) }
    }
  } catch (e) {

  }
}

const onRowEdit = (row) => { console.log('edit row', row) }
const onRowDelete = (row) => { console.log('delete row', row) }

</script>

<style scoped>
/* make floating-label behave for inputs in Home like CustomSelect */
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

/* Export button and dropdown */
.export-group { position: relative; }
.export-dropdown { position: absolute; right: 0; margin-top: 34px; min-width: 150px; z-index: 1050; background: #fff; border: 1px solid rgba(0,0,0,.15); border-radius: 6px; box-shadow: 0 .5rem 1rem rgba(0,0,0,.175); list-style: none; padding: 6px 0; }
.export-dropdown .dropdown-item { width:100%; text-align:left; padding:8px 16px; background:transparent; border:none;font-size: 10px; }

/* Recent dropdown */
.dropup { position: relative; display: block; }
.recent-dropdown { position: absolute; left: 0; right: 0; bottom: calc(100% + -12px); min-width: 0; width: auto; max-width: 100%; box-sizing: border-box; z-index: 2060; background: #fff; border: 1px solid rgba(0,0,0,.15); border-radius: 25px;  list-style: none; padding: 6px 0; transform-origin: bottom right; }
.recent-dropdown .dropdown-item { width:100%; text-align:left; padding:8px 12px; background:transparent; border:none; font-size:12px }

/* Prevent my-favorite-search card from clipping the dropup */
.my-favorite-search .card,
.my-favorite-search .card-body { overflow: visible; }

/* Clear icon for top search input */
.search-group .search-input { padding-right: 28px; }
.search-group .clear-icon {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  color: #9aa4ad;
  font-size: 12px;
  cursor: pointer;
}

input[type="checkbox" i] {
 cursor: pointer
}
</style>
