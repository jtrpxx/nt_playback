<template>
  <div v-if="modelValue" class="modal-backdrop" @click.self="close" id="myFavoriteSearchModal">
    <div class="modal-box">
      <div class="modal-header">
        <h5 class="modal-title">My Favorite Search</h5>
        <button type="button" class="btn-close" @click="close">×</button>
      </div>
      <div class="modal-body">
        <div class="tabs-header">
          <div class="tab-buttons">
            <button :class="['tab-btn', { active: activeTab === 'list' }]" @click.prevent="activeTab = 'list'">List My Favorite</button>
            <button :class="['tab-btn', { active: activeTab === 'add' }]" id="tab-btn-add"
              @click.prevent="activeTab = 'add'">Create My Favorite</button>
            <button :class="['tab-btn', { active: activeTab === 'edit' }]" @click.prevent="activeTab = 'edit'">Edit My Favorite</button>
          </div>
          <div v-if="activeTab === 'list'" class="search-group" style="width: 260px; position: relative;">
            <i class="fa-solid fa-magnifying-glass search-icon"></i>
            <input type="text" v-model="searchTerm" class="form-control form-control-sm search-input"
              placeholder="Search...">
          </div>
        </div>

        <div class="tabs-content">
          <div :class="['tab-pane', { active: activeTab === 'list' }]">
            <div class="card-header-role" style="justify-content: space-between; align-items: center;">
              <div style="display: flex; align-items: center; gap: 12px;"></div>
              <div style="display: flex; align-items: center; gap: 10px;"></div>
            </div>

            <div class="card card-custom-role" style="border: 2px dashed #e2e8f0;">
              <div class="custom-roles-list" style="padding: 10px;max-height: 396px !important; overflow:auto !important;">
                <template v-if="favorites && favorites.length">
                  <div v-for="favorite in filteredFavorites" :key="favorite.id" class="custom-role-item"
                    @click="applyFavorite(favorite)" style="cursor: pointer;" :data-id="favorite.id">
                    <div class="group-card-main">
                      <div class="group-card-header">
                        <span class="group-card-title">{{ favorite.favorite_name }}</span>
                        <span class="group-card-group-badge">My Favorite</span>
                      </div>
                      <div class="group-card-desc">{{ favorite.description || 'No description provided for this favorite.' }}</div>
                    </div>
                    <div class="custom-role-actions" @click.stop>
                      <span class="role-box-badge" style="cursor: pointer;" @click.stop="editFavorite(favorite)">Click
                        to edit</span>
                      <button type="button" class="group-delete-btn" @click.stop="deleteFavorite(favorite.id)"
                        title="Delete My Favorite">
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </div>
                </template>
                <div v-else class="empty-state" style="cursor: pointer; padding: 40px 0; text-align: center; color: #94a3b8;" @click="activeTab = 'add'">
                  <i class="fa-solid fa-plus-circle" style="font-size: 24px; margin-bottom: 10px;"></i>
                  <p>No favorites yet. Click to create.</p>
                </div>
                <div v-show="filteredFavorites.length === 0 && favorites && favorites.length" class="empty-state">
                  <i class="fa-solid fa-dove"></i>
                  <p>No My Favorite found matching your search.</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Add Tab (simplified, kept structure) -->
          <div :class="['tab-pane', { active: activeTab === 'add' }]">
            <div class="tab-placeholder">
              <div class="favorite-card">
                <form id="addFavoriteForm" @submit.prevent>
                  <div class="permissions-grid-1">
                    <div class="input-group" v-has-value>
                      <input required="" type="text" name="firstNameModal" autocomplete="off" class="input">
                      <label class="title-label">First Name</label>
                    </div>
                    <div class="input-group" v-has-value>
                      <input required="" type="text" name="descriptionModal" autocomplete="off" class="input">
                      <label class="title-label">Description</label>
                    </div>
                  </div>

                  <div class="permissions-grid">
                    <div class="input-group">
                      <CustomSelect class="select-search select-checkbox" v-model="filters.databaseServer"
                        :options="mainDbOptions" placeholder="Database Server" name="databaseServerModal" />
                    </div>

                    <div class="input-group" v-has-value>
                      <input ref="fromInput" required type="text" name="fromModal" autocomplete="off" class="input">
                      <label class="title-label">From</label>
                      <span class="calendar-icon" @click="fromInput && fromInput.focus()"><i
                          class="fa-regular fa-calendar"></i></span>
                    </div>

                    <div class="input-group" v-has-value>
                      <input ref="toInput" required type="text" name="toModal" autocomplete="off" class="input">
                      <label class="title-label">To</label>
                      <span class="calendar-icon" @click="toInput && toInput.focus()"><i
                          class="fa-regular fa-calendar"></i></span>
                    </div>

                    <div class="input-group" v-has-value>
                      <input required="" type="text" name="durationModal" autocomplete="off" class="input">
                      <label class="title-label">Duration</label>
                    </div>

                    <div class="input-group" v-has-value>
                      <input required="" type="text" name="fileNameModal" autocomplete="off" class="input">
                      <label class="title-label">File Name</label>
                    </div>

                    <div class="input-group">
                      <CustomSelect class="select-checkbox"
                        :options="[{ label: 'All', value: 'All' }, { label: 'Internal', value: 'Internal' }, { label: 'Inbound', value: 'Inbound' }, { label: 'Outbound', value: 'Outbound' }]"
                        placeholder="Call Direction" name="callDirectionModal" />
                    </div>

                    <div class="input-group" v-has-value>
                      <input required="" type="text" name="customerNumberModal" autocomplete="off" class="input">
                      <label class="title-label">Customer Number</label>
                    </div>

                    <div class="input-group" v-has-value>
                      <input required="" type="text" name="extensionModal" autocomplete="off" class="input">
                      <label class="title-label">Extension</label>
                    </div>

                    <div class="input-group">
                      <CustomSelect class="select-search select-checkbox" v-model="filters.agent"
                        :options="agentOptions" placeholder="Agent" name="agentModal" />
                    </div>

                    <div class="input-group" v-has-value>
                      <input required="" type="text" name="fullNameModal" autocomplete="off" class="input">
                      <label class="title-label">Full Name</label>
                    </div>

                    <div class="input-group" v-has-value>
                      <input required="" type="text" name="customFieldModal" autocomplete="off" class="input">
                      <label class="title-label">Custom Field</label>
                    </div>
                  </div>

                </form>
              </div>
            </div>
          </div>

          <div :class="['tab-pane', { active: activeTab === 'edit' }]">
            <div id="edit-placeholder" :class="['empty-tab-placeholder', { 'd-none': !showEditPlaceholder }]" style="cursor: pointer;" @click="activeTab = 'list'">
              <i class="fa-solid fa-pen-to-square"></i>Select a my favorite to edit.
            </div>
            <div id="edit-form-container" :class="['tab-placeholder', { 'd-none': !showEditForm }]" >
              <div class="favorite-card">
                <form id="addFavoriteForm" @submit.prevent>
                  <div class="permissions-grid-1">
                    <div class="input-group" v-has-value>
                      <input v-model="editForm.firstName" required="" type="text" name="firstNameModal" autocomplete="off" class="input">
                      <label class="title-label">First Name</label>
                    </div>
                    <div class="input-group" v-has-value>
                      <input v-model="editForm.description" required="" type="text" name="descriptionModal" autocomplete="off" class="input">
                      <label class="title-label">Description</label>
                    </div>
                  </div>

                  <div class="permissions-grid">
                    <div class="input-group">
                      <CustomSelect class="select-search select-checkbox" v-model="editForm.databaseServer"
                        :options="mainDbOptions" placeholder="Database Server" name="databaseServerEdit" />
                    </div>

                    <div class="input-group" v-has-value>
                      <input v-model="editForm.from" ref="fromInput" required type="text" name="fromModal" autocomplete="off" class="input">
                      <label class="title-label">From</label>
                      <span class="calendar-icon" @click="fromInput && fromInput.focus()"><i
                          class="fa-regular fa-calendar"></i></span>
                    </div>

                    <div class="input-group" v-has-value>
                      <input v-model="editForm.to" ref="toInput" required type="text" name="toModal" autocomplete="off" class="input">
                      <label class="title-label">To</label>
                      <span class="calendar-icon" @click="toInput && toInput.focus()"><i
                          class="fa-regular fa-calendar"></i></span>
                    </div>

                    <div class="input-group" v-has-value>
                      <input v-model="editForm.duration" required="" type="text" name="durationModal" autocomplete="off" class="input">
                      <label class="title-label">Duration</label>
                    </div>

                    <div class="input-group" v-has-value>
                      <input v-model="editForm.fileName" required="" type="text" name="fileNameModal" autocomplete="off" class="input">
                      <label class="title-label">File Name</label>
                    </div>

                    <div class="input-group">
                      <CustomSelect class="select-checkbox" v-model="editForm.callDirection"
                        :options="[{ label: 'All', value: 'All' }, { label: 'Internal', value: 'Internal' }, { label: 'Inbound', value: 'Inbound' }, { label: 'Outbound', value: 'Outbound' }]"
                        placeholder="Call Direction" name="callDirectionEdit" />
                    </div>

                    <div class="input-group" v-has-value>
                      <input v-model="editForm.customerNumber" required="" type="text" name="customerNumberModal" autocomplete="off" class="input">
                      <label class="title-label">Customer Number</label>
                    </div>

                    <div class="input-group" v-has-value>
                      <input v-model="editForm.extension" required="" type="text" name="extensionModal" autocomplete="off" class="input">
                      <label class="title-label">Extension</label>
                    </div>

                    <div class="input-group">
                      <CustomSelect class="select-search select-checkbox" v-model="editForm.agent"
                        :options="agentOptions" placeholder="Agent" name="agentEdit" />
                    </div>

                    <div class="input-group" v-has-value>
                      <input v-model="editForm.fullName" required="" type="text" name="fullNameModal" autocomplete="off" class="input">
                      <label class="title-label">Full Name</label>
                    </div>

                    <div class="input-group" v-has-value>
                      <input v-model="editForm.customField" required="" type="text" name="customFieldModal" autocomplete="off" class="input">
                      <label class="title-label">Custom Field</label>
                    </div>
                  </div>

                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button v-if="activeTab === 'add'" id="btn-reset-fav" class="btn-role btn-secondary" onclick="resetMyFavoriteSearch()"
          style="margin-right: auto;">
          <i class="fas fa-undo"></i>
          Reset
        </button>

        <button class="btn-role btn-secondary" @click="close()">
          <i class="fas fa-times"></i>
          Cancel
        </button>

        <button v-if="activeTab === 'add' || activeTab === 'edit'" id="btn-save-fav" class="btn-role btn-primary">
          <i class="fas fa-save"></i>
          Save Changes
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref, computed, reactive, onMounted, watch } from 'vue'
import CustomSelect from './CustomSelect.vue'
import '../assets/css/modal-favorite.css'

const props = defineProps({ modelValue: { type: Boolean, default: false }, favorites: { type: Array, default: () => [] }, mainDbOptions: { type: Array, default: () => [] }, agentOptions: { type: Array, default: () => [] } })
const emit = defineEmits(['update:modelValue', 'apply', 'edit', 'delete'])
const activeTab = ref('list')
const searchTerm = ref('')

// local filter state for the add form (so CustomSelect v-model has a target)
const filters = reactive({ databaseServer: '' })

// Modal receives `mainDbOptions` and `agentOptions` as props from parent `Home.vue`.
// It uses those props directly in the template. No fallback fetch here to avoid
// duplicate network calls when parent already loaded the data.

const filteredFavorites = computed(() => {
  const q = String(searchTerm.value || '').trim().toLowerCase()
  if (!q) return props.favorites
  return props.favorites.filter(f => (String(f.favorite_name || '') + ' ' + String(f.description || '')).toLowerCase().includes(q))
})

// edit form state
const editForm = reactive({
  id: null,
  firstName: '',
  description: '',
  databaseServer: '',
  from: '',
  to: '',
  duration: '',
  fileName: '',
  callDirection: [],
  customerNumber: '',
  extension: '',
  agent: '',

  fullName: '',
  customField: ''
})

// control visibility of the edit-placeholder helper text
const showEditPlaceholder = ref(true)
// control visibility of the edit form container
const showEditForm = ref(false)

// reset placeholder when modal opens
watch(() => props.modelValue, (val) => {
  if (val) {
    showEditPlaceholder.value = true
    showEditForm.value = false
  }
})

function close() { emit('update:modelValue', false) }
function applyFavorite(f) { emit('apply', f); emit('update:modelValue', false) }
function editFavorite(f) {
  // populate editForm from favorite.raw_data and metadata
  try {
    const raw = typeof f.raw_data === 'string' ? JSON.parse(f.raw_data || '{}') : (f.raw_data || {})
    editForm.id = f.id || null
    editForm.firstName = f.favorite_name || ''
    editForm.description = f.description || ''

    // map raw keys
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
    for (const [k, v] of Object.entries(raw)) {
      const t = keyMap[k]
      if (!t || !Object.prototype.hasOwnProperty.call(editForm, t)) continue

      // normalize multi-select fields (these CustomSelects use checkbox mode)
      if (['databaseServer', 'agent', 'callDirection'].includes(t)) {
        // build an array of values
        let vals = []
        if (v == null || v === '') {
          vals = []
        } else if (Array.isArray(v)) {
          vals = v.slice()
        } else if (typeof v === 'string') {
          if (v.indexOf(',') !== -1) vals = v.split(',').map(x => x.trim()).filter(Boolean)
          else vals = [v]
        } else {
          vals = [v]
        }

        // convert types/casing to match option values
        if (t === 'databaseServer' || t === 'agent') {
          // ids: convert numeric strings to numbers
          vals = vals.map(x => { const s = String(x).trim(); return /^\d+$/.test(s) ? Number(s) : s })
        }
        if (t === 'callDirection') {
          // normalize to capitalized form (Inbound, Outbound, Internal, All)
          vals = vals.map(x => { const s = String(x || '').trim(); return s ? (s.charAt(0).toUpperCase() + s.slice(1).toLowerCase()) : s })
        }

        editForm[t] = vals
      } else {
        editForm[t] = v
      }
    }
    // hide the placeholder helper, show edit form and switch to edit tab
    showEditPlaceholder.value = false
    showEditForm.value = true
    activeTab.value = 'edit'
    // optionally focus first input in edit form after render
  } catch (e) {
    console.error('editFavorite parse error', e)
  }
}
function deleteFavorite(id) { emit('delete', id) }
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000
}

.modal-box {
  background: #fff;
  border-radius: 8px;
  width: 800px;
  max-width: 90%;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  overflow: hidden
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid #eee
}

.modal-title {
  margin: 0;
  font-size: 14px
}

.btn-close {
  background: transparent;
  border: none;
  font-size: 18px;
  line-height: 1;
  cursor: pointer
}

.modal-body {
  padding: 16px;
  font-size: 13px
}

.modal-footer {
  padding: 12px 16px;
  border-top: 1px solid #eee;
  text-align: right
}

.tabs-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px
}

.tabs-header .tab-buttons {
  display: flex;
  gap: 8px
}

.tab-btn {
  padding: 6px 10px;
  border-radius: 6px;
  border: none;
  background: #f3f4f6;
  cursor: pointer
}

.tab-btn.active {
  background: #e2e8f0
}

.custom-role-item {
  display: flex;
  justify-content: space-between;
  padding: 8px;
  border-radius: 6px;
  background: #fff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03)
}

.group-card-title {
  font-weight: 600
}

.group-card-desc {
  font-size: 10px;
  color: #6b7280
}

.custom-role-actions {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 10px;
}

@keyframes fadeInTab {
  from {
    opacity: 0;
    transform: translateY(5px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* แก้ไขข้อขัดแย้งกับ Bootstrap .modal */
#myFavoriteSearchModal .modal {
  display: flex !important;
  /* บังคับให้แสดงผล (แก้ display: none ของ Bootstrap) */
  position: relative !important;
  /* ให้จัดกึ่งกลางตาม Flexbox ของ Overlay */
  top: auto !important;
  /* ยกเลิกการจัดตำแหน่งแบบ Absolute/Fixed เดิม */
  left: auto !important;
  width: 90%;
  /* กำหนดความกว้างตาม Design เดิม */
  /* height: auto !important; */
  transform: scale(0.9);
  /* เริ่มต้นให้เล็กนิดนึงเพื่อรอ Animation */
  transition: all 0.3s ease;
  z-index: 1006;
}

#myFavoriteSearchModal.show .modal {
  transform: scale(1) !important;
  /* ขยายเต็มเมื่อแสดงผล */
}

/* Fix scrolling to be inside tabs-content only */
#myFavoriteSearchModal .modal-body {
  padding: 0 !important;
  overflow: hidden !important;
  display: flex !important;
  flex-direction: column;
  min-height: 0;
  /* ช่วยให้ Flex item หดตัวได้เมื่อ content ยาวเกิน */
}

/* Allow select dropdowns to escape clipping of inner containers (show full list) */
#myFavoriteSearchModal .modal-body,
#myFavoriteSearchModal .tabs-content,
#myFavoriteSearchModal .favorite-card,
#myFavoriteSearchModal .custom-roles-list {
  overflow: visible !important;
}

.btn-secondary {
  background: #f1f5f9 !important;
  border: 1px solid #e2e8f0 !important;
  color: #64748b !important;
}

.btn-secondary:hover {
  background: #e2e8f0 !important;
  color: #1e293b !important;
}

/* Tabs Styling */
#myFavoriteSearchModal .tabs-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e2e8f0;
  margin: 0px 24px 0 24px;
  flex-shrink: 0;
  gap: 24px;
}

#myFavoriteSearchModal .tab-buttons {
  display: flex;
  gap: 24px;
}

#myFavoriteSearchModal .tab-btn {
  background: none;
  border: none;
  padding: 12px 4px;
  font-size: 12px;
  font-weight: 500;
  color: #64748b;
  cursor: pointer;
  position: relative;
  transition: all 0.2s ease;
}

#myFavoriteSearchModal .tab-btn:hover {
  color: #416fd6;
}

#myFavoriteSearchModal .tab-btn.active {
  color: #416fd6;
  font-weight: 600;
}

#myFavoriteSearchModal .tab-btn.active::after {
  content: "";
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 2px;
  background: #416fd6;
  border-radius: 2px 2px 0 0;
}

#myFavoriteSearchModal .tabs-content {
  flex: 1;
  overflow: hidden;
  /* ปิด scroll ที่ container ใหญ่ */
  padding: 12px 23px 11px 22px;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

#myFavoriteSearchModal .tab-pane {
  display: none;
  animation: fadeInTab 0.3s ease;
  flex: 1;
  min-height: 400px;
  flex-direction: column;
}

#myFavoriteSearchModal .tab-pane.active {
  display: flex;
}

@keyframes fadeInTab {
  from {
    opacity: 0;
    transform: translateY(5px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.empty-tab-placeholder {
  padding: 60px 20px;
  text-align: center;
  color: #94a3b8;
  background: #ffffff;
  border-radius: 16px;
  border: 2px dashed #e2e8f0;
  font-size: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  height: 100%;
  overflow-y: auto;
  flex: 1;
  min-height: 0;
  transition: all 0.2s ease;
}

.empty-tab-placeholder:hover {
  border-color: #416fd6;
  background-color: #f8fafc;
  color: #416fd6;
}

.empty-tab-placeholder i {
  font-size: 32px;
  margin-bottom: 12px;
  opacity: 0.5;
  transition: all 0.2s ease;
}

.empty-tab-placeholder:hover i {
  opacity: 1;
  transform: scale(1.1);
}

.tab-placeholder {
  border: none;
  display: block;
  text-align: left;
  color: inherit;
  padding: 0;
  background: transparent;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}

.favorite-card {
  background: #ffffff;
  padding: 12px;
  border-radius: 16px;
  border: 2px dashed #e2e8f0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
  flex: 1;
  min-height: 400px;
}

.favorite-card::-webkit-scrollbar {
  width: 4px;
}

.favorite-card::-webkit-scrollbar-track {
  border: 2px dashed #e2e8f0;
  margin-top: 6px;
  margin-bottom: 6px;
}

.favorite-card::-webkit-scrollbar-thumb {
  background-color: #416fd6;
  border-radius: 4px;
}

.form-label-modal {
  font-size: 12px !important;
}

/* Ensure CustomSelect dropdowns inside modal appear above favorite-card and other containers */
#myFavoriteSearchModal .favorite-card {
  overflow: visible !important;
}
#myFavoriteSearchModal .options {
  z-index: 4000 !important;
  position: absolute !important;
}

.empty-tab-placeholder {
  padding: 60px 20px;
  text-align: center;
  color: #94a3b8;
  background: #ffffff;
  border-radius: 16px;
  border: 2px dashed #e2e8f0;
  font-size: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  height: 100%;
  overflow-y: auto;
  flex: 1;
  min-height: 0;
  transition: all 0.2s ease;
}

.empty-tab-placeholder:hover {
  border-color: #416fd6;
  background-color: #f8fafc;
  color: #416fd6;
}

.empty-tab-placeholder i {
  font-size: 32px;
  margin-bottom: 12px;
  opacity: 0.5;
  transition: all 0.2s ease;
}

.empty-tab-placeholder:hover i {
  opacity: 1;
  transform: scale(1.1);
}

.tab-placeholder {
  border: none;
  display: block;
  text-align: left;
  color: inherit;
  padding: 0;
  background: transparent;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}

.favorite-card {
  background: #ffffff;
  padding: 12px;
  border-radius: 16px;
  border: 2px dashed #e2e8f0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
  flex: 1;
  min-height: 0;
}

.favorite-card::-webkit-scrollbar {
  width: 4px;
}

.favorite-card::-webkit-scrollbar-track {
  border: 2px dashed #e2e8f0;
  margin-top: 6px;
  margin-bottom: 6px;
}

.favorite-card::-webkit-scrollbar-thumb {
  background-color: #416fd6;
  border-radius: 4px;
}

.form-label-modal {
  font-size: 12px !important;
}
</style>
