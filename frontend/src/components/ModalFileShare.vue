<template>
    <!-- Modal Share -->
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
                        <CustomSelect v-model="shareUser" :options="userOptions" :always-up="true" placeholder="User" name="shareUser" />
                    </div>

                    <div v-else class="input-group" v-has-value style="margin-top:8px;">
                        <input required type="text" name="emailTicket" autocomplete="off" class="input" v-model="emailTicket" maxlength="255">
                        <label class="title-label">Email</label>
                    </div>
                </div>

                <div class="d-flex gap-3 mt-3">
                   <input ref="fromInput" v-flatrangepickr="{ target: exp, key: 'ticketPeriod' }"  required type="text" name="ticketPeriod" autocomplete="off" :class="['input', { 'form-input-modal': errors.ticketPeriod }]">
<label class="title-label">Ticket Period*</label>
<span class="calendar-icon"><i class="fa-regular fa-calendar"></i></span>
<div v-show="errors.ticketPeriod" class="validate"><i class="fa-solid fa-circle-exclamation"></i> This field is required.</div>
                </div>
            </div>

            <div class="modal-footer">
                <button class="btn-role btn-secondary" @click="close"><i class="fas fa-times"></i> Cancel</button>
                <button class="btn-role btn-primary" :disabled="files.length === 0" @click="onCreate"><i class="fa-solid fa-plus"></i> Create</button>
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

    <!-- Modal Share complete -->

    <div v-if="showResult" class="modal-backdrop" @click.self="closeResult" id="fileShareResult">
        <div class="modal-box" style="max-width: 400px;">
            <div class="modal-header">
                <div style="display: flex; align-items: center; gap: 8px">
                    <div class="green-icon"><i class="fa-solid fa-share-nodes"></i></div>
                    <h3 class="modal-title ad" v-if="resultType === 'ticket'">Ticket Created Successfully</h3>
                    <h3 class="modal-title ad" v-else>File shared successfully!</h3>
                </div>
                <button type="button" class="btn-close" @click="closeResult"></button>
            </div>

            <div class="modal-body">
                <div v-if="resultType === 'ticket'">
                    <div style="text-align:center; margin-bottom:12px;">
                        <i class="fa-regular fa-check-circle" style="color:#10b981;margin-bottom: 15px;font-size: 45px;"></i>
                        <p style="margin:0">Ticket <strong style="color:#2563eb">{{ resultData.ticketCode }}</strong> created successfully!</p>
                    </div>

                    <div class="card" style="padding:16px; border:1px solid #e6eef8;">
                        <p style="margin:0 0 8px 0">Dear <strong style="color:#2563eb">{{ resultData.recipient }}</strong>,</p>
                        <p style="margin:0 0 12px 0">An access ticket has been created for you to listen to specific audio records on NT Audio Search.</p>
                        <div style="border:1px dashed #e6eef8; padding:12px; margin-bottom:12px;">
                            <div class="detail-file-share"><strong class="strong-title">Ticket Code:</strong> <span style="color:#2563eb">{{ resultData.ticketCode }}</span></div>
                            <div class="detail-file-share"><strong class="strong-title">Password:</strong> <code style="background:#f3f4f6; padding:4px 8px; border-radius:4px">{{ resultData.password }}</code></div>
                            <div class="detail-file-share"><strong class="strong-title">Valid Start:</strong> {{ resultData.validStart }}</div>
                            <div class="detail-file-share"><strong class="strong-title">Valid Expire:</strong> {{ resultData.validExpiry }}</div>
                        </div>
                        <p style="margin:0 0 8px 0">Please visit our portal to login using the credentials above.</p>
                        <div style="margin-bottom:12px;"><a href="/login">https://192.168.1.95/login</a></div>
                        <div>
                            Best regards,<br>
                            <b>NT Audio Search Team</b>
                        </div>
                    </div>
                </div>

                <div v-else>
                    <div style="text-align:center; margin-bottom:12px;">
                        <i class="fa-regular fa-check-circle" style="color:#10b981;margin-bottom: 15px;font-size: 45px;"></i>
                        <p style="margin:0">User <strong style="color:#2563eb">{{ resultData.recipient }}</strong> created successfully!</p>
                    </div>
                    <div class="card" style="padding:16px; border:1px solid #e6eef8;">
                        <p>Dear {{ resultData.recipient }},</p>
                        <p>Files are shared so you can listen to specific audio records on <br> NT Audio Search.</p>
                        <div style="border:1px dashed #e6eef8; padding:12px; margin-bottom:12px;">
                            <div><strong>Valid Start:</strong> {{ resultData.validStart }}</div>
                            <div><strong>Valid Expire:</strong> {{ resultData.validExpiry }}</div>
                        </div>
                        <p>You can find it in the ticket menu.</p>
                        <div style="margin-bottom:12px;"><a href="/login">https://192.168.1.95/ticket</a></div>
                        <div>
                            Best regards,<br>
                            <b>NT Audio Search Team</b>
                        </div>
                    </div>
                </div>
            </div>

            <div class="modal-footer btn-file-share" style="justify-content: space-between;">
                <button class="btn-role btn-secondary" @click="() => { navigator.clipboard && navigator.clipboard.writeText(JSON.stringify(resultData)); }"><i class="fa-regular fa-envelope" style="font-size: 12px;"></i>Send email</button>
                <button class="btn-role btn-primary" @click="closeResult">OK</button>
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

const showResult = ref(false)
const resultType = ref('')
const resultData = ref({})

function genTicketCode() {
    const n = Math.floor(Math.random() * 900000) + 100000
    return `TKT-${n}`
}

function genPassword() {
    const chars = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'
    let out = ''
    for (let i = 0; i < 6; i++) out += chars[Math.floor(Math.random() * chars.length)]
    return out
}

function close() { emit('update:modelValue', false) }

function onCreate() {
    const targetValue = selectionType.value === 'user' ? shareUser.value : emailTicket.value
    // emit for parent/backend
    emit('share', { files: props.files, targetType: selectionType.value, target: targetValue, start: start.value, expiry: expiry.value })

    // prepare result modal
    const validStart = start.value || new Date().toISOString().slice(0,16)
    const validExpiry = expiry.value || new Date(Date.now()).toISOString().slice(0,16)

    if (selectionType.value === 'ticket') {
        resultType.value = 'ticket'
        resultData.value = {
            recipient: emailTicket.value,
            ticketCode: genTicketCode(),
            password: genPassword(),
            validStart: formatDate(validStart),
            validExpiry: formatDate(validExpiry)
        }
    } else {
        resultType.value = 'user'
        resultData.value = {
            recipient: shareUser.value,
            validStart: formatDate(validStart),
            validExpiry: formatDate(validExpiry)
        }
    }

    // close share input modal and open result
    emit('update:modelValue', false)
    showResult.value = true
}

function closeResult() {
    showResult.value = false
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
.detail-file-share {
    margin-bottom: 4px;
}

strong {
    font-weight: 500;
}

.strong-title{
    margin-right: 4px;
    font-weight: 500;
}
</style>

<style scoped>
/* Make modal footer buttons sit on the same row and fill available width */
.btn-file-share {
    display: flex !important;
    flex-direction: row !important;
    gap: 8px;
    padding: 12px 16px;
}
.btn-role {
    border-radius: 25px;
}
.btn-file-share .btn-role {
    flex: 1 1 0;
    min-width: 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}
</style>