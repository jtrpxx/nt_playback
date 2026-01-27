<template>
    <!-- Base Role Modal -->
    <div v-if="modelValue && mode === 'base'" class="modal-backdrop" @click.self="close" id="baseRolesModal">
        <div class="modal-box">
            <div class="modal-header">
                <div style="display: flex; align-items: center; gap: 4px">
                    <div :class="'base-role-modal-icon ' + titleIcon" id="baseRoleModalIcon">
                        <i :class="iconClass"></i>
                    </div>
                    <h3 class="modal-title ad" id="baseRoleModalTitle">{{ title }}</h3>
                </div>
                <button type="button" class="btn-close" @click="close"></button>
            </div>
            <div class="modal-body">
                <div class="form-group-modal">
                    <div class="permissions-section-title">Permissions</div>
                    <div class="permissions-grid" id="baseRolePermissionsGrid">
                        <template v-if="loading">
                            <div class="container-overlay" style="height: 487px;">
                                <div class="overlay-box">Loading...</div>
                            </div>
                        </template>
                        <template v-else>
                            <div v-for="(perms, type) in groupedPermissions" :key="type" class="permission-group">
                                <div class="permission-group-header">{{ type }}</div>
                                <div class="permission-list">
                                    <label v-for="perm in perms" :key="perm.action" class="permission-item">
                                        <input type="checkbox" :value="perm.action" v-model="rolePermissions"
                                            :disabled="checkDisabled" />
                                        <span class="perm-checkbox" aria-hidden></span>
                                        <span class="perm-label">{{ perm.name }}</span>
                                    </label>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn-role btn-secondary" @click="onReset" style="margin-right: auto">
                    <i class="fas fa-undo"></i>
                    Reset to Default
                </button>
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

    <!-- Create Role Modal -->
    <div v-if="modelValue && mode === 'create'" class="modal-backdrop" @click.self="close" id="createRolesModal">
        <div class="modal-box">
            <div class="modal-header">
                <div style="display: flex; align-items: center; gap: 4px">
                    <div class="base-role-modal-icon operator" id="createRoleModalIcon">
                        <i class="fas fa-users-cog"></i>
                    </div>
                    <h3 class="modal-title ad" id="createRoleModalTitle">Create New Role</h3>
                </div>
                <button type="button" class="btn-close" @click="close"></button>
            </div>
            <div class="modal-body">
                <div class="form-group-modal">
                    <label class="form-label-modal">Role Name</label>
                    <input v-model="roleNameInput" type="text" class="form-input-modal" id="createRoleName"
                        placeholder="Enter role name..." maxlength="25">
                </div>
                <div class="form-group-modal">                  
                    <div class="permissions-grid" id="createRolePermissionsGrid">
                        <template v-if="loading">
                            <div class="container-overlay" style="height: 487px;">
                                <div class="overlay-box">Loading...</div>
                            </div>
                        </template>
                        <template v-else>
                            <div
                                style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                <div class="permissions-section-title" style="margin-bottom: 0;">Select Permissions
                                </div>
                                <div style="width: 250px;">
                                    <div class="input-group">
                                    <CustomSelect class="select-search select-checkbox" v-model="filters.roleAll"
                                        :options="roleAllOptions" placeholder="Copy from Role..." name="copyRoleModal" />
                                    </div>
                                </div>
                            </div>
                            <div v-for="(perms, type) in groupedPermissions" :key="type" class="permission-group">
                                <div class="permission-group-header">{{ type }}</div>
                                <div class="permission-list">
                                    <label v-for="perm in perms" :key="perm.action" class="permission-item">
                                        <input type="checkbox" :value="perm.action" v-model="rolePermissions"
                                            :disabled="checkDisabled" />
                                        <span class="perm-checkbox" aria-hidden></span>
                                        <span class="perm-label">{{ perm.name }}</span>
                                    </label>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn-role btn-secondary" @click="onReset" style="margin-right: auto">
                    <i class="fas fa-undo"></i>
                    Reset to Default
                </button>
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

    <!-- Edit Role Modal -->
    <div v-if="modelValue && mode === 'edit'" class="modal-backdrop" @click.self="close" id="editRolesModal">
        <div class="modal-box">
            <div class="modal-header">
                <div style="display: flex; align-items: center; gap: 4px">
                    <div class="base-role-modal-icon operator" id="editRoleModalIcon">
                        <i class="fa-solid fa-pen-to-square"></i>
                    </div>
                    <h3 class="modal-title ad" id="editRoleModalTitle">Edit Role</h3>
                </div>
                <button type="button" class="btn-close" @click="close"></button>
            </div>
            <div class="modal-body">
                <div class="form-group-modal">
                    <label class="form-label-modal">Role Name</label>
                    <input v-model="roleNameInput" type="text" class="form-input-modal" id="editRoleName"
                        placeholder="Enter role name..." maxlength="25">
                </div>
                <div class="form-group-modal">
                    <div class="permissions-section-title">Select Permissions</div>
                    <div class="permissions-grid" id="editRolePermissionsGrid">
                        <template v-if="loading">
                            <div class="container-overlay" style="height: 487px;">
                                <div class="overlay-box">Loading...</div>
                            </div>
                        </template>
                        <template v-else>
                            <div v-for="(perms, type) in groupedPermissions" :key="type" class="permission-group">
                                <div class="permission-group-header">{{ type }}</div>
                                <div class="permission-list">
                                    <label v-for="perm in perms" :key="perm.action" class="permission-item">
                                        <input type="checkbox" :value="perm.action" v-model="rolePermissions"
                                            :disabled="checkDisabled" />
                                        <span class="perm-checkbox" aria-hidden></span>
                                        <span class="perm-label">{{ perm.name }}</span>
                                    </label>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn-role btn-secondary" @click="onReset" style="margin-right: auto">
                    <i class="fas fa-undo"></i>
                    Reset to Default
                </button>
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
import { watch, computed, ref } from 'vue'
import CustomSelect from './CustomSelect.vue'
import '../assets/css/components.css'

import { API_GET_DETAILS_ROLE, API_INDEX_ROLE } from '../api/paths'

const props = defineProps({
    modelValue: { type: Boolean, default: false },
    roleId: { type: [String, Number], default: null },
    roleName: { type: String, default: '' },
    mode: { type: String, default: 'base' }
})
const emit = defineEmits(['update:modelValue'])

const close = () => emit('update:modelValue', false)

const onReset = () => {
    if (window && typeof window.resetBaseRole === 'function') window.resetBaseRole()
}

const onSave = () => {
    if (window && typeof window.updateBaseRole === 'function') window.updateBaseRole()
}

// using centralized endpoint functions from src/api/paths.js

const loading = ref(false)
const roleNameInput = ref('')
const allPermissions = ref([])
const rolePermissions = ref([])
const isAdministrator = ref(false)
const checkDisabled = computed(() => String(props.roleId) === '1')

// For the "Copy from Role" select
const roleAllOptions = ref([])
const filters = ref({ roleAll: [] })

async function fetchIndexRoles() {
    try {
        const res = await fetch(API_INDEX_ROLE(), { credentials: 'include' })
        if (!res.ok) throw new Error('Failed to fetch index roles')
        const json = await res.json()
        const customs = Array.isArray(json.user_permission_other) ? json.user_permission_other : []
        // Build options: base roles first, then custom roles
        const base = [
            { label: 'Administrator', value: 'base:1' },
            { label: 'Auditor', value: 'base:2' },
            { label: 'Operator/Agent', value: 'base:3' }
        ]
        const customOpts = customs.map(r => ({ label: r.name || `Role ${r.id}`, value: `custom:${r.id}` }))
        roleAllOptions.value = [
            { group: 'Base Roles', options: base },
            { group: 'Custom Roles', options: customOpts }
        ]
    } catch (e) {
        console.error('fetchIndexRoles error', e)
        roleAllOptions.value = [
            { group: 'Base Roles', options: base },
            { group: 'Custom Roles', options: [] }
        ]
    }
}

// When user selects an option to copy from, fetch that role's permissions and apply
watch(() => filters.value.roleAll, async (val) => {
    if (!props.modelValue || props.mode !== 'create') return
    if (!Array.isArray(val) || val.length === 0) {
        rolePermissions.value = []
        return
    }
    // take the last selected (most recent) as the source to copy
    const sel = val[val.length - 1]
    if (!sel) return
    if (String(sel).startsWith('base:')) {
        const id = String(sel).split(':')[1]
        // fetch the base role details and set rolePermissions
        try {
            const res = await fetch(API_GET_DETAILS_ROLE() + id, { credentials: 'include' })
            if (!res.ok) throw new Error('Failed to fetch role details')
            const data = await res.json()
            const rp = Array.isArray(data.role_permissions) ? data.role_permissions : []
            rolePermissions.value = rp.slice()
        } catch (e) {
            console.error('Error copying base role permissions', e)
        }
    } else if (String(sel).startsWith('custom:')) {
        const id = String(sel).split(':')[1]
        try {
            const res = await fetch(API_GET_DETAILS_ROLE() + id, { credentials: 'include' })
            if (!res.ok) throw new Error('Failed to fetch custom role details')
            const data = await res.json()
            const rp = Array.isArray(data.role_permissions) ? data.role_permissions : []
            rolePermissions.value = rp.slice()
        } catch (e) {
            console.error('Error copying custom role permissions', e)
        }
    }
})

async function fetchRoleDetails(roleId) {
    if (!roleId) return
    loading.value = true
    const startTime = Date.now()
    try {
        const res = await fetch(API_GET_DETAILS_ROLE() + roleId, { credentials: 'include' })
        if (!res.ok) throw new Error('Failed to fetch role details')
        const data = await res.json()
        if (data && data.status) {
            roleNameInput.value = data.role_name || ''
            allPermissions.value = Array.isArray(data.all_permissions) ? data.all_permissions : []
            rolePermissions.value = Array.isArray(data.role_permissions) ? data.role_permissions : []
            // fallback for administrator detection
            isAdministrator.value = Boolean(data.is_administrator) || String(roleId) === '1' || (data.role_name && String(data.role_name).toLowerCase() === 'administrator')
        } else {
            allPermissions.value = []
            rolePermissions.value = []
        }
    } catch (e) {
        console.error('Error fetching role details:', e)
        allPermissions.value = []
        rolePermissions.value = []
    } finally {
        // ensure loading indicator is visible at least 1s for UX
        const elapsed = Date.now() - startTime
        const minMs = 500
        if (elapsed < minMs) {
            await new Promise(r => setTimeout(r, minMs - elapsed))
        }
        loading.value = false
    }
}

const title = computed(() => {
    if (props.roleName) return props.roleName
    switch (String(props.roleId)) {
        case '1': return 'Edit Administrator'
        case '2': return 'Edit Auditor'
        case '3': return 'Edit Operator/Agent'
    }
})

const titleIcon = computed(() => {
    switch (String(props.roleId)) {
        case '1': return 'admin'
        case '2': return 'auditor'
        case '3': return 'operator'
    }
})

const iconClass = computed(() => {
    switch (String(props.roleId)) {
        case '1': return 'fas fa-crown'
        case '2': return 'fas fa-clipboard-check'
        case '3': return 'fas fa-headset'
    }
})

watch(() => props.modelValue, async (val) => {
    if (!val) return
    // prefer legacy initializer only for non-create flows
    if (props.mode !== 'create' && window && typeof window.initBaseRoleModal === 'function') {
        try { window.initBaseRoleModal(props.roleId) } catch (e) { console.error(e) }
    }

    // When opening the modal in `create` mode, use roleId=1 (Administrator) as the
    // source of available permissions but do not pre-check any boxes.
    if (props.mode === 'create') {
        // Fetch admin permissions as the default available set
        await fetchRoleDetails(1)
        rolePermissions.value = []
        // Clear any role name input so the user provides a new name (roleName prop may provide placeholder)
        roleNameInput.value = ''
        // populate copy-select options
        await fetchIndexRoles()
        // reset copy selection
        filters.value.roleAll = []
        return
    }

    // default: fetch details for the provided roleId
    fetchRoleDetails(props.roleId)
})

const groupedPermissions = computed(() => {
    const ap = allPermissions.value || []
    const grouped = ap.reduce((acc, perm) => {
        const type = perm.type || 'Other'
        if (!acc[type]) acc[type] = []
        acc[type].push(perm)
        return acc
    }, {})

    const order = ['access', 'audio recordings', 'user management', 'logs']
    const keys = Object.keys(grouped).sort((a, b) => {
        const ia = order.indexOf(a.toLowerCase())
        const ib = order.indexOf(b.toLowerCase())
        if (ia !== -1 && ib !== -1) return ia - ib
        if (ia !== -1) return -1
        if (ib !== -1) return 1
        return a.localeCompare(b)
    })

    const ordered = {}
    keys.forEach(k => ordered[k] = grouped[k])
    return ordered
})
</script>

<style scoped>
/* Permissions layout */
.permission-group {
    margin-bottom: 22px !important;
}

.permissions-section-title {
    margin-bottom: 8px;
    font-weight: 700
}

.permissions-grid {
    display: block;
    position: relative;
    min-height: 140px
}

.container-overlay {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    background: rgba(255, 255, 255, 0.7);
    border-radius: 8px;
    width: 100%;
    padding-top: 15%;
    box-sizing: border-box
}

.permission-group {
    margin-bottom: 18px
}

.permission-group-header {
    font-weight: 700;
    color: #6c757d;
    margin: 10px 0 8px;
    text-transform: uppercase;
    font-size: 12px;
    letter-spacing: .02em;
}

.permission-list {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 8px;
}

.permission-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 14px;
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    cursor: pointer;
    transition: all .15s ease;
}

/* responsive: fewer columns on small widths */
@media (max-width: 900px) {
    .permission-list {
        grid-template-columns: repeat(2, 1fr)
    }
}

@media (max-width: 520px) {
    .permission-list {
        grid-template-columns: repeat(1, 1fr)
    }
}

/* make modal body scrollable if content tall */
.modal-body {
    max-height: 60vh;
    overflow: auto
}

/* checked state (non-disabled only) */
.permission-item:has(input:checked):not(:has(input:disabled)) {
    background: rgba(65, 111, 214, 0.1);
    border-color: #416fd6;
}

.permission-item:has(input:checked):not(:has(input:disabled)) .perm-checkbox {
    background: #416fd6 !important;
    border-color: #416fd6;
}

.permission-item:has(input:checked):not(:has(input:disabled)) .perm-checkbox::after {
    content: "\2713";
    color: #fff;
}

.permission-item:has(input:checked):not(:has(input:disabled)) .perm-label {
    color: #777f8c;
}

.permission-item:has(input:checked):has(input:disabled) .perm-checkbox {
    background: #c5c5c5 !important;
    border-color: transparent;
}


</style>