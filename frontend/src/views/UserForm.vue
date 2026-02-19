<template>
    <MainLayout>
        <div class="main-wrapper container-fluid-home py-3">
            <Breadcrumbs :items="[{ text: 'Home', to: '/' }, { text: 'User Management', to: '/user-management' }, { text: mode === 'edit' ? 'Save User' : 'Add User' }]" />

            <div class="row col-lg-12">
                <div class="col-lg-6" style="margin-bottom: 14px;">
                    <div class="card card-left">
                        <div class="card">
                            <div class="card-body">
                                <div class="d-flex align-items-start justify-content-between"
                                    style="margin-bottom: 18px;">
                                    <div class="d-flex align-items-center">
                                        <div class="d-flex align-items-center justify-content-center me-1"
                                            style="width:35px;height:35px;background-color: #D9E2F6;border-radius: 10px !important;">
                                            <i class="fas fa-user-plus" style="color:#2b6cb0;font-size:18px"></i>
                                        </div>
                                        <h5 class="card-title mb-2 mt-1">User Information</h5>
                                    </div>
                                    <div class="d-flex align-items-center">
                                        <div>
                                            <button class="customize-btn" type="button" id="clearUserInfoBtn"
                                                @click="clearUserInfo" style=" position:relative;">
                                                <i class="fas fa-eraser" style="margin-right: 6px;"></i> Clear
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                <div class="permissions-grid-1">
                                    <div class="input-group" style="margin-bottom: 12.2px;" v-has-value>
                                        <input v-model="form.username" required type="text" name="username" autocomplete="off" :class="['input', { 'form-input-modal': usernameCheck || errors.username }]" maxlength="30" >
                                        <label class="title-label">Username*</label>
                                        <div v-show="usernameCheck" class="validate"><i class="fa-solid fa-circle-exclamation"></i> This username is already in the system.</div>
                                        <div v-show="errors.username && !usernameCheck" class="validate"><i class="fa-solid fa-circle-exclamation"></i> {{ typeof errors.username === 'string' ? errors.username : 'This field is required.' }}</div>
                                    </div>
                                </div>

                                <div class="permissions-grid-2">
                                    <div class="input-group" v-has-value v-if="mode !== 'edit'">
                                        <input v-model="form.password" required :type="passwordVisible ? 'text' : 'password'" name="password" autocomplete="off" :class="['input', { 'form-input-modal': errors.password }]" maxlength="30">
                                        <button type="button" class="toggle-visibility" @click="passwordVisible = !passwordVisible" aria-label="Toggle password visibility">
                                            <i :class="passwordVisible ? 'fa-regular fa-eye-slash' : 'fa-regular fa-eye'"></i>
                                        </button>
                                        <label class="title-label">Password*</label>
                                        <div v-show="errors.password" class="validate"><i class="fa-solid fa-circle-exclamation"></i> {{ typeof errors.password === 'string' ? errors.password : 'This field is required.' }}</div>
                                    </div>
                                    <div class="input-group" v-has-value v-if="mode !== 'edit'">
                                        <input v-model="form.confirmPassword" required :type="confirmPasswordVisible ? 'text' : 'password'" name="confirmPassword" autocomplete="off" :class="['input', { 'form-input-modal': errors.confirmPassword }]" maxlength="30">
                                        <button type="button" class="toggle-visibility" @click="confirmPasswordVisible = !confirmPasswordVisible" aria-label="Toggle confirm password visibility">
                                            <i :class="confirmPasswordVisible ? 'fa-regular fa-eye-slash' : 'fa-regular fa-eye'"></i>
                                        </button>
                                        <label class="title-label">Confirm Password*</label>
                                        <div v-show="errors.confirmPassword" class="validate"><i class="fa-solid fa-circle-exclamation"></i> {{ typeof errors.confirmPassword === 'string' ? errors.confirmPassword : 'This field is required.' }}</div>
                                    </div>
                                    <div class="input-group" v-has-value>
                                        <input v-model="form.firstName" required type="text" name="firstName" autocomplete="off" :class="['input', { 'form-input-modal': errors.firstName }]" maxlength="30">
                                        <label class="title-label">First Name*</label>
                                        <div v-show="errors.firstName" class="validate"><i class="fa-solid fa-circle-exclamation"></i> {{ typeof errors.firstName === 'string' ? errors.firstName : 'This field is required.' }}</div>
                                    </div>
                                    <div class="input-group" v-has-value>
                                        <input v-model="form.lastName" required type="text" name="lastName" autocomplete="off" :class="['input', { 'form-input-modal': errors.lastName }]" maxlength="30">
                                        <label class="title-label">Last Name*</label>
                                        <div v-show="errors.lastName" class="validate"><i class="fa-solid fa-circle-exclamation"></i> {{ typeof errors.lastName === 'string' ? errors.lastName : 'This field is required.' }}</div>
                                    </div>
                                    <div class="input-group" v-has-value>
                                        <input v-model="form.email" required type="text" name="email" autocomplete="off" class="input" maxlength="30">
                                        <label class="title-label">Email</label>
                                        <div v-show="errors.email" class="validate"><i class="fa-solid fa-circle-exclamation"></i> {{ typeof errors.email === 'string' ? errors.email : 'Please enter a valid email address.' }}</div>
                                    </div>
                                    <div class="input-group" v-has-value>
                                        <input v-model="form.phone" required type="text" name="phone" autocomplete="off" class="input" maxlength="10">
                                        <label class="title-label">Phone</label>
                                    </div>
                                    <div class="input-group">
                                        <CustomSelect :class="['select-search', { 'select-toggle-error': errors.group }]" v-model="selectedGroupId" :options="groupOptions" :always-up="false" placeholder="Select Group*" name="groupModal" />
                                        <div v-show="errors.group" class="validate"><i class="fa-solid fa-circle-exclamation"></i> This dropdown is required.</div>
                                    </div>
                                    <div class="input-group" :class="{ 'select-disabled': !selectedGroupId }">
                                        <CustomSelect :class="['select-search', { 'select-toggle-error': errors.team }]" v-model="selectedTeamId" :always-up="false" :options="teamOptions" placeholder="Select Team*" name="teamModal" />
                                        <div v-show="errors.team" class="validate"><i class="fa-solid fa-circle-exclamation"></i> This dropdown is required.</div>
                                    </div>
                                    <div class="input-group">
                                        <CustomSelect class="select-search select-checkbox" v-model="selectedFileId" :options="fileOptions"  placeholder="Select File Audio*" name="fileModal" @search="onFileSearch" />
                                        <div v-show="errors.file" class="validate"><i class="fa-solid fa-circle-exclamation"></i> This dropdown is required.</div>
                                    </div>
                                    <div class="input-group" v-has-value>
                                        <input ref="fromInput" v-flatrangepickr="{ target: exp, key: 'expires' }"  required type="text" name="expires" autocomplete="off" class="input">
                                        <label class="title-label">Ticket Period</label>
                                        <span class="calendar-icon"><i class="fa-regular fa-calendar"></i></span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
                <div class="col-lg-6" style="margin-bottom: 14px;">
                    <!-- Select Role Card -->
                    <div class="card card-right">
                        <div class="card">
                            <div class="card-body">
                                <div class="d-flex align-items-start justify-content-between"
                                    style="margin-bottom: 18px;">
                                    <div class="d-flex align-items-center">
                                        <div class="d-flex align-items-center justify-content-center me-1"
                                            style="width:35px;height:35px;background-color: #D9E2F6;border-radius: 10px !important;">
                                            <i class="fas fa-shield-alt" style="color:#2b6cb0;font-size:18px"></i>
                                        </div>
                                        <h5 class="card-title mb-2 mt-1">Select Role</h5>
                                    </div>
                                </div>

                                <div v-show="errors.role" class="validate"><i class="fa-solid fa-circle-exclamation"></i> This Select Role is required.</div>
                                <div class="role-cards-4" id="roleCards" :class="{ disabled: roleCardsDisabled }">
                                    <label class="role-card" :class="[ { selected: selectedBaseRoleKey==='administrator' }, { 'role-card-error': errors.role } ]" @click.prevent="selectBaseRole('administrator')">
                                        <input type="checkbox" name="role" value="administrator" :checked="selectedBaseRoleKey==='administrator'">
                                        <div class="role-icon"><i class="fas fa-crown"></i></div>
                                        <div class="role-name">Administrator</div>
                                        <div class="role-desc">Full system access</div>
                                    </label>
                                    <label class="role-card" :class="[ { selected: selectedBaseRoleKey==='auditor' }, { 'role-card-error': errors.role } ]" @click.prevent="selectBaseRole('auditor')">
                                        <input type="checkbox" name="role" value="auditor" :checked="selectedBaseRoleKey==='auditor'">
                                        <div class="role-icon"><i class="fas fa-clipboard-check"></i></div>
                                        <div class="role-name">Auditor</div>
                                        <div class="role-desc">Read & audit access</div>
                                    </label>
                                    <label class="role-card" :class="[ { selected: selectedBaseRoleKey==='operator' }, { 'role-card-error': errors.role } ]" @click.prevent="selectBaseRole('operator')">
                                        <input type="checkbox" name="role" value="operator" :checked="selectedBaseRoleKey==='operator'">
                                        <div class="role-icon"><i class="fas fa-headset"></i></div>
                                        <div class="role-name">Operator</div>
                                        <div class="role-desc">Standard operations</div>
                                    </label>
                                    <label class="role-card" :class="[ { selected: selectedBaseRoleKey==='ticket' }, { 'role-card-error': errors.role } ]" @click.prevent="selectBaseRole('ticket')">
                                        <input type="checkbox" name="role" value="ticket" :checked="selectedBaseRoleKey==='ticket'">
                                        <div class="role-icon"><i class="fas fa-ticket"></i></div>
                                        <div class="role-name">Ticket</div>
                                        <div class="role-desc">Temporary user</div>
                                    </label>
                                </div>

                                <div class="custom-role-row" style="display: flex; gap: 12px; align-items: stretch;">
                                    <div class="custom-dropdown" id="otherRoleDropdown" :class="{ open: otherRoleOpen, selected: selectedCustomRoleId }" style="flex: 1;">
                                        <div class="dropdown-selected" @click="toggleOtherRoleDropdown">
                                            <span class="dropdown-text">
                                                <i v-if="selectedCustomRoleId" class="fas fa-user" style="margin-right: 8px;"></i>
                                                {{ selectedCustomRoleName || 'Select Custom Role' }}
                                            </span>
                                            <i class="fas fa-chevron-down dropdown-arrow"></i>
                                        </div>
                                        <div class="dropdown-options">
                                            <div v-if="customRoles.length === 0" class="dropdown-option disabled" style="color: #94a3b8; cursor: default; pointer-events: none;">
                                                <i class="fas fa-info-circle"></i>
                                                <span>No custom roles available</span>
                                            </div>
                                            <div v-else>
                                                <div v-for="role in customRoles" :key="role.id" class="dropdown-option" :class="{ selected: selectedCustomRoleId === role.id }" @click="selectCustomRole(role)">
                                                    <i class="fas fa-user"></i>
                                                    <span>{{ role.name }}</span>
                                                </div>
                                            </div>
                                        </div>
                                        <input type="hidden" name="otherRole" id="otherRoleInput" :value="selectedCustomRoleId || ''">
                                    </div>
                                    <button class="customize-btn" type="button" @click="clearCustomRole"
                                        style="display: flex; align-items: center; justify-content: center; margin: 0;">
                                        <i class="fas fa-eraser" style="margin-right: 6px;"></i> Clear
                                    </button>
                                </div>


                            </div>
                        </div>
                        <div class="card">
                            <div class="card-body">
                                <div class="d-flex align-items-start justify-content-between"
                                    style="margin-bottom: 18px;">
                                    <div class="d-flex align-items-center">
                                        <div class="d-flex align-items-center justify-content-center me-1"
                                            style="width:35px;height:35px;background-color: #D9E2F6;border-radius: 10px !important;">
                                            <i class="fas fa-database" style="color:#2b6cb0;font-size:18px"></i>
                                        </div>
                                        <h5 class="card-title mb-2 mt-1">Select Database Server</h5>
                                    </div>
                                    <div class="d-flex align-items-center">
                                        <button type="button" class="btn-role btn-secondary" @click="resetDatabase" :disabled="databaseDisabled"
                                            style="margin-right: 6px">
                                            <i class="fas fa-undo"></i>
                                            Reset to Default
                                        </button>
                                        <button class="customize-btn" type="button" @click="clearDatabaseScope" :disabled="databaseDisabled">
                                            <i class="fas fa-eraser" style="margin-right: 6px;"></i> Clear
                                        </button>
                                    </div>
                                </div>

                                <div class="database-grid">
                                    <label class="db-card">
                                        <input type="checkbox" value="all" :checked="selectedAllDatabases" @change="toggleAllDatabases" :disabled="databaseDisabled">
                                        <span class="db-checkbox"></span>
                                        <span class="db-name">All Databases</span>
                                    </label>
                                    <label class="db-card" v-for="db in databases" :key="db.id">
                                        <input type="checkbox" :value="db.id" :checked="selectedDatabaseIds.includes(String(db.id))" @change="() => toggleDatabase(db)" :disabled="databaseDisabled">
                                        <span class="db-checkbox"></span>
                                        <span class="db-name">{{ db.database_name }}</span>
                                    </label>
                                </div>

                            </div>
                        </div>
                    </div>

                </div>
               
                <div class="col-lg-12">
                    <div class="card">
                        <div class="card-body">
                            <div class="d-flex align-items-start justify-content-between" style="margin-bottom: 6px;">
                                <div class="d-flex align-items-center">
                                    <div class="d-flex align-items-center justify-content-center me-1"
                                        style="width:35px;height:35px;background-color: #D9E2F6;border-radius: 10px !important;">
                                        <i class="fas fa-key" style="color:#2b6cb0;font-size:18px"></i>
                                    </div>
                                    <h5 class="card-title mb-2 mt-1">Permissions</h5>
                                </div>
                            </div>

                            <div class="permissions-grid" id="permissionsGrid">
                                <template v-for="type in orderedTypes" :key="type">
                                    <div v-if="groupedPermissions[type] && groupedPermissions[type].length"
                                        class="permission-group-header">{{ typeLabels[type] }}</div>

                                    <label v-for="perm in groupedPermissions[type]" :key="perm.action"
                                        :class="['permission-item']">
                                        <input type="checkbox" disabled :data-permission="perm.action" :checked="!!selectedPermissions[perm.action]" @change="() => togglePermission(perm)">
                                        <span class="perm-checkbox"></span>
                                        <span class="perm-label">{{ perm.name }}</span>
                                    </label>
                                </template>
                            </div>

                            <div class="button-group">
                                <button class="btn btn-primary" type="button" @click="submit">
                                    <i class="fas fa-check"></i>
                                    {{ mode === 'edit' ? 'Save User' : 'Add User' }}
                                </button>
                                <button class="btn btn-secondary" @click="cancel">
                                    <i class="fas fa-times"></i>
                                    Cancel
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </MainLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'
import CustomSelect from '../components/CustomSelect.vue'
import { registerRequest } from '../utils/pageLoad'
import { getCookie, showToast } from '../assets/js/function-all'
import { API_GROUP_INDEX, API_GET_DATABASE, API_GET_ALL_ROLES_PERMISSIONS, API_CHECK_USERNAME, API_CREATE_USER, API_UPDATE_USER, API_GET_FILE_AUDIO } from '../api/paths'
import { ensureCsrf, getCsrfToken } from '../api/csrf'

const loading = ref(false)
const selectedGroupId = ref(null)
const usernameCheck = ref(false)
// CSRF handled by centralized helper

const route = useRoute()
const router = useRouter()

const props = defineProps({
    mode: { type: String, default: null },
    initialData: { type: Object, default: null }
})

const mode = computed(() => {
    if (props.mode) return props.mode
    try {
        if (!route) return 'add'
        const q = route.query && route.query.mode
        if (q === 'edit') return 'edit'
        const p = (route.path || route.fullPath || '').toString().toLowerCase()
        if (p.includes('/edit')) return 'edit'
        const paramMode = route.params && route.params.mode
        if (paramMode === 'edit') return 'edit'
        return 'add'
    } catch (e) {
        return 'add'
    }
})

// form reactive state used by v-model bindings
const form = ref({
    username: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    email: '',
    phone: ''
})

const exp = ref({
    expires: '',
})

// debounce timer for username check
let _usernameTimer = null

const getInitialUserId = () => {
    try {
        const d = props.initialData || null
        if (!d) return null
        const up = d.user_profile || d.userProfile || null
        const u = (up && (up.user || up.user_to_edit || up.user)) || (d.user_to_edit && d.user_to_edit) || d.user || null
        if (u && (u.id || u.user_id)) return u.id || u.user_id
        if (d.id) return d.id
        return null
    } catch (e) {
        return null
    }
}

// validation error state for form fields (string message or false)
const errors = reactive({
    username: false,
    password: false,
    confirmPassword: false,
    firstName: false,
    lastName: false,
    email: false,
    group: false,
    team: false,
    role: false
})

// watch username and debounce check against backend
watch(() => form.value.username, (val) => {
    usernameCheck.value = false
    errors.username = false
    if (_usernameTimer) clearTimeout(_usernameTimer)
    _usernameTimer = setTimeout(async () => {
        try {
            if (!val || String(val).trim() === '') { usernameCheck.value = false; return }
            // allow only English letters and numbers
            const uname = String(val).trim()
            const unameOk = /^[A-Za-z0-9]+$/.test(uname)
            if (!unameOk) {
                errors.username = 'Username must contain only English letters and numbers'
                usernameCheck.value = false
                return
            }
            const userId = getInitialUserId()
            const url = API_CHECK_USERNAME() + `?username=${encodeURIComponent(uname)}` + (userId ? `&user_id=${encodeURIComponent(String(userId))}` : '')
            const res = await fetch(url, { method: 'GET', credentials: 'include' })
            if (!res.ok) { usernameCheck.value = false; return }
            const j = await res.json()
            usernameCheck.value = !!(j && j.is_taken === true)
        } catch (e) {
            console.error('username check error', e)
            usernameCheck.value = false
        }
    }, 400)
})

const groups = ref([])
const teams = ref([])
const groupTeamsMap = ref({})
const databases = ref([])

// password visibility
const passwordVisible = ref(false)
const confirmPasswordVisible = ref(false)

// permissions state
const allPermissions = ref([])
const groupedPermissions = ref({})
const orderedTypes = [
    'access',
    'audio recording',
    'user management',
    'logs'
]
const typeLabels = {
    'access': 'ACCESS',
    'audio recording': 'AUDIO RECORDING',
    'user management': 'USER MANAGEMENT',
    'logs': 'LOGS'
}

for (const t of orderedTypes) groupedPermissions.value[t] = []

const customRoles = ref([])
const selectedCustomRoleId = ref(null)
const otherRoleOpen = ref(false)
const selectedCustomRoleName = computed(() => {
    const r = customRoles.value.find(x => String(x.id) === String(selectedCustomRoleId.value))
    return r ? r.name : null
})

function toggleOtherRoleDropdown() {
    otherRoleOpen.value = !otherRoleOpen.value
}

function selectCustomRole(role) {
    if (!role) return
    selectedCustomRoleId.value = role.id
    otherRoleOpen.value = false

    // clear any selected base role
    selectedBaseRoleKey.value = null
    // clear role error when user selects a role
    errors.role = false

    setSelectedPermissionsFromCustomRole(role.id)
}

function clearCustomRole() {
    selectedCustomRoleId.value = null
    otherRoleOpen.value = false
    clearSelectedPermissions()
}

// populate form when `initialData` prop is provided (Edit mode)
function populateFromInitial(data) {
    if (!data) return
    const up = data.user_profile || data.userProfile || null
    // user fields
    const u = up && (up.user || up.user_to_edit || up.user) || (data.user_to_edit && data.user_to_edit) || null
    if (u) {
        if (form && form.value) {
            form.value.username = u.username || u.user_name || ''
            form.value.firstName = u.first_name || u.firstName || ''
            form.value.lastName = u.last_name || u.lastName || ''
            form.value.email = u.email || ''
        }
    }

    // profile-level phone
    if (up && up.phone) {
        if (form && form.value) form.value.phone = up.phone
    } else if (data.phone) {
        if (form && form.value) form.value.phone = data.phone
    }

    // team/group
    const team = up && up.team ? up.team : (data.team || null)
    if (team) {
        // group id may be nested under user_group
        const gid = (team.user_group && team.user_group.id) || team.user_group_id || (team.user_group && team.user_group.user_group_id) || null
        if (gid) selectedGroupId.value = String(gid)
        if (team.id) selectedTeamId.value = String(team.id)
    }

    // selected databases - accept several field name variants
    let selD = data.selected_db_id || data.selected_db_ids || data.selected_db_ids_json || data.selected_db_ids_json || data.selected_db_ids || data.selected_db_id
    if (!selD && data.selected_db_id === undefined && data.selected_db_ids === undefined) {
        // also check older keys
        selD = data.selectedDatabaseIds || data.selected_database_ids
    }
    if (typeof selD === 'string') {
        try { selD = JSON.parse(selD) } catch (e) { selD = selD.replace(/[[\]"]+/g, '').split(',').map(s=>s.trim()).filter(Boolean) }
    }
    if (Array.isArray(selD)) {
        selectedDatabaseIds.value = selD.map(x => String(x))
        defaultDatabaseIds.value = [...selectedDatabaseIds.value]
        selectedAllDatabases.value = databases.value.length > 0 && selectedDatabaseIds.value.length === databases.value.length
    }

    // honor explicit all_db_selected flag from API
    const allSelectedFlag = data.all_db_selected || data.all_db_selected === true || data.all_db_selected === 'true'
    if (allSelectedFlag) {
        selectedAllDatabases.value = true
        // if databases already loaded, set selectedDatabaseIds now
        if (databases.value && databases.value.length > 0) {
            selectedDatabaseIds.value = databases.value.map(d => String(d.id))
            defaultDatabaseIds.value = [...selectedDatabaseIds.value]
            selectedAllDatabases.value = databases.value.length > 0 && selectedDatabaseIds.value.length === databases.value.length
        }
    }

    // role
    const selRoleType = data.selected_role_type || data.selected_role_type_json || data.selectedRoleType || null
    const selRoleId = data.selected_role_id || data.selected_role_id_json || data.selectedRoleId || null
    if (selRoleType && ['administrator','auditor','operator','ticket'].includes(selRoleType)) {
        selectedBaseRoleKey.value = selRoleType
        selectedCustomRoleId.value = null
    } else if (selRoleId) {
        selectedCustomRoleId.value = String(selRoleId)
        selectedBaseRoleKey.value = null
    }

}


// (watch moved below declarations that populateFromInitial depends on)
function clearUserInfo() {
    clearSelectedPermissions()
    selectedBaseRoleKey.value = null
    selectedCustomRoleId.value = null
    otherRoleOpen.value = false

    // reset visibility toggles
    passwordVisible.value = false
    confirmPasswordVisible.value = false

    try {
        const userCard = document.querySelector('.card-left')
        if (userCard) {
            userCard.querySelectorAll('input').forEach(inp => {
                if (inp.type === 'checkbox' || inp.type === 'radio') inp.checked = false
                else inp.value = ''
            })
            userCard.querySelectorAll('.input-group.has-value').forEach(el => el.classList.remove('has-value'))
        }
    } catch (e) {
        console.warn('clearUserInfo: failed to clear inputs', e)
    }

    // clear the reactive form values so v-model bindings are reset
    if (form && form.value) {
        form.value.username = ''
        form.value.password = ''
        form.value.confirmPassword = ''
        form.value.firstName = ''
        form.value.lastName = ''
        form.value.email = ''
        form.value.phone = ''
    }

    selectedGroupId.value = null
    selectedTeamId.value = null
}

function clearDatabaseScope() {
    // Clear the user's explicit selection but keep the "default" databases
    // provided by the selected team so that "Reset to Default" can restore them.
    selectedDatabaseIds.value = []
    selectedAllDatabases.value = false
}

async function submit() {
    // client-side validation for required fields (fields marked with *)
    // clear previous errors
    errors.username = false
    errors.password = false
    errors.confirmPassword = false
    errors.firstName = false
    errors.lastName = false
    errors.email = false
    errors.phone = false
    errors.group = false
    errors.team = false

    let hasError = false
    if (!form.value.username || String(form.value.username).trim() === '') { errors.username = 'This field is required.'; hasError = true }
    else {
        // username pattern
        const uname = String(form.value.username).trim()
        if (!/^[A-Za-z0-9]+$/.test(uname)) { errors.username = 'Username must contain only English letters and numbers'; hasError = true }
    }
    if (mode && mode.value !== 'edit') {
        if (!form.value.password || String(form.value.password).trim() === '') { errors.password = 'This field is required.'; hasError = true }
        else if (String(form.value.password).length < 8) { errors.password = 'Password must be at least 8 characters long'; hasError = true }
        if (!form.value.confirmPassword || String(form.value.confirmPassword).trim() === '') { errors.confirmPassword = 'This field is required.'; hasError = true }
        if (form.value.password && form.value.confirmPassword && form.value.password !== form.value.confirmPassword) { errors.confirmPassword = 'Passwords do not match'; hasError = true }
    }
    if (!form.value.firstName || String(form.value.firstName).trim() === '') { errors.firstName = 'This field is required.'; hasError = true }
    else if (!/^[\p{L}\s]+$/u.test(String(form.value.firstName).trim())) { errors.firstName = 'Special characters are not allowed in first name'; hasError = true }
    if (!form.value.lastName || String(form.value.lastName).trim() === '') { errors.lastName = 'This field is required.'; hasError = true }
    else if (!/^[\p{L}\s]+$/u.test(String(form.value.lastName).trim())) { errors.lastName = 'Special characters are not allowed in last name'; hasError = true }
    if (!selectedGroupId.value) { errors.group = true; hasError = true }
    if (!selectedTeamId.value) { errors.team = true; hasError = true }
    // email validate if provided
    if (form.value.email && String(form.value.email).trim() !== '') {
        const e = String(form.value.email).trim()
        const eok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e)
        if (!eok) { errors.email = 'Please enter a valid email address'; hasError = true }
    }
    // phone validate if provided: digits only
    if (form.value.phone && String(form.value.phone).trim() !== '') {
        const p = String(form.value.phone).trim()
        if (!/^[0-9]+$/.test(p)) { errors.phone = 'Phone must contain only numbers'; hasError = true }
    }
    // role required (either base role or custom role must be selected)
    if (!selectedBaseRoleKey.value && !selectedCustomRoleId.value) { errors.role = true; hasError = true }

    if (hasError) {
        // stop submission so user can correct fields
        // wait for DOM to update so v-show messages are visible, then scroll to first visible validation message
        try {
            await nextTick()
            const validates = Array.from(document.querySelectorAll('.validate'))
                .filter(el => el.offsetParent !== null)
            if (validates.length) {
                const first = validates[0]
                const group = first.closest('.input-group') || first
                try { group.scrollIntoView({ behavior: 'smooth', block: 'center' }) } catch (e) { first.scrollIntoView() }
            }
        } catch (e) {
            console.error('scroll to validation error failed', e)
        }
        return
    }

    // Build FormData for POST
    const fd = new FormData()
    fd.append('username', form.value.username || '')
    if (form.value.password) fd.append('password', form.value.password)
    fd.append('first_name', form.value.firstName || '')
    fd.append('last_name', form.value.lastName || '')
    if (form.value.email) fd.append('email', form.value.email)
    if (form.value.phone) fd.append('phone', form.value.phone)

    // role: prefer custom role id, otherwise base role key (type)
    if (selectedCustomRoleId.value) fd.append('role', selectedCustomRoleId.value)
    else if (selectedBaseRoleKey.value) fd.append('role', selectedBaseRoleKey.value)

    if (selectedTeamId.value) fd.append('team', selectedTeamId.value)
    if (selectedGroupId.value) fd.append('group', selectedGroupId.value)

    // databases: send either db_id-all=all or db_id-{id} flags
    if (selectedAllDatabases.value) {
        fd.append('db_id-all', 'all')
    } else {
        for (const db of databases.value || []) {
            const key = `db_id-${db.id}`
            if (selectedDatabaseIds.value.includes(String(db.id))) fd.append(key, 'on')
        }
    }

    // include permissions as JSON string (optional)
    try {
        const perms = Object.keys(selectedPermissions.value).filter(k => selectedPermissions.value[k])
        fd.append('permissions', JSON.stringify(perms))
    } catch (e) {}

    // Determine endpoint based on mode
    let url = API_CREATE_USER()
    let method = 'POST'
    const initialUserId = getInitialUserId()
    if (mode && mode.value === 'edit') {
        // prefer to call update endpoint with id in URL if available
        const id = initialUserId || route.params.id || route.query.user_id
        if (id) {
            url = API_UPDATE_USER(id)
        } else {
            // fallback: include user_id in payload and call create endpoint (backend supports update when user_id present)
            fd.append('user_id', initialUserId || '')
            url = API_CREATE_USER()
        }
    }

    try {
    loading.value = true
    // CSRF token cached at login/startup; use cached token
    const csrfToken = getCsrfToken()
        const res = await fetch(url, { method, credentials: 'include', body: fd, headers: { 'X-CSRFToken': csrfToken || '' } })
        const j = res.ok ? await res.json() : null
        if (!res.ok) {
            showToast(`Error: Request failed`, 'error')
            return
        }
        if (j && j.status === 'success') {
            try {
                try {
                    const name = form.value.firstName || form.value.username || ''
                    const toast = { message: `Create ${name} successfully`, type: 'success' }
                    localStorage.setItem('pending_toast', JSON.stringify(toast))
                } catch (e) {}
                try {
                    const pendingUser = {
                        username: form.value.username || '',
                        first_name: form.value.firstName || '',
                        last_name: form.value.lastName || '',
                        email: form.value.email || '',
                        id: initialUserId || null,
                        mode: mode && mode.value ? mode.value : 'add'
                    }
                    localStorage.setItem('pending_user', JSON.stringify(pendingUser))
                } catch (e) {}
                try { router.push('/user-management') } catch (e) { router.back() }
            } catch (e) { console.error('redirect error', e) }
            return
        } else {
            const msg = (j && (j.message || j.error)) || 'Unknown error'
            showToast(`Error: ${msg}`, 'error')
            return
        }
    } catch (e) {
        console.error('submit error', e)
        showToast(`submit error ${e.message || e}`, 'error')
    } finally {
        loading.value = false
    }
}

function cancel() {
    try { router.back() } catch (e) { router.push('/user-management') }
}

function setSelectedPermissionsFromCustomRole(roleId) {
    const role = customRoles.value.find(r => String(r.id) === String(roleId))
    clearSelectedPermissions()
    if (!role) return
    // Normalize role permission names: flatten nested arrays, trim and lowercase
    let permNames = []
    if (Array.isArray(role.permissions)) {
        permNames = role.permissions.flat(Infinity).map(x => String(x || '').trim().toLowerCase()).filter(Boolean)
    }

    for (const p of allPermissions.value) {
        const pname = String(p.name || p.action || '').trim().toLowerCase()
        // exact match or fuzzy contains (to handle 'PlayBack' vs 'Playback')
        const matched = permNames.some(rn => rn === pname || rn.includes(pname) || pname.includes(rn))
        if (matched) selectedPermissions.value[p.action] = true
    }
}

const buildGroupTeamsMap = (groupList, teamList) => {
    const map = {}
    for (const g of groupList) map[g.id] = []
    for (const t of teamList) {
        const gid = t.user_group_id || t.user_group || t.user_group_id_id || t.user_group_id
        if (gid != null && map[gid]) map[gid].push(t)
    }
    return map
}

const groupOptions = computed(() => {
    return groups.value.map(g => ({
        value: String(g.id || g.user_group_id || g.user_group || ''),
        label: g.group_name || g.group || g.name || (g.user_group && g.user_group.group_name) || g.user_group || ''
    }))
})


const selectedTeamId = ref(null)

// File audio select state
const selectedFileId = ref([])
const fileOptions = ref([])
let _fileSearchTimer = null

function onFileSearch(term) {
    if (_fileSearchTimer) clearTimeout(_fileSearchTimer)
    _fileSearchTimer = setTimeout(async () => {
        try {
            const q = String(term || '').trim()
            // when search is empty: show only the currently-selected items (fetch any missing)
            if (!q) {
                if (Array.isArray(selectedFileId.value) && selectedFileId.value.length > 0) {
                    const selIds = selectedFileId.value.map(x => String(x))
                    // existing selected options already present
                    const existingSelected = (fileOptions.value || []).filter(f => selIds.includes(String(f.value)))
                    const missing = selIds.filter(id => !existingSelected.some(e => String(e.value) === String(id)))
                    let fetched = []
                    if (missing.length > 0) {
                        try {
                            const urlSel = `${API_GET_FILE_AUDIO()}?ids=${encodeURIComponent(missing.join(','))}`
                            const resSel = await fetch(urlSel, { credentials: 'include' })
                            if (resSel.ok) {
                                const js = await resSel.json()
                                const its = Array.isArray(js.data) ? js.data : (Array.isArray(js.results) ? js.results : [])
                                fetched = its.map(it => ({ label: it.file_name, value: it.id != null ? String(it.id) : (it.file_name || '') }))
                            }
                        } catch (e) {
                            console.error('file missing fetch error', e)
                        }
                    }
                    // show only selected items (existing + fetched) in the dropdown
                    const onlySelected = [...existingSelected]
                    for (const f of fetched) if (!onlySelected.some(x => String(x.value) === String(f.value))) onlySelected.push(f)
                    fileOptions.value = onlySelected
                    return
                }
                fileOptions.value = []
                return
            }

            const url = `${API_GET_FILE_AUDIO()}?file_name=${encodeURIComponent(q)}`
            const res = await fetch(url, { credentials: 'include' })
            if (!res.ok) {
                fileOptions.value = []
                return
            }
            const j = await res.json()
            const items = Array.isArray(j.data) ? j.data : (Array.isArray(j.results) ? j.results : (Array.isArray(j) ? j : []))
            // map search results to options (value = id as string, label = file_name)
            const mapped = items.map(it => ({ label: it.file_name, value: it.id != null ? String(it.id) : (it.file_name || '') }))

            // Ensure any currently-selected IDs are also present (fetch missing by ids)
            const sel = Array.isArray(selectedFileId.value) ? selectedFileId.value.map(x => String(x)) : []
            const missing = sel.filter(id => !mapped.some(m => String(m.value) === String(id)))
            if (missing.length > 0) {
                try {
                    const urlMiss = `${API_GET_FILE_AUDIO()}?ids=${encodeURIComponent(missing.join(','))}`
                    const resMiss = await fetch(urlMiss, { credentials: 'include' })
                    if (resMiss.ok) {
                        const jm = await resMiss.json()
                        const itsm = Array.isArray(jm.data) ? jm.data : (Array.isArray(jm.results) ? jm.results : [])
                        const mappedMissing = itsm.map(it => ({ label: it.file_name, value: it.id != null ? String(it.id) : (it.file_name || '') }))
                        // merge keeping search order first, then missing (dedupe)
                        const merged = [...mapped]
                        for (const mm of mappedMissing) if (!merged.some(x => String(x.value) === String(mm.value))) merged.push(mm)
                        fileOptions.value = merged
                    } else {
                        fileOptions.value = mapped
                    }
                } catch (e) {
                    console.error('file missing fetch error', e)
                    fileOptions.value = mapped
                }
            } else {
                fileOptions.value = mapped
            }

        } catch (e) {
            console.error('file search error', e)
            fileOptions.value = []
        }
    }, 300)
}


const selectedDatabaseIds = ref([])
const selectedAllDatabases = ref(false)
const defaultDatabaseIds = ref([])

function toggleDatabase(db) {
    if (databaseDisabled && databaseDisabled.value) return
    const idStr = String(db.id)
    const idx = selectedDatabaseIds.value.indexOf(idStr)
    if (idx === -1) selectedDatabaseIds.value.push(idStr)
    else selectedDatabaseIds.value.splice(idx, 1)
    selectedAllDatabases.value = databases.value.length > 0 && selectedDatabaseIds.value.length === databases.value.length
}

watch(selectedTeamId, (teamId) => {
    // If selectedDatabaseIds already set (e.g., from initialData), don't overwrite it.
    if (selectedDatabaseIds.value && selectedDatabaseIds.value.length > 0) {
        // Still clear when team is unset
        if (!teamId) selectedDatabaseIds.value = []
        return
    }

    if (!teamId) {
        selectedDatabaseIds.value = []
        return
    }
    const team = teams.value.find(t => String(t.id) === String(teamId))
    if (!team) return
    let mains = []
    try {
        if (typeof team.maindatabase === 'string') mains = JSON.parse(team.maindatabase)
        else if (Array.isArray(team.maindatabase)) mains = team.maindatabase
    } catch (e) {
        if (typeof team.maindatabase === 'string') {
            mains = team.maindatabase.replace(/[[\]\"]+/g, '').split(',').map(s => s.trim()).filter(Boolean)
        }
    }
    selectedDatabaseIds.value = mains.map(x => String(x))
    defaultDatabaseIds.value = [...selectedDatabaseIds.value]
    selectedAllDatabases.value = databases.value.length > 0 && selectedDatabaseIds.value.length === databases.value.length
})

function resetDatabase() {
    selectedDatabaseIds.value = [...defaultDatabaseIds.value]
    // reflect if all databases are selected by the default
    selectedAllDatabases.value = databases.value.length > 0 && selectedDatabaseIds.value.length === databases.value.length
}

function toggleAllDatabases() {
    if (databaseDisabled && databaseDisabled.value) return
    selectedAllDatabases.value = !selectedAllDatabases.value
    if (selectedAllDatabases.value) {
        selectedDatabaseIds.value = databases.value.map(d => String(d.id))
    } else {
        selectedDatabaseIds.value = []
    }
}

const baseRoles = ref({})
const selectedBaseRoleKey = ref(null)
const selectedPermissions = ref({})

const databaseDisabled = computed(() => String(selectedBaseRoleKey.value) === 'ticket')

watch(selectedBaseRoleKey, (val) => {
    try {
        if (String(val) === 'ticket') {
            // clear any selected databases and prevent changes
            selectedDatabaseIds.value = []
            selectedAllDatabases.value = false
        }
    } catch (e) {}
})

const permissionInputsEnabled = computed(() => {
    // Always enable editing of permissions in edit mode
    if (mode && mode.value === 'edit') return true
    return !!selectedBaseRoleKey.value || !!selectedCustomRoleId.value
})

const roleCardsDisabled = computed(() => false)

function clearSelectedPermissions() {
    selectedPermissions.value = {}
}

function selectBaseRole(roleKey) {
    if (!roleKey) return
    if (selectedBaseRoleKey.value === roleKey) {
        selectedBaseRoleKey.value = null
        clearSelectedPermissions()
        return
    }

    selectedBaseRoleKey.value = roleKey
    selectedCustomRoleId.value = null

    // clear role error when user selects a base role
    errors.role = false

    clearSelectedPermissions()
    const br = baseRoles.value && baseRoles.value[roleKey]
    if (br && Array.isArray(br.permissions)) {
        const perms = br.permissions.flat().map(p => p.toString().trim())
        for (const p of perms) selectedPermissions.value[p] = true
    }
}

// Apply base role permissions without toggling selection (used when initializing from API)
function applyBaseRolePermissions(roleKey) {
    if (!roleKey) return
    selectedBaseRoleKey.value = roleKey
    selectedCustomRoleId.value = null
    clearSelectedPermissions()
    const br = baseRoles.value && baseRoles.value[roleKey]
    if (br && Array.isArray(br.permissions)) {
        const perms = br.permissions.flat().map(p => p.toString().trim())
        for (const p of perms) selectedPermissions.value[p] = true
    }
}

function togglePermission(perm) {
    if (!permissionInputsEnabled.value) return
    const k = perm.action
    selectedPermissions.value[k] = !selectedPermissions.value[k]
}

const teamOptions = computed(() => {
    const gid = selectedGroupId.value
    if (!gid) return []
    return teams.value
        .filter(t => {
            const tgid = (t.user_group && (t.user_group.id || t.user_group.user_group_id)) || t.user_group_id || t.user_group_id_id || t.user_group
            return String(tgid) === String(gid)
        })
        .map(t => ({ value: String(t.id || t.user_team_id || t.id || ''), label: t.name || t.team_name || t.name }))
})

watch(selectedGroupId, (val, old) => {
    // Only clear selected team when the group changes after an existing selection.
    // This prevents populateFromInitial (which sets group then team) from being cleared.
    if (old !== null && old !== undefined && String(old) !== String(val)) {
        selectedTeamId.value = null
    }
})

const fetchData = async () => {
    const task = (async () => {
        loading.value = true
        try {
            const res = await fetch(API_GROUP_INDEX(), { credentials: 'include' })
            if (!res.ok) {
                console.error('Failed to fetch groups', res.status)
                return
            }
            const json = await res.json()
            groups.value = Array.isArray(json.user_group) ? json.user_group : []
            teams.value = Array.isArray(json.user_team) ? json.user_team : []
            groupTeamsMap.value = buildGroupTeamsMap(groups.value, teams.value)
            try {
                const dbRes = await fetch(API_GET_DATABASE(), { credentials: 'include' })
                if (dbRes.ok) {
                    const dbJson = await dbRes.json()
                    if (Array.isArray(dbJson.results)) {
                        databases.value = dbJson.results
                    } else if (Array.isArray(dbJson)) {
                        databases.value = dbJson
                    } else if (Array.isArray(dbJson.main_db)) {
                        databases.value = dbJson.main_db
                    } else if (Array.isArray(dbJson.databases)) {
                        databases.value = dbJson.databases
                    } else {
                        databases.value = []
                    }
                    // If initial data requested all DBs selected, apply selection now that DB list is available
                    if (selectedAllDatabases.value) {
                        selectedDatabaseIds.value = databases.value.map(d => String(d.id))
                        defaultDatabaseIds.value = [...selectedDatabaseIds.value]
                        selectedAllDatabases.value = databases.value.length > 0 && selectedDatabaseIds.value.length === databases.value.length
                    }
                } else {
                    console.error('Failed to fetch databases', dbRes.status)
                }
            } catch (dbError) {
                console.error('Error fetching databases:', dbError)
            }
        } catch (error) {
            console.error('Error fetching groups:', error)
        } finally {
            loading.value = false
        }
    })()
    registerRequest(task)
    await task
}

const fetchGetAllRolesPermissions = async () => {
    const task = (async () => {
        loading.value = true
        try {
            const res = await fetch(API_GET_ALL_ROLES_PERMISSIONS(), { credentials: 'include' })
            if (!res.ok) {
                console.error('Failed to fetch get all roles permissions', res.status)
                return
            }
            const json = await res.json()
            const perms = Array.isArray(json.all_permissions) ? json.all_permissions : []
            allPermissions.value = perms
            customRoles.value = Array.isArray(json.custom_roles) ? json.custom_roles : []
            baseRoles.value = json.base_roles || {}

            const map = {}
            for (const t of orderedTypes) map[t] = []
            for (const p of perms) {
                const t = (p.type || '').toString().trim().toLowerCase()
                if (!map[t]) map[t] = []
                map[t].push(p)
            }
            for (const t of orderedTypes) {
                groupedPermissions.value[t] = map[t] || []
            }

            // If the component already has an initial selected role (from props.initialData),
            // apply the corresponding permissions now that baseRoles/customRoles are loaded.
            if (selectedBaseRoleKey.value) {
                applyBaseRolePermissions(selectedBaseRoleKey.value)
            } else if (selectedCustomRoleId.value) {
                setSelectedPermissionsFromCustomRole(selectedCustomRoleId.value)
            }

        } catch (error) {
            console.error('Error fetching permissions:', error)
        } finally {
            loading.value = false
        }
    })()
    registerRequest(task)
    await task
}
onMounted(() => {
    fetchData()
    fetchGetAllRolesPermissions()
})

// react to initial data (populate when parent passes data or it arrives async)
onMounted(() => {
    if (props.initialData) populateFromInitial(props.initialData)
})

watch(() => props.initialData, (val) => {
    if (val) populateFromInitial(val)
})

// clear individual field errors when user edits inputs
// Real-time field validation watchers
watch(() => form.value.firstName, (val) => {
    if (!val || String(val).trim() === '') {
        errors.firstName = false
        return
    }
    const v = String(val).trim()
    if (!/^[\p{L}\s]+$/u.test(v)) errors.firstName = 'Special characters are not allowed in first name'
    else errors.firstName = false
})

watch(() => form.value.lastName, (val) => {
    if (!val || String(val).trim() === '') {
        errors.lastName = false
        return
    }
    const v = String(val).trim()
    if (!/^[\p{L}\s]+$/u.test(v)) errors.lastName = 'Special characters are not allowed in last name'
    else errors.lastName = false
})

watch(() => form.value.password, (val) => {
    // clear or validate password length
    if (!val || String(val).trim() === '') {
        errors.password = false
    } else if (String(val).length < 8) {
        errors.password = 'Password must be at least 8 characters long'
    } else {
        errors.password = false
    }
    // also validate confirm match when confirm present
    if (form.value.confirmPassword && String(form.value.confirmPassword).trim() !== '') {
        if (val !== form.value.confirmPassword) errors.confirmPassword = 'Passwords do not match'
        else errors.confirmPassword = false
    }
})

watch(() => form.value.confirmPassword, (val) => {
    if (!val || String(val).trim() === '') { errors.confirmPassword = false; return }
    if (form.value.password !== val) errors.confirmPassword = 'Passwords do not match'
    else errors.confirmPassword = false
})

watch(() => selectedGroupId.value, (v) => { if (v) errors.group = false })
watch(() => selectedTeamId.value, (v) => { if (v) errors.team = false })

watch(() => form.value.email, (val) => {
    if (!val || String(val).trim() === '') { errors.email = false; return }
    const e = String(val).trim()
    const eok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e)
    errors.email = eok ? false : 'Please enter a valid email address'
})

watch(() => form.value.phone, (val) => {
    if (!val || String(val).trim() === '') { errors.phone = false; return }
    const v = String(val)
    // auto-strip non-digit characters to enforce numeric-only input
    const digits = v.replace(/\D+/g, '')
    if (digits !== v) {
        try { if (form && form.value) form.value.phone = digits } catch (e) {}
    }
    errors.phone = digits.length > 0 ? false : 'Phone must contain only numbers'
})
</script>

<style scoped>
/* (retain styles from AddUser.vue) */
.customize-btn {
    margin-left: auto;
    padding: 6px 16px;
    background: transparent;
    border: 1px solid #416fd6;
    border-radius: 20px;
    color: #416fd6;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
}

.customize-btn:hover {
    background: #416fd6;
    color: #fff;
}

.select-disabled {
    opacity: 0.6;
    pointer-events: none;
}

.card-left,
.card-right {
    background-color: rgba(0, 0, 0, 0);
    border: rgba(0, 0, 0, 0);
    gap: 14px;

}

.main-content {
    flex: 1 1 auto;
    padding: 83.5px 0px 16px 0px;
}

.main-wrapper {
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    max-height: calc(100vh - 140px);
}

.main-wrapper::-webkit-scrollbar {
    width: 4px;
    height: 4px;
}

.main-wrapper::-webkit-scrollbar-track {
    background: transparent;
}

.main-wrapper::-webkit-scrollbar-thumb {
    background-color: #416fd6;
    border-radius: 4px;
}

.database-grid,
.permissions-grid-3 {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
}

.permissions-grid-3 {
    max-height: none;
}

.db-card,
.permission-item {
    box-sizing: border-box;
    flex: 0 1 220px;
    min-width: 180px;
}

.card {
    overflow: visible;
}

.permission-group-header {
    grid-column: 1 / -1;
    font-weight: 600;
    color: rgb(108, 117, 125);
    margin: 16px 0px 8px;
    text-transform: uppercase;
    font-size: 12px;
}

.main-wrapper .card-body {
    overflow: visible ;
}

.dropdown-options::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

.dropdown-options::-webkit-scrollbar-track {
  background: transparent;
  margin-top: 6px;
  margin-bottom: 12px;
}

.dropdown-options::-webkit-scrollbar-thumb {
  background-color: #416fd6;
  border-radius: 4px;
}

/* Password visibility toggle styles */
.input-group { position: relative; }
.input-group .input { padding-right: 40px; }
.input-group .toggle-visibility {
    position: absolute;
    right: 8px;
    top: 16.5px;
    transform: translateY(-50%);
    background: transparent;
    border: none;
    cursor: pointer;
    color: #6b7280;
    font-size: 14px;
    padding: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.input-group .toggle-visibility:focus { outline: none; }

/* Role card error styling */
.role-card.role-card-error {
    border: 1px solid rgb(245, 163, 163) !important;
    box-shadow: rgba(220, 53, 69, 0.25) 0px 0px 0px 0.2rem !important;
    border-radius: 8px;
}
.permission-item:has(input:checked):has(input:disabled)  {
    border-color: #416fd6;
}
.permission-item:has(input:checked):has(input:disabled) .perm-checkbox {
    background: #416fd6 !important;
    border-color: #416fd6;
}

.form-input-modal {
    border-radius: 25px;
    border: 1px solid rgb(245, 163, 163) !important;
    box-shadow: rgba(220, 53, 69, 0.25) 0px 0px 0px 0.2rem !important;
}

</style>
