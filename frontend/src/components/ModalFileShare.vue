<template>
    <div v-if="modelValue" class="modal-backdrop" @click.self="close" id="fileShareModal">
        <div v-if="files && files.length" class="modal-box" style="max-width: 640px;">
            <div class="modal-header">
                <div style="display: flex; align-items: center; gap: 8px">
                    <div class="blue-icon"><i class="fa-solid fa-share-nodes"></i></div>
                    <h3 class="modal-title ad">File Share</h3>
                </div>
                <button type="button" class="btn-close" @click="close"></button>
            </div>

            <div class="modal-body">
                <div class="mb-2">You have selected <strong>{{ files.length }}</strong> files to grant access:</div>

                <div class="card card-custom-role" style="border: 2px dashed #e2e8f0;">
                    <div class="custom-roles-list" style="padding: 10px; max-height: 226px; overflow:auto;">
                        <div v-for="(f, idx) in files" :key="f.file_id || f.file_name + '-' + idx" class="custom-role-item">
                            <div style="display:flex;align-items:center;gap:10px;">
                                <div class="blue-icon" style="font-size: 14px;width: 25px;height: 25px;"><i class="fa-solid fa-file-audio"></i></div>
                                <div class="group-card-main">
                                    <div class="group-card-header">
                                        <span class="group-card-title">{{ truncateFileName(f.file_name) }}</span>
                                    </div>
                                    <div class="group-card-desc">Customer number: {{ f.customer_number || f.customerNumber || '-' }} | Date: {{ formatDate(f.start_datetime) }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mt-3">
                    <label class="form-label">Target</label>

                    <div class="d-flex align-items-center" style="gap:12px; margin-top:6px;">
                        <div class="form-check">
                            <input class="form-check-input" type="radio" id="shareTypeUser" value="user" v-model="selectionType">
                            <label class="form-check-label" for="shareTypeUser">User</label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="radio" id="shareTypeTicket" value="ticket" v-model="selectionType">
                            <label class="form-check-label" for="shareTypeTicket">Ticket</label>
                        </div>
                    </div>

                    <div v-if="selectionType === 'user'" class="input-group" style="margin-top:8px;">
                        <CustomSelect class="select-checkbox" v-model="shareUser" :options="userOptions" :always-up="true" placeholder="User" name="shareUser" />
                    </div>

                    <div v-else class="input-group" v-has-value style="margin-top:8px;">
                        <input required type="text" name="emailTicket" autocomplete="off" class="input" v-model="emailTicket" maxlength="255">
                        <label class="title-label">Email</label>
                    </div>
                </div>

                <div class="d-flex gap-3 mt-3">
                    <div style="flex:1">
                        <label class="form-label">Start Date & Time</label>
                        <input type="datetime-local" class="form-control" v-model="start" />
                    </div>
                    <div style="flex:1">
                        <label class="form-label">Expiry Date & Time</label>
                        <input type="datetime-local" class="form-control" v-model="expiry" />
                    </div>
                </div>
            </div>

            <div class="modal-footer">
                <button class="btn-role btn-secondary" @click="close"><i class="fas fa-times"></i> Cancel</button>
                <button class="btn-role btn-primary" :disabled="files.length === 0" @click="onShare"><i class="fas fa-share"></i> Share</button>
            </div>
        </div>

        <div v-else class="modal-box" style="max-width: 520px;">
            <div class="modal-header">
                <h5 class="modal-title">No Files Selected</h5>
                <button type="button" class="btn-close" @click="close"></button>
            </div>
            <div class="modal-body" style="text-align: center; padding: 32px 24px;">
                <div style="font-size: 36px; color: #f6c23e;"><i class="fa-solid fa-triangle-exclamation"></i></div>
                <p style="margin-top: 12px; color: #6b7280;">Please select at least one audio file to share.</p>
            </div>
            <div class="modal-footer" style="justify-content: center;">
                <button class="btn-role btn-primary" @click="close">OK</button>
            </div>
        </div>
    </div>
</template>


<script setup>
import { defineProps, defineEmits, ref, onMounted } from 'vue'
import CustomSelect from './CustomSelect.vue'
import { API_GET_USER_ALL } from '../api/paths'
import '../assets/css/modal-favorite.css'

const props = defineProps({ modelValue: { type: Boolean, default: false }, files: { type: Array, default: () => [] } })
const emit = defineEmits(['update:modelValue', 'share'])

const selectionType = ref('user')
const shareUser = ref('')
const userOptions = ref([])
// fetch users to populate select
const fetchUsers = async () => {
    try {
        const params = new URLSearchParams()
        params.set('draw', 1)
        params.set('start', 0)
        params.set('length', 1000)
        const res = await fetch(`${API_GET_USER_ALL()}?${params.toString()}`, { credentials: 'include' })
        if (!res.ok) throw new Error('Failed to fetch users')
        const json = await res.json()
        const list = json.data || []
        const opts = []
        for (const p of list) {
            const u = p.user ? p.user : p
            const uname = u?.username || ''
            const fullname = `${u?.first_name || ''} ${u?.last_name || ''}`.trim()
            const label = fullname ? `${uname} (${fullname})` : uname
            opts.push({ label, value: uname })
        }
        userOptions.value = opts
    } catch (e) {
        console.error('ModalFileShare fetchUsers error', e)
    }
}
const emailTicket = ref('')
const start = ref('')
const expiry = ref('')

function close() { emit('update:modelValue', false) }

function onShare() {
    const targetValue = selectionType.value === 'user' ? shareUser.value : emailTicket.value
    emit('share', { files: props.files, targetType: selectionType.value, target: targetValue, start: start.value, expiry: expiry.value })
    close()
}

onMounted(() => {
    fetchUsers()
})

function formatDate(v) {
    if (!v) return ''
    const d = new Date(v)
    if (isNaN(d.getTime())) return v
    const pad = (n) => String(n).padStart(2, '0')
    return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

function truncateFileName(s){ if(!s) return ''; return s.length>100 ? s.slice(0,57)+'...' : s }
</script>
<style scoped>
.custom-role-item {
    padding: 8px 20px;
    margin-bottom: 0px;
}
.group-card-title,.form-label {
font-size: 10px;
}
.group-card-desc {
    font-size: 8px;
}
</style>