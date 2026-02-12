<template>
    <MainLayout>
        <div class="main-wrapper container-fluid py-3">
            <Breadcrumbs :items="[{ text: 'Home', to: '/' }, { text: 'Set Column' }]" />
            <div class="col-lg-12">
                <div class="card">
                    <div class="card-body card-body-datatable" style="position: relative;">
                        <div class="d-flex align-items-start justify-content-between" style="margin-bottom: 6px;">
                            <div class="d-flex align-items-center">
                                <div class="d-flex align-items-center justify-content-center me-1"
                                    style="width:35px;height:35px;background-color: #D9E2F6;border-radius: 10px !important;">
                                    <i class="fa-solid fa-gear" style="color:#2b6cb0;font-size:18px"></i>
                                </div>
                                <h5 class="card-title mb-2 mt-1">Set Column</h5>
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
                                    Add New Column
                                </button>
                            </div>
                        </div>

                        <!-- Content Column here. -->
                        <div class="custom-roles-list" id="customRolesList">
                            <template v-if="loading">
                                <div class="table-overlay" style="height: 487px;">
                                    <div class="overlay-box">Loading...</div>
                                </div>
                            </template>
                            <template v-else>
                                <div v-if="columns.length">
                                    <div v-if="filteredColumns.length" class="group-list" style="margin-top: 4px;">
                                        <div v-for="column in filteredColumns" :key="column.id"
                                            :class="['group-card-item', { active: selectedColumnId === column.id }]"
                                            @click.stop="selectColumn(column)">
                                            <div class="group-card-main">
                                                <div class="group-card-header">
                                                    <span class="group-card-title">{{ column.name }}</span>
                                                    <label class="switch_status">
                                                        <input type="checkbox" :checked="column.use"
                                                            @change="() => toggleSetColumnUse(column.user?.id, column)" />
                                                        <span class="slider_status round"></span>
                                                    </label>
                                                </div>
                                                <div class="group-card-desc">
                                                    {{ column.description || 'No description provided for this column.' }}
                                                </div>
                                            </div>

                                            <div class="group-card-actions">
                                                <button class="group-edit-btn" @click.stop="openEditColumn(column.id)">
                                                    Click to edit
                                                </button>
                                                <button type="button" class="group-delete-btn"
                                                    @click.stop="deleteColumn(column.id)">
                                                    <i class="fas fa-trash" style="font-size: 12px;"></i>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                    <div v-else class="empty-state">
                                        <i class="fa-solid fa-dove"></i>
                                        <p>This column not found.</p>
                                    </div>
                                </div>

                                <div v-else class="empty-state">
                                    <i class="fa-solid fa-chart-column"></i>
                                    <p>No columns yet. Click "Add New Column" to create one.</p>
                                </div>
                            </template>
                        </div>


                    </div>
                </div>
            </div>
        </div>
    </MainLayout>
    <ModalSetColumn v-model="showModal" :mode="modalMode" :columnData="editColumnData" @saved="onModalSaved"/>
</template>


<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import MainLayout from '../layouts/MainLayout.vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'
import { API_GET_COLUMN_AUDIO_RECORD } from '../api/paths'
import { registerRequest } from '../utils/pageLoad'
import ModalSetColumn from '../components/ModalSetColumn.vue'
import { showToast, confirmDelete } from '../assets/js/function-all'
import { ensureCsrf, getCsrfToken } from '../api/csrf'
import { API_SAVE_COLUMN_AUDIO_RECORD } from '../api/paths'

const searchQuery = ref('')
const columns = ref([])
const selectedColumnId = ref(null)
const loading = ref(false)

const showModal = ref(false)
const modalMode = ref('createColumn')
const editColumnData = ref(null)

// Placeholder for API path if not exists in global paths

const filteredColumns = computed(() => {
    const q = (searchQuery.value || '').toLowerCase().trim()
    if (!q) return columns.value
    return columns.value.filter(c => (c.name || '').toLowerCase().includes(q))
})

const fetchGetColumnAudioRecord = async (showLoading = true) => {
    const task = (async () => {
        if (showLoading) loading.value = true
        try {
            const res = await fetch(API_GET_COLUMN_AUDIO_RECORD(), { credentials: 'include' })
            if (!res.ok) return
            const json = await res.json()
            columns.value = json.data || []
        } catch (err) {
            console.error('fetchGetColumnAudioRecord error', err)
        } finally {
            if (showLoading) loading.value = false
        }
    })()
    registerRequest(task)
    await task
}

onMounted(() => {
    fetchGetColumnAudioRecord()
})

function onTyping() {
    // Client-side filtering handled by computed
}

function onSearch() {
    // Client-side filtering handled by computed
}

function selectColumn(column) {
    selectedColumnId.value = column.id
}

// Placeholders for template actions
function openCreateGroup() {
    modalMode.value = 'createColumn'
    editColumnData.value = null
    showModal.value = true
}

function openEditColumn(id) {
    const col = columns.value.find(c => c.id === id)
    if (col) {
        editColumnData.value = col
        modalMode.value = 'editColumn'
        showModal.value = true
    }
}

async function deleteColumn(id) {
    const confirmed = await confirmDelete()
    if (!confirmed) return
    
    // Reuse onModalSaved logic with action='delete'
    await onModalSaved({ id, action: 'delete' })
}

async function toggleSetColumnUse(userId, column) {
    const newUse = !column.use
    
    // Optimistic update: update UI immediately without waiting for server
    const previousColumns = JSON.stringify(columns.value)
    
    if (newUse) {
        // Enable this one, disable others
        columns.value.forEach(c => {
            c.use = (c.id === column.id)
        })
    } else {
        column.use = false
    }

    try {
        await ensureCsrf()
        const csrfToken = getCsrfToken()
        
        const payload = {
            action: 'toggle',
            id: column.id,
            use: newUse,
            name: column.name,
            description: column.description,
            raw_data: column.raw_data
        }

        const res = await fetch(API_SAVE_COLUMN_AUDIO_RECORD(), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken || '' },
            body: JSON.stringify(payload)
        })
        
        const json = await res.json()
        if (json.status === 'success') {
            showToast(json.message, 'success')
            // No need to fetch again, state is already updated
        } else {
            showToast(json.message || 'Failed to update status', 'error')
            columns.value = JSON.parse(previousColumns) // Revert
        }
    } catch (e) {
        console.error('Error toggling column', e)
        showToast('An error occurred', 'error')
        columns.value = JSON.parse(previousColumns) // Revert
    }
}

async function onModalSaved(data) {
    try {
        await ensureCsrf()
        const csrfToken = getCsrfToken()
        
        // Prepare payload
        const payload = { ...data }
        if (!payload.action) {
            payload.action = (modalMode.value === 'createColumn') ? 'create' : 'update'
        }

        const res = await fetch(API_SAVE_COLUMN_AUDIO_RECORD(), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken || '' },
            body: JSON.stringify(payload)
        })
        
        const json = await res.json()
        if (json.status === 'success') {
            showToast(json.message || 'Saved successfully', 'success')
            showModal.value = false
            fetchGetColumnAudioRecord(false)
        } else {
            showToast(json.message || 'Failed to save', 'error')
        }
    } catch (e) {
        console.error('Error saving column', e)
        showToast('An error occurred', 'error')
    }
}
</script>

<style scoped>
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
    content: "Disable";
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
    content: "Enable";
    left: 12px;
    right: auto;
    color: white;
}

.custom-roles-list {
    max-height: calc(75vh - 50px);
}
</style>
