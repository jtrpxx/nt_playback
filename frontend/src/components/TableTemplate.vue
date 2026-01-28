<template>
  <div class="table-container">
    <div class="table-responsive table-scroll">
      <table class="table table-sm table-striped">
        <thead class="table-primary">
          <tr>
            <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(r, idx) in rows" :key="r.id ?? idx">
            <td v-for="col in columns" :key="col.key">
              <slot :name="`cell-${col.key}`" :row="r" :index="idx">
                <template v-if="col.isIndex">{{ startIndex + idx + 1 }}</template>
                <template v-else-if="col.tooltip">
                  <div class="file-name-cell" :class="{ 'is-active': activeTooltip === idx }" @mouseenter="activeTooltip = idx" @mouseleave="activeTooltip = null">
                    <span class="truncated">{{ truncate(r[col.key], 20) }}</span>
                    <div v-if="activeTooltip === idx" class="tooltip bs-tooltip-top show" role="tooltip" @mousedown.stop @mouseup.stop @click.stop>
                      <div class="tooltip-inner d-flex align-items-center">
                        <span class="file-full me-2">{{ r[col.key] }}</span>
                        <button class="btn btn-sm btn-outline-secondary btn-copy" @click="copyFileName(r[col.key], idx)" :aria-label="copiedIndex===idx ? 'Copied' : 'Copy'">
                          <i :class="copiedIndex === idx ? 'fa-solid fa-check' : 'fa-regular fa-copy'"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </template>
                <template v-else-if="callDirectionKey && col.key === callDirectionKey">
                  <span :class="['badge', callDirectionClass(r[col.key]) ]">{{ r[col.key] }}</span>
                </template>
                <template v-else-if="col.isAction">
                  <div class="group-card-actions">
                      <button class="group-edit-btn" @click.stop="$emit('edit', r)">Click to edit</button>
                      <button type="button" class="group-delete-btn" @click.stop="$emit('delete', r)">
                          <i class="fas fa-trash" style="font-size: 12px;"></i>
                      </button>
                  </div>
                </template>
                <template v-else>{{ r[col.key] }}</template>
              </slot>
            </td>
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
            <span class="selected">{{ props.perPage }}</span>
            <i class="fa-solid fa-caret-down "></i>
          </button>
          <ul v-if="perDropdownOpen" class="custom-select-menu">
            <li v-for="opt in props.perPageOptions" :key="opt" :class="{ active: opt === props.perPage }" @click="setPerPage(opt)">{{ opt }}</li>
          </ul>
        </div>
        entries per page, Showing {{ startItem }} to {{ endItem }} of {{ props.totalItems }} entries
      </div>
    </div>
    <nav>
      <ul class="pagination pagination-sm mb-0">
        <li class="page-item" :class="{ disabled: props.currentPage === 1 }"><button class="page-link" @click="changePage(props.currentPage - 1)">Previous</button></li>
        <li class="page-item" v-for="p in pagesToShow" :key="String(p)" :class="[{ active: p === props.currentPage }, { disabled: p === '...' }]">
          <button v-if="p !== '...'" class="page-link" @click="changePage(p)">{{ p }}</button>
          <span v-else class="page-link">…</span>
        </li>
        <li class="page-item" :class="{ disabled: props.currentPage === totalPages }"><button class="page-link" @click="changePage(props.currentPage + 1)">Next</button></li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  columns: { type: Array, required: true },
  rows: { type: Array, default: () => [] },
  startIndex: { type: Number, default: 0 },
  loading: { type: Boolean, default: false },
  callDirectionKey: { type: String, default: '' },
  // pagination-related props (UI-only)
  perPage: { type: Number, default: 50 },
  perPageOptions: { type: Array, default: () => [50, 100, 500, 1000] },
  currentPage: { type: Number, default: 1 },
  totalItems: { type: Number, default: 0 }
})

const emit = defineEmits(['edit', 'delete', 'page-change', 'per-change'])

const activeTooltip = ref(null)
const copiedIndex = ref(null)

// per-page dropdown state (local UI)
const perWrap = ref(null)
const perDropdownOpen = ref(false)
const perDropdownUp = ref(false)

const togglePerDropdown = () => {
  perDropdownOpen.value = !perDropdownOpen.value
  if (perDropdownOpen.value) {
    const wrap = perWrap.value
    if (wrap) {
      const rect = wrap.getBoundingClientRect()
      const spaceBelow = window.innerHeight - rect.bottom
      const estimatedMenuHeight = Math.min(300, props.perPageOptions.length * 40 + 12)
      perDropdownUp.value = spaceBelow < estimatedMenuHeight
    } else {
      perDropdownUp.value = false
    }
  }
}

const onDocClick = (e) => { if (perWrap.value && !perWrap.value.contains(e.target)) perDropdownOpen.value = false }

onMounted(() => document.addEventListener('click', onDocClick))
onBeforeUnmount(() => document.removeEventListener('click', onDocClick))

const totalPages = computed(() => Math.max(1, Math.ceil(props.totalItems / props.perPage)))
const startIndexLocal = computed(() => (props.currentPage - 1) * props.perPage)
const paginatedRecords = computed(() => props.rows)
const startItem = computed(() => props.totalItems === 0 ? 0 : startIndexLocal.value + 1)
const endItem = computed(() => Math.min(props.totalItems, startIndexLocal.value + (props.rows.length || 0)))

const pagesToShow = computed(() => {
  const pages = []
  const total = totalPages.value
  if (total <= 6) {
    for (let i = 1; i <= total; i++) pages.push(i)
    return pages
  }
  const end = Math.min(5, total)
  for (let i = 1; i <= end; i++) pages.push(i)
  if (total > end + 1) pages.push('...')
  pages.push(total)
  return pages
})

const changePage = (p) => {
  if (p < 1) p = 1
  if (p > totalPages.value) p = totalPages.value
  emit('page-change', p)
}

const setPerPage = (opt) => {
  emit('per-change', opt)
  perDropdownOpen.value = false
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


.table-overlay { position: absolute; inset: 0; display:flex; align-items:center; justify-content:center; background: rgba(255,255,255,0.6); }
.overlay-box { padding: 12px 18px; background: rgba(0,0,0,0.6); color: #fff; border-radius: 6px }

</style>
