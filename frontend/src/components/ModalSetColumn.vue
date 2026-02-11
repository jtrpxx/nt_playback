<template>
    <div v-if="modelValue" class="modal-backdrop" @click.self="close" id="columnModal">
        <div class="modal-box" style="max-width: 500px;">
            <div class="modal-header">
                <div style="display: flex; align-items: center; gap: 4px">
                    <div class="blue-icon">
                        <i class="fa-solid fa-chart-column"></i>
                    </div>
                    <h3 class="modal-title ad">{{ mode === 'createColumn' ? 'Create Column' : 'Edit Column' }}</h3>
                </div>
                <button type="button" class="btn-close" @click="close"></button>
            </div>
            <div class="modal-body">
                <div class="form-group-modal">
                    <div class="input-group" v-has-value>
                        <input v-model="form.name" required type="text" class="input" maxlength="30">
                        <label class="title-label">Column Name</label>
                    </div>
                    <div class="input-group" v-has-value>
                        <input v-model="form.description" required type="text" class="input" maxlength="100">
                        <label class="title-label">Description</label>
                    </div>

                    <div class="column-config-area" >
                        <div class="section-title" style="font-weight: 600; margin-bottom: 10px; font-size: 12px; color: #64748b;">
                            Column Ordering (Drag to reorder)
                        </div>
                        <div class="drag-list">
                            <div v-for="(col, index) in form.columns" :key="col.key" 
                                class="drag-item" 
                                :class="{ 'dragging': draggedIndex === index }"
                                draggable="true"
                                @dragstart="onDragStart($event, index)"
                                @dragover.prevent
                                @dragenter.prevent
                                @drop="onDrop($event, index)">
                                <div class="drag-handle">
                                    <i class="fas fa-grip-vertical"></i>
                                </div>
                                <div class="col-checkbox">
                                    <input type="checkbox" v-model="col.visible" :id="'col-' + col.key">
                                </div>
                                <label :for="'col-' + col.key" class="col-label">{{ col.label }}</label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn-role btn-secondary" @click="close">
                    <i class="fas fa-times"></i>
                    Cancel
                </button>
                <button class="btn-role btn-primary" @click="onSave">
                    <i class="fas fa-save"></i>
                    Save Changes
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { showToast } from '../assets/js/function-all'

const props = defineProps({
    modelValue: { type: Boolean, default: false },
    mode: { type: String, default: 'createColumn' },
    columnData: { type: Object, default: null }
})

const emit = defineEmits(['update:modelValue', 'saved'])

const form = reactive({
    id: null,
    name: '',
    description: '',
    columns: []
})

const draggedIndex = ref(null)

// รายชื่อคอลัมน์ทั้งหมดที่มีให้เลือก
const allAvailableColumns = [
    { key: 'main_db', label: 'Database Server' },
    { key: 'start_datetime', label: 'Start Date & Time' },
    { key: 'end_datetime', label: 'End Date & Time' },
    { key: 'duration', label: 'Duration' },
    { key: 'file_name', label: 'File Name' },
    { key: 'call_direction', label: 'Call Direction' },
    { key: 'customer_number', label: 'Customer Number' },
    { key: 'extension', label: 'Extension' },
    { key: 'agent', label: 'Agent' },
    { key: 'full_name', label: 'Full Name' },
    { key: 'custom_field_1', label: 'Custom Field' }
]

watch(() => props.modelValue, (val) => {
    if (val) initForm()
})

function initForm() {
    if (props.mode === 'editColumn' && props.columnData) {
        form.id = props.columnData.id
        form.name = props.columnData.name || ''
        form.description = props.columnData.description || '' // Assuming description exists
        
        let savedCols = []
        try {
            let raw = props.columnData.raw_data
            if (typeof raw === 'string') {
                // แปลง format "{...}" เป็น "[...]" เพื่อให้ parse JSON ได้
                if (raw.startsWith('{') && raw.endsWith('}')) {
                     raw = raw.replace('{', '[').replace('}', ']')
                }
                savedCols = JSON.parse(raw)
            } else if (Array.isArray(raw)) {
                savedCols = raw
            }
        } catch (e) {
            console.error('Error parsing raw_data', e)
            savedCols = []
        }

        // จัดเรียงคอลัมน์ตามที่บันทึกไว้
        const merged = []
        const savedKeys = new Set()
        
        if (Array.isArray(savedCols)) {
            savedCols.forEach(key => {
                const found = allAvailableColumns.find(c => c.key === key)
                if (found) {
                    merged.push({ ...found, visible: true })
                    savedKeys.add(key)
                }
            })
        }

        // เพิ่มคอลัมน์ที่เหลือ (ที่ไม่ได้เลือก) ต่อท้าย
        allAvailableColumns.forEach(col => {
            if (!savedKeys.has(col.key)) {
                merged.push({ ...col, visible: false })
            }
        })
        
        form.columns = merged
    } else {
        form.id = null
        form.name = ''
        form.description = ''
        form.columns = allAvailableColumns.map(c => ({ ...c, visible: true }))
    }
}

function onDragStart(e, index) {
    draggedIndex.value = index
    e.dataTransfer.effectAllowed = 'move'
    e.dataTransfer.dropEffect = 'move'
}

function onDrop(e, index) {
    const fromIndex = draggedIndex.value
    const toIndex = index
    if (fromIndex === null || fromIndex === toIndex) return

    const item = form.columns[fromIndex]
    form.columns.splice(fromIndex, 1)
    form.columns.splice(toIndex, 0, item)
    draggedIndex.value = null
}

function close() {
    emit('update:modelValue', false)
}

function onSave() {
    if (!form.name.trim()) {
        showToast('Column Name is required', 'error')
        return
    }

    // ส่งเฉพาะคอลัมน์ที่ visible=true และเรียงตามลำดับ
    const selectedKeys = form.columns.filter(c => c.visible).map(c => c.key)
    
    // Format as Postgres array string {"key1","key2"}
    const rawDataStr = `{${selectedKeys.map(k => `"${k}"`).join(',')}}`

    emit('saved', {
        id: form.id,
        name: form.name,
        description: form.description,
        raw_data: rawDataStr,
        mode: props.mode
    })
}
</script>

<style scoped>
.drag-list {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
    max-height: 300px;
    overflow-y: auto;
}
.drag-item {
    display: flex;
    align-items: center;
    padding: 10px 15px;
    background: #fff;
    border-bottom: 1px solid #f1f5f9;
    transition: background 0.2s;
}
.drag-item:last-child {
    border-bottom: none;
}
.drag-item:hover {
    background: #f8fafc;
}
.drag-item.dragging {
    opacity: 0.5;
    background: #e2e8f0;
}
.drag-handle {
    cursor: grab;
    margin-right: 12px;
    color: #94a3b8;
}
.col-checkbox {
    margin-right: 10px;
    display: flex;
    align-items: center;
}
.col-label {
    font-size: 13px;
    color: #334155;
    cursor: pointer;
    flex: 1;
    user-select: none;
}
.drag-list::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

.drag-list::-webkit-scrollbar-track {
  background: transparent;
  margin-top: 6px;
  margin-bottom: 12px;
}

.drag-list::-webkit-scrollbar-thumb {
  background-color: #416fd6;
  border-radius: 4px;
}

.form-group-modal {
    margin-bottom: 0px !important;
}
</style>