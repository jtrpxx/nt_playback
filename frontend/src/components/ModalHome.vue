<template>
  <div v-if="modelValue" class="modal-backdrop" @click.self="close" id="myFavoriteSearchModal">
    <div class="modal-box">
      <div class="modal-header">
        <h5 class="modal-title">My Favorite Search</h5>
        <button type="button" class="btn-close" @click="close">×</button>
      </div>
        <div class="modal-body" >
            <div class="tabs-header">
                <button :class="['tab-btn',{ active: activeTab === 'list' }]" @click.prevent="activeTab = 'list'">List My Favorite</button>
                <button :class="['tab-btn',{ active: activeTab === 'add' }]" id="tab-btn-add" @click.prevent="activeTab = 'add'">Create My Favorite</button>
                <button :class="['tab-btn',{ active: activeTab === 'edit' }]" @click.prevent="activeTab = 'edit'">Edit My Favorite</button>
            </div>

            <div class="tabs-content">
                <div :class="['tab-pane', { active: activeTab === 'list' }]">
                    <div class="card-header-role" style="justify-content: space-between;">
                        <div style="display: flex; align-items: center; gap: 12px;"></div>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <div class="search-role-container">
                                <i class="fas fa-search"></i>
                                <input type="text" v-model="searchTerm" placeholder="Search..." @keydown.enter.prevent />
                            </div>
                        </div>
                    </div>

                    <div class="card card-custom-role" style="border: 2px dashed #e2e8f0;">
                        <div class="custom-roles-list" style="padding: 5px;max-height: 220px !important; overflow:auto;">
                            <template v-if="favorites && favorites.length">
                                <div v-for="favorite in filteredFavorites" :key="favorite.id" class="custom-role-item" @click="applyFavorite(favorite)" style="cursor: pointer;" :data-id="favorite.id">
                                    <div class="group-card-main">
                                        <div class="group-card-header">
                                            <span class="group-card-title">{{ favorite.favorite_name }}</span>
                                            <span class="group-card-group-badge">My Favorite</span>
                                        </div>
                                        <div class="group-card-desc">{{ favorite.description || 'No description provided for this favorite.' }}</div>
                                    </div>
                                    <div class="custom-role-actions" @click.stop>
                                        <span class="role-box-badge" style="cursor: pointer;" @click.stop="editFavorite(favorite)">Click to edit</span>
                                        <button type="button" class="group-delete-btn" @click.stop="deleteFavorite(favorite.id)" title="Delete My Favorite">
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
                                <div class="permissions-grid-2">
                                    <div class="form-group-modal">
                                        <label class="form-label-modal" for="create_favorite_name"><span style="color: red;">*</span>Favorite Name</label>
                                        <input type="text" class="form-input-modal" id="create_favorite_name" name="favorite_name" placeholder="favorite name" maxlength="30" required>
                                        <div class="validate d-none" id="validateAddMyfavoriteName"><i class="fa-solid fa-circle-exclamation"></i> This field is required</div>
                                    </div>
                                    <div class="form-group-modal">
                                        <label class="form-label-modal">Description</label>
                                        <input type="text" class="form-input-modal" id="createv_favorite_description" name="createv_favorite_description" placeholder="Description" maxlength="100">
                                    </div>
                                </div>

                                <div class="permissions-grid">
                                    <div class="form-group-modal">
                                        <label class="form-label-modal">Database Server</label>
                                        <select class="form-input-modal custom-select-modal" id="fav_database_name" name="database_name">
                                            <option value="" selected disabled>Select Server</option>
                                            <option value="all">All</option>
                                            <option v-for="opt in main_db" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                                        </select>
                                    </div>
                                    <div class="form-group-modal">
                                        <label class="form-label-modal">From</label>
                                        <input type="text" class="form-input-modal datetimepicker" id="fav_start_date" name="start_date" placeholder="From">
                                    </div>
                                    <div class="form-group-modal">
                                        <label class="form-label-modal">To</label>
                                        <input type="text" class="form-input-modal datetimepicker" id="fav_end_date" name="end_date" placeholder="To">
                                    </div>
                                </div>

                                <!-- other fields kept as plain inputs (no JS wiring) -->
                            </form>
                        </div>
                    </div>
                </div>

                <div :class="['tab-pane', { active: activeTab === 'edit' }]">
                    <div id="edit-placeholder" class="empty-tab-placeholder" style="cursor: pointer;">
                        <i class="fa-solid fa-pen-to-square"></i>Select a my favorite to edit.
                    </div>
                    <!-- edit form can be implemented similarly to add form if needed -->
                </div>
            </div>
        </div>
              <div class="modal-footer">
            <button id="btn-reset-fav" class="btn-role btn-secondary" onclick="resetMyFavoriteSearch()" style="margin-right: auto; display: none;">
                <i class="fas fa-undo"></i>
                Reset
            </button>
            <button class="btn-role btn-secondary" onclick="closeMyFavoriteSearch()">
                <i class="fas fa-times"></i>
                Cancel
            </button>
            <button id="btn-save-fav" class="btn-role btn-primary" style="display: none;">
                <i class="fas fa-save"></i>
                Save Changes
            </button>
        </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref, computed } from 'vue'
const props = defineProps({ modelValue: { type: Boolean, default: false }, favorites: { type: Array, default: () => [] }, main_db: { type: Array, default: () => [] } })
const emit = defineEmits(['update:modelValue','apply','edit','delete'])
const activeTab = ref('list')
const searchTerm = ref('')

const filteredFavorites = computed(() => {
    const q = String(searchTerm.value || '').trim().toLowerCase()
    if (!q) return props.favorites
    return props.favorites.filter(f => (String(f.favorite_name || '') + ' ' + String(f.description || '')).toLowerCase().includes(q))
})

function close(){ emit('update:modelValue', false) }
function applyFavorite(f){ emit('apply', f); emit('update:modelValue', false) }
function editFavorite(f){ emit('edit', f) }
function deleteFavorite(id){ emit('delete', id) }
</script>

<style scoped>
.modal-backdrop{ position: fixed; inset: 0; background: rgba(0,0,0,0.45); display:flex; align-items:center; justify-content:center; z-index:2000 }
.modal-box{ background:#fff; border-radius:8px; width:520px; max-width:90%; box-shadow:0 10px 30px rgba(0,0,0,0.2); overflow:hidden }
.modal-header{ display:flex; align-items:center; justify-content:space-between; padding:12px 16px; border-bottom:1px solid #eee }
.modal-title{ margin:0; font-size:14px }
.btn-close{ background:transparent; border:none; font-size:18px; line-height:1; cursor:pointer }
.modal-body{ padding:16px; font-size:13px }
.modal-footer{ padding:12px 16px; border-top:1px solid #eee; text-align:right }
.tabs-header{ display:flex; gap:8px; margin-bottom:12px }
.tab-btn{ padding:6px 10px; border-radius:6px; border:none; background:#f3f4f6; cursor:pointer }
.tab-btn.active{ background:#e2e8f0 }
.custom-role-item{ display:flex; justify-content:space-between; padding:8px; border-radius:6px; margin-bottom:6px; background:#fff; box-shadow:0 1px 2px rgba(0,0,0,0.03) }
.group-card-title{ font-weight:600 }
.group-card-desc{ font-size:12px; color:#6b7280 }
.custom-role-actions{ display:flex; gap:8px; align-items:center }
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
  display: flex !important; /* บังคับให้แสดงผล (แก้ display: none ของ Bootstrap) */
  position: relative !important; /* ให้จัดกึ่งกลางตาม Flexbox ของ Overlay */
  top: auto !important; /* ยกเลิกการจัดตำแหน่งแบบ Absolute/Fixed เดิม */
  left: auto !important;
  width: 90%; /* กำหนดความกว้างตาม Design เดิม */
  /* height: auto !important; */
  transform: scale(0.9); /* เริ่มต้นให้เล็กนิดนึงเพื่อรอ Animation */
  transition: all 0.3s ease;
  z-index: 1006;
}

#myFavoriteSearchModal.show .modal {
  transform: scale(1) !important; /* ขยายเต็มเมื่อแสดงผล */
}

/* Fix scrolling to be inside tabs-content only */
#myFavoriteSearchModal .modal-body {
  padding: 0 !important;
  overflow: hidden !important;
  display: flex !important;
  flex-direction: column;
  min-height: 0; /* ช่วยให้ Flex item หดตัวได้เมื่อ content ยาวเกิน */
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
  border-bottom: 1px solid #e2e8f0;
  margin: 0px 24px 0 24px;
  flex-shrink: 0;
  gap: 24px;
}

#myFavoriteSearchModal .tab-btn {
  background: none;
  border: none;
  padding: 12px 4px;
  font-size: 15px;
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
  overflow: hidden; /* ปิด scroll ที่ container ใหญ่ */
  padding: 12px 23px 11px 22px;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

#myFavoriteSearchModal .tab-pane {
  display: none;
  animation: fadeInTab 0.3s ease;
  flex: 1;
  min-height: 0;
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

input:not([type="submit"]):not([type="radio"]):not([type="checkbox"]):not(input[type="search"]),
textarea {
  font-size: 16px !important;
  max-height: 30px ;
}
.card-header-role {
  margin-bottom: 9px !important;
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

input:not([type="submit"]):not([type="radio"]):not([type="checkbox"]):not(input[type="search"]),
textarea {
  font-size: 16px !important;
  max-height: 30px ;
}
.card-header-role {
  margin-bottom: 9px !important;
}

</style>
