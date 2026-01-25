<template>

  <MainLayout>
    <div class="main-wrapper container-fluid py-3">
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
                  <CustomSelect class="select-search select-checkbox" v-model="filters.databaseServer"
                    :options="mainDbOptions"
                    placeholder="Database Server" name="databaseServer" />
                </div>

                <div class="input-group" v-has-value>
                  <input ref="fromInput" v-flatpickr="{ target: filters, key: 'from' }" required type="text" name="from"
                    autocomplete="off" class="input">
                  <label class="title-label">From</label>
                  <span class="calendar-icon" @click="fromInput && fromInput.focus()"><i
                      class="fa-regular fa-calendar"></i></span>
                </div>

                <div class="input-group" v-has-value>
                  <input ref="toInput" v-flatpickr="{ target: filters, key: 'to' }" required type="text" name="to"
                    autocomplete="off" class="input">
                  <label class="title-label">To</label>
                  <span class="calendar-icon" @click="toInput && toInput.focus()"><i
                      class="fa-regular fa-calendar"></i></span>
                </div>

                <div class="input-group" v-has-value>
                  <input v-model="filters.duration" required="" type="text" name="duration" autocomplete="off" class="input">
                  <label class="title-label">Duration</label>
                </div>

                <div class="input-group" v-has-value>
                  <input v-model="filters.fileName" required="" type="text" name="fileName" autocomplete="off" class="input">
                  <label class="title-label">File Name</label>
                </div>

                <div class="input-group">
                  <CustomSelect class="select-checkbox" v-model="filters.callDirection"
                    :options="[{ label: 'All', value: 'All' }, { label: 'Internal', value: 'Internal' }, { label: 'Inbound', value: 'Inbound' }, { label: 'Outbound', value: 'Outbound' }]"
                    placeholder="Call Direction" name="callDirection" />
                </div>

                <div class="input-group" v-has-value>
                  <input v-model="filters.customerNumber" required="" type="text" name="customerNumber" autocomplete="off" class="input">
                  <label class="title-label">Customer Number</label>
                </div>

                <div class="input-group" v-has-value>
                  <input v-model="filters.extension" required="" type="text" name="extension" autocomplete="off" class="input">
                  <label class="title-label">Extension</label>
                </div>

                <div class="input-group" >
                  <CustomSelect class="select-search select-checkbox" v-model="filters.agent"
                    :options="agentOptions"
                    placeholder="Agent" name="agent" />
                </div>

                <div class="input-group" v-has-value>
                  <input v-model="filters.fullName" required="" type="text" name="fullName" autocomplete="off" class="input">
                  <label class="title-label">Full Name</label>
                </div>

                <div class="input-group" v-has-value>
                  <input v-model="filters.customField" required="" type="text" name="customField" autocomplete="off" class="input">
                  <label class="title-label">Custom Field</label>
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

                    <div class="dropup d-flex justify-content-center">
                      <button class="btn btn-light" type="button" id="recentDropdown" data-bs-toggle="dropdown"
                        aria-expanded="false" style="width: 100%;font-size: 12px;margin-bottom: 4px;">
                        <div style="text-align: left;"><i class="fa-regular fa-clock"></i> <span>Recent</span></div>
                      </button>
                      <ul class="dropdown-menu" id="recentMenu" style="width: 241px;">
                        <li class="dropdown-item disabled">No recent searches<span>No recent searches</span></li>
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
                            style="border-color: #f2e1e1;font-size: 12px;"><span>Reset</span></button>
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

              <div class="table-container">
                <div class="table-responsive table-scroll">
                  <table class="table table-sm table-striped">
                    <thead class="table-primary">
                      <tr>
                        <th>#</th>
                        <th>Database Server</th>
                        <th>START DATE & TIME</th>
                        <th>END DATE & TIME</th>
                        <th>Duration</th>
                        <th>File Name</th>
                        <th>Call Direction</th>
                        <th>Customer Number</th>
                        <th>Extension</th>
                        <th>Agent</th>
                        <th>Full Name</th>
                        <th>Custom Field</th>

                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(r, idx) in paginatedRecords" :key="r.no">
                        <td>{{ startIndex + idx + 1 }}</td>
                        <td>{{ r.main_db }}</td>
                        <td>{{ r.start_datetime }}</td>
                        <td>{{ r.end_datetime }}</td>
                        <td>{{ r.duration }}</td>
                        <td>
                          <div class="file-name-cell" :class="{ 'is-active': activeTooltip === idx }" @mouseenter="activeTooltip = idx"
                            @mouseleave="activeTooltip = null">
                            <span class="truncated">{{ truncate(r.file_name, 20) }}</span>
                            <div v-if="activeTooltip === idx" :class="['tooltip','bs-tooltip-top','show', { 'tooltip-down': activeTooltip === idx && idx === 0 }]" role="tooltip"
                              @mousedown.stop @mouseup.stop @click.stop>
                              <div class="tooltip-inner d-flex align-items-center">
                                <span class="file-full me-2">{{ r.file_name }}</span>
                                <button class="btn btn-sm btn-outline-secondary btn-copy" @click="copyFileName(r.file_name, idx)" :aria-label="copiedIndex===idx ? 'Copied' : 'Copy'">
                                  <i :class="copiedIndex === idx ? 'fa-solid fa-check' : 'fa-regular fa-copy'"></i>
                                </button>
                              </div>
                            </div>
                          </div>
                        </td>
                        <td><span :class="['badge', callDirectionClass(r.call_direction)]">{{ r.call_direction }}</span>
                        </td>
                        <td>{{ r.customer_number }}</td>
                        <td>{{ r.extension }}</td>
                        <td>{{ r.agent }}</td>
                        <td>{{ r.full_name }}</td>
                        <td>{{ r.custom_field_1 }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div v-if="loading" class="table-overlay">
                  <div class="overlay-box">Processing...</div>
                </div>
              </div>

              <div class="d-flex justify-content-between align-items-center mt-2 pagination-div">
                <div>
                  <div class="show-entries">
                    Show
                    <div class="custom-select-wrap" ref="perWrap" :class="{ up: perDropdownUp, open: perDropdownOpen }">
                      <button type="button" class="custom-select-toggle" @click="togglePerDropdown">
                        <span class="selected">{{ perPage }}</span>
                        <i class="fa-solid fa-caret-down "></i>
                      </button>
                      <ul v-if="perDropdownOpen" class="custom-select-menu">
                        <li v-for="opt in perPageOptions" :key="opt" :class="{ active: opt === perPage }"
                          @click="setPerPage(opt)">{{ opt }}</li>
                      </ul>
                    </div>
                    entries per page, Showing {{ startItem }} to {{ endItem }} of {{ totalItems }} entries
                  </div>
                </div>
                <nav>
                  <ul class="pagination pagination-sm mb-0">
                    <li class="page-item" :class="{ disabled: currentPage === 1 }"><button class="page-link"
                        @click="changePage(currentPage - 1)">Previous</button></li>
                    <li class="page-item" v-for="p in pagesToShow" :key="String(p)"
                      :class="[{ active: p === currentPage }, { disabled: p === '...' }]">
                      <button v-if="p !== '...'" class="page-link" @click="changePage(p)">{{ p }}</button>
                      <span v-else class="page-link">…</span>
                    </li>
                    <li class="page-item" :class="{ disabled: currentPage === totalPages }"><button class="page-link"
                        @click="changePage(currentPage + 1)">Next</button></li>
                  </ul>
                </nav>
              </div>

              <!-- Content Audio Records-->
            </div>
          </div>
        </div>

      </div>
    </div>
  </MainLayout>
  <ModalHome v-model="showFavoriteModal" :favorites="favoriteSearchAll" :main-db="mainDbOptions" @apply="applyFavorite" @edit="editFavorite" @delete="deleteFavorite" />
</template>

<script setup>
import MainLayout from '../layouts/MainLayout.vue'
import CustomSelect from '../components/CustomSelect.vue'
import ModalHome from '../components/ModalHome.vue'
import { reactive, ref, computed, watch, onMounted } from 'vue'
import { onBeforeUnmount } from 'vue'
import { nextTick } from 'vue'


const API_AUDIO_LIST = 'http://localhost:8000/api/audio/list/'
const API_HOME_INDEX = 'http://localhost:8000/api/home/index/'

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
let searchTimeout = null

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
const perDropdownOpen = ref(false)
const perDropdownUp = ref(false)
const mainDbOptions = ref([])
const favoriteSearchAll = ref([])
const agentOptions = ref([{ label: 'All', value: 'all' }])

const fetchIndex = async () => {
  try {
    const res = await fetch(API_HOME_INDEX, { credentials: 'include' })
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
    console.error('fetchIndex error', err)
  }
}

const togglePerDropdown = () => {
  perDropdownOpen.value = !perDropdownOpen.value
  if (perDropdownOpen.value) {
    // decide whether to open upwards based on available space
    const wrap = perWrap.value
    if (wrap) {
      const rect = wrap.getBoundingClientRect()
      const spaceBelow = window.innerHeight - rect.bottom
      // estimate menu height (items * approx item height + padding)
      const estimatedMenuHeight = Math.min(300, perPageOptions.length * 40 + 12)
      perDropdownUp.value = spaceBelow < estimatedMenuHeight
    } else {
      perDropdownUp.value = false
    }
  }
}

const setPerPage = (opt) => {
  perPage.value = opt
  perDropdownOpen.value = false
}

const perWrap = ref(null)
const showFavoriteModal = ref(false)

const onDocClick = (e) => {
  if (!perWrap.value) return
  if (!perWrap.value.contains(e.target)) perDropdownOpen.value = false
}

onMounted(() => {
  fetchIndex()
  fetchData()
  document.addEventListener('click', onDocClick)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', onDocClick)
})

const records = ref([])
const totalItems = ref(0)
const loading = ref(false)
const activeTooltip = ref(null)
const copiedIndex = ref(null)

const fetchData = async () => {
  loading.value = true
  try {
    const start = (currentPage.value - 1) * perPage.value
    const params = new URLSearchParams()
    params.set('draw', 1)
    params.set('start', start)
    params.set('length', perPage.value)
    params.set('search[value]', searchQuery.value || '')
    // include filters
    // databaseServer may be a single value or an array (multi-select)
    if (Array.isArray(filters.databaseServer)) {
      const vals = filters.databaseServer.filter(v => String(v).toLowerCase() !== 'all')
      if (vals.length) params.set('database_name', vals.join(','))
    } else if (filters.databaseServer && String(filters.databaseServer) !== 'all') {
      params.set('database_name', filters.databaseServer)
    }

    // callDirection may be multi-select (checkbox-only)
    if (Array.isArray(filters.callDirection)) {
      const vals = filters.callDirection.filter(v => String(v).toLowerCase() !== 'all')
      if (vals.length) params.set('call_direction', vals.join(','))
    } else if (filters.callDirection && String(filters.callDirection).toLowerCase() !== 'all') {
      params.set('call_direction', filters.callDirection)
    }

    // agent may be multi-select
    if (Array.isArray(filters.agent)) {
      const vals = filters.agent.filter(v => String(v).toLowerCase() !== 'all')
      if (vals.length) params.set('agent_id', vals.join(','))
    } else if (filters.agent && String(filters.agent) !== 'all') {
      params.set('agent_id', filters.agent)
    }
    if (filters.from) params.set('start_date', filters.from)
    if (filters.to) params.set('end_date', filters.to)

    // helper to normalize multi-value inputs (comma separated or arrays)
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

    // include credentials so session cookie (from backend at localhost:8000) is sent
    const res = await fetch(`${API_AUDIO_LIST}?${params.toString()}`, { credentials: 'include' })
    if (!res.ok) throw new Error('Failed to fetch')
    const json = await res.json()
    records.value = json.data || []
    // prefer recordsFiltered, fallback to recordsTotal
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

const onSearch = () => {
  currentPage.value = 1
  if (searchTimeout) { clearTimeout(searchTimeout); searchTimeout = null }
  fetchData()
}

function applyFavorite(fav){
  try{
    const raw = typeof fav.raw_data === 'string' ? JSON.parse(fav.raw_data || '{}') : (fav.raw_data || {})
    // map raw_data keys to local `filters` keys
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
    // close modal and refresh
    showFavoriteModal.value = false
    fetchData()
  }catch(e){
    console.error('applyFavorite parse error', e)
  }
}

function editFavorite(fav){
  console.log('edit favorite', fav)
}

function deleteFavorite(id){
  console.log('delete favorite', id)
}

function truncate(s, max) {
  if (!s) return ''
  const str = String(s)
  if (str.length <= max) return str
  return str.slice(0, max - 3) + '...'
}

async function copyFileName(text, idx) {
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(text)
    } else {
      const ta = document.createElement('textarea')
      ta.value = text
      ta.style.position = 'fixed'
      ta.style.left = '-9999px'
      document.body.appendChild(ta)
      ta.select()
      document.execCommand('copy')
      document.body.removeChild(ta)
    }
    copiedIndex.value = idx
    setTimeout(() => { if (copiedIndex.value === idx) copiedIndex.value = null }, 1400)
  } catch (e) {
    console.error('copy failed', e)
  }
}

onMounted(() => {
  // moved fetchData to combined onMounted above to ensure dropdown listener setup
})

const onExport = () => console.log('Export triggered')
const onExportFormat = (format) => console.log('Export format:', format)

const callDirectionClass = (dir) => {
  if (!dir) return 'bg-secondary'
  const key = String(dir).toLowerCase()
  if (key === 'internal') return 'badge-warning'
  if (key === 'inbound') return 'badge-success'
  if (key === 'outbound') return 'badge-primary'
  return 'bg-secondary'
}

</script>

<style scoped>
.file-name-cell {
  position: relative;
  display: inline-block;
  font-size: 10px;
  cursor: pointer;
}

.truncated {
  display: inline-block;
  max-width: 220px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: middle;
}

.file-name-cell .tooltip {
  font-size: 10px;
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translate(-50%, -6px);
  z-index: 1050;
  display: inline-block;
  border-radius: 6px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
}

.file-name-cell .tooltip .tooltip-inner {
  display: inline-block;
  max-width: 560px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #fff;
  background: rgba(0, 0, 0, 0.85);
  padding: 6px 8px;
  border-radius: 6px;
}

.file-name-cell .tooltip .file-full {
  display: inline-block;
  max-width: 460px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #fff;
  user-select: text
}

.file-name-cell .btn-copy {
  font-size: 10px;
  padding: 2px 6px;
  margin-left: 8px
}
.file-name-cell .tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  border-width: 6px;
  border-style: solid;
  border-color: rgba(0, 0, 0, 0.85) transparent transparent transparent;
}
.file-name-cell .tooltip.tooltip-down {
  bottom: auto;
  border-width: 8px;
  top: 100%;
  transform: translate(-50%, 5px);
}
.file-name-cell .tooltip.tooltip-down::after {
  top: -11.5px;
  border-color: transparent transparent rgba(0, 0, 0, 0.85) ;
}
.file-name-cell.is-active .truncated {
  background: rgba(0,0,0,0.04);
  box-shadow: inset 0 0 0 1px rgba(0,0,0,0.06);
  border-radius: 3px;
}
</style>
