<template>
  <div class="custom-select-root" :class="{'is-open': open, 'has-value': hasValue, 'up': up}" ref="root">
    <button type="button" class="select-toggle" @click="toggle" @keydown.down.prevent="openList" @keydown.up.prevent="openList" :aria-expanded="open" :aria-haspopup="true">
      <span class="selected-text">{{ hasValue ? selectedLabel : '' }}</span>
      <span class="chev" aria-hidden><i class="fa-solid fa-angle-down" style="font-size: 12px;"></i></span>
    </button>
    <label class="floating-label">{{ placeholder }}</label>

    <ul v-if="open" class="options" role="listbox">
      <li v-if="searchable" class="option option-search">
        <div class="search-input-wrap">
          <i class="fa-solid fa-magnifying-glass search-icon" aria-hidden="true"></i>
          <input v-model="searchTerm" class="form-control form-control-sm select-search-input" placeholder="Search..." />
        </div>
      </li>
      <li v-for="(opt, idx) in filteredOptions" :key="idx" class="option" :class="{selected: isSelected(opt.value)}" @click="onOptionClick(opt.value)" @mouseenter="hoverIndex=idx" @mouseleave="hoverIndex=null" :aria-selected="isSelected(opt.value)" role="option">
        <template v-if="checkboxable">
          <input type="checkbox" :checked="isSelected(opt.value)" @click.stop.prevent="select(opt.value)" />
          <span class="opt-label">{{ opt.label }}</span>
        </template>
        <template v-else>
          <span class="opt-label">{{ opt.label }}</span>
        </template>
        <span class="opt-check" aria-hidden v-if="!checkboxable && opt.value===modelValue"><i class="fa-solid fa-check"></i></span>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
const props = defineProps({
  modelValue: { type: [String, Number, null], default: '' },
  options: { type: Array, required: true },
  placeholder: { type: String, default: '' }
})
const emit = defineEmits(['update:modelValue'])

const open = ref(false)
const hoverIndex = ref(null)
const root = ref(null)
const up = ref(false)
const searchable = ref(false)
const checkboxable = ref(false)
const searchTerm = ref('')

const normalizedOptions = computed(() => props.options.map(o => (typeof o === 'string' ? { label: o, value: o } : o)))
const filteredOptions = computed(() => {
  const q = String(searchTerm.value || '').trim().toLowerCase()
  if (!searchable.value || !q) return normalizedOptions.value
  return normalizedOptions.value.filter(o => String(o.label).toLowerCase().includes(q))
})

const selectedLabel = computed(() => {
  if (checkboxable.value && Array.isArray(props.modelValue)) {
    const labels = normalizedOptions.value.filter(o => props.modelValue.includes(o.value)).map(o => o.label)
    if (labels.length === 0) return props.placeholder
    if (labels.length <= 3) return labels.join(', ')
    return `${labels.length} selected`
  }
  const sel = normalizedOptions.value.find(o => o.value === props.modelValue)
  return sel ? sel.label : props.placeholder
})

function isSelected(v) {
  if (checkboxable.value) return Array.isArray(props.modelValue) && props.modelValue.indexOf(v) !== -1
  return v === props.modelValue
}

const hasValue = computed(() => props.modelValue !== '' && props.modelValue !== null && props.modelValue !== undefined)

function toggle() { open.value = !open.value }
function openList() { open.value = true }
function computeUp() {
  if (!root.value) return
  const rect = root.value.getBoundingClientRect()

  // Find nearest ancestor that can clip/contain the dropdown (overflow auto|scroll|hidden).
  function findClippingAncestor(el) {
    let parent = el.parentElement
    while (parent && parent !== document.documentElement) {
      const style = getComputedStyle(parent)
      const overflowY = style.overflowY || ''
      const overflowX = style.overflowX || ''
      if (/(auto|scroll|hidden)/.test(overflowY) || /(auto|scroll|hidden)/.test(overflowX)) {
        return parent
      }
      parent = parent.parentElement
    }
    return document.documentElement
  }

  const clip = findClippingAncestor(root.value)
  let containerRect
  if (clip === document.documentElement) {
    containerRect = { top: 0, bottom: window.innerHeight }
  } else {
    containerRect = clip.getBoundingClientRect()
  }

  const spaceBelow = containerRect.bottom - rect.bottom
  const spaceAbove = rect.top - containerRect.top
  const estimatedMenuHeight = Math.min(400, normalizedOptions.value.length * 40 + 12)

  // Prefer opening downward unless not enough space; open upward when above has more space.
  if (spaceBelow >= estimatedMenuHeight) {
    up.value = false
  } else if (spaceAbove >= estimatedMenuHeight) {
    up.value = true
  } else {
    // choose the side with more space
    up.value = spaceAbove > spaceBelow
  }
}

watch(open, async (val) => {
  if (val) {
    await nextTick()
    computeUp()
    window.addEventListener('resize', computeUp)
    window.addEventListener('scroll', computeUp, true)
  } else {
    up.value = false
    window.removeEventListener('resize', computeUp)
    window.removeEventListener('scroll', computeUp, true)
  }
})
function select(v) {
  if (checkboxable.value) {
    const current = Array.isArray(props.modelValue) ? [...props.modelValue] : []
    const isAll = String(v).toLowerCase() === 'all'
    if (isAll) {
      // If 'All' was not selected, select every option; otherwise clear selection
      const allVals = normalizedOptions.value.map(o => o.value)
      const hasAllSelected = allVals.every(val => current.indexOf(val) !== -1)
      if (!hasAllSelected) {
        emit('update:modelValue', Array.from(new Set(allVals)))
      } else {
        emit('update:modelValue', [])
      }
    } else {
      const idx = current.indexOf(v)
      if (idx === -1) current.push(v)
      else current.splice(idx, 1)
      // remove 'all' keyword if present when selecting individual items
      const allIdx = current.findIndex(x => String(x).toLowerCase() === 'all')
      if (allIdx !== -1) current.splice(allIdx, 1)
      emit('update:modelValue', current)
    }
  } else {
    if (v === props.modelValue) emit('update:modelValue', '')
    else emit('update:modelValue', v)
    open.value = false
  }
}

function onOptionClick(v) {
  // For checkboxable selects, clicking the row should toggle the checkbox as well.
  select(v)
}

function onDocClick(e){ if (!root.value.contains(e.target)) open.value = false }
onMounted(()=> {
  document.addEventListener('click', onDocClick)
  if (root.value) {
    const cls = root.value.classList
    searchable.value = cls.contains('select-search')
    checkboxable.value = cls.contains('select-checkbox')
  }
})
onBeforeUnmount(()=> {
  document.removeEventListener('click', onDocClick)
  window.removeEventListener('resize', computeUp)
  window.removeEventListener('scroll', computeUp, true)
})
</script>

<style scoped>
.option-search .search-input-wrap{ position: relative; }
.option-search .search-icon{ position: absolute; left: 10px; top: 50%; transform: translateY(-50%); color: #9aa4ad; font-size: 10px; pointer-events: none; }
.option-search .select-search-input{ padding-left: 26px;border-radius: 25px;font-size: 10px }
</style>