<template>
    <!-- Create group  -->
    <div v-if="modelValue && mode === 'createGroup'" class="modal-backdrop" @click.self="close" id="createGroupModal">
        <div class="modal-box">
            <div class="modal-header">
                <div style="display: flex; align-items: center; gap: 4px">
                    <div class="blue-icon" id="createGroupModalIcon">
                        <i class="fa-solid fa-user-group"></i>
                    </div>
                    <h3 class="modal-title ad" id="createGroupModalTitle">Create Group</h3>
                </div>
                <button type="button" class="btn-close" @click="close"></button>
            </div>
            <div class="modal-body">
                <div class="form-group-modal">
                    <div class="permissions-grid-2" id="groupGrid">
                        <div class="col-lg-12">
                            <div class="form-group-modal">
                                <div class="input-group" v-has-value>
                                    <input required="" v-model="name" type="text" name="groupNameModal"
                                        autocomplete="off" class="input" maxlength="30">
                                    <label class="title-label">Group name</label>
                                </div>
                            </div>
                        </div>

                        <div class="col-lg-12">
                            <div class="form-group-modal">
                                <div class="form-group-modal">
                                    <div class="input-group" v-has-value>
                                        <input required="" v-model="description" type="text" name="descriptionModal"
                                            autocomplete="off" class="input" maxlength="50">
                                        <label class="title-label">Description</label>
                                    </div>
                                </div>
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

    <!-- Edit group  -->
    <div v-if="modelValue && mode === 'editGroup'" class="modal-backdrop" @click.self="close" id="editGroupModal">
        <div class="modal-box">
            <div class="modal-header">
                <div style="display: flex; align-items: center; gap: 4px">
                    <div class="blue-icon" id="editGroupModalIcon">
                        <i class="fa-solid fa-user-group"></i>
                    </div>
                    <h3 class="modal-title ad" id="editGroupModalTitle">Edit Group</h3>
                </div>
                <button type="button" class="btn-close" @click="close"></button>
            </div>
            <div class="modal-body">
                <div class="form-group-modal">
                    <div class="permissions-grid-2" id="groupGrid">
                        <div class="col-lg-12">
                            <div class="form-group-modal">
                                <div class="input-group" v-has-value>
                                    <input required="" v-model="name" type="text" name="groupNameModal"
                                        autocomplete="off" class="input" maxlength="30">
                                    <label class="title-label">Group name</label>
                                </div>
                            </div>
                        </div>

                        <div class="col-lg-12">
                            <div class="form-group-modal">
                                <div class="form-group-modal">
                                    <div class="input-group" v-has-value>
                                        <input required="" v-model="description" type="text" name="descriptionModal"
                                            autocomplete="off" class="input" maxlength="50">
                                        <label class="title-label">Description</label>
                                    </div>
                                </div>
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

    <!-- Create Team  -->
    <div v-if="modelValue && mode === 'createTeam'" class="modal-backdrop" @click.self="close" id="createTeamModal">
        <div class="modal-box">
            <div class="modal-header">
                <div style="display: flex; align-items: center; gap: 4px">
                    <div class="blue-icon" id="createTeamModalIcon">
                        <i class="fa-solid fa-people-group"></i>
                    </div>
                    <h3 class="modal-title ad" id="createTeamModalTitle">Create Team</h3>
                </div>
                <button type="button" class="btn-close" @click="close"></button>
            </div>
            <div class="modal-body">
                <div class="form-group-modal">
                    <div class="permissions-grid-2" id="groupGrid">
                        <div class="col-lg-12">
                            <div class="form-group-modal">
                                <div class="input-group">
                                    <CustomSelect class="select-search select-checkbox" v-model="selectedGroupId"
                                        :options="groupOptions" placeholder="Select Group" name="groupModal" />
                                </div>
                            </div>
                        </div>

                        <div class="col-lg-12">
                            <div class="form-group-modal">
                                <div class="form-group-modal">
                                    <div class="input-group" v-has-value>
                                        <input required="" v-model="name" type="text" name="teamNameModal"
                                            autocomplete="off" class="input" maxlength="30">
                                        <label class="title-label">Team Name</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="col-lg-12">
                        <div class="form-group-modal">
                            <div class="permissions-section-title"
                                style="display: flex; align-items: center; gap: 15px;margin-bottom: 5px;">
                                Database Server
                                <span class="d-none" style="color: red; font-size: 14px; font-weight: normal;"
                                    id="validateCreateDatabase"><i class="fa-solid fa-circle-exclamation"></i> This
                                    select is required</span>
                            </div>
                            <div class="permissions-grid-2" id="DatabseSeverGrid">
                                <div v-if="loadingDatabases" style="padding:8px;color:#64748b">Loading databases...</div>
                                <template v-else>
                                    <div style="margin-bottom:8px;">
                                        <label class="permission-item">
                                            <input type="checkbox" v-model="selectAll" />
                                            <span class="perm-checkbox" aria-hidden></span>
                                            <span style="font-weight:600">All databases</span>
                                        </label>
                                    </div>
                                    <div v-for="db in databases" :key="db.id" style="margin-bottom:8px;">
                                        <label class="permission-item">
                                            <input type="checkbox" :value="db.id" v-model="selectedDatabaseIds" />
                                            <span class="perm-checkbox" aria-hidden></span>
                                            <span>{{ db.database_name || db.name || db.display_name }}</span>
                                        </label>
                                    </div>
                                    <div v-if="databases.length === 0" class="empty-state" style="padding:8px;color:#64748b">No databases found.</div>
                                </template>
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

    <!-- Edit team  -->
    <div v-if="modelValue && mode === 'editTeam'" class="modal-backdrop" @click.self="close" id="editTeamModal">
        <div class="modal-box">
            <div class="modal-header">
                <div style="display: flex; align-items: center; gap: 4px">
                    <div class="blue-icon" id="editTeamModalIcon">
                        <i class="fa-solid fa-people-group"></i>
                    </div>
                    <h3 class="modal-title ad" id="editTeamModalTitle">Edit Team</h3>
                </div>
                <button type="button" class="btn-close" @click="close"></button>
            </div>
            <div class="modal-body">
                <div class="form-group-modal">
                    <div class="permissions-grid-2" id="groupGrid">
                        <div class="col-lg-12">
                            <div class="form-group-modal">
                                <div class="input-group">
                                    <CustomSelect class="select-search select-checkbox" v-model="selectedGroupId"
                                        :options="groupOptions" placeholder="Select Group" name="groupModal" />
                                </div>
                            </div>
                        </div>

                        <div class="col-lg-12">
                            <div class="form-group-modal">
                                <div class="form-group-modal">
                                    <div class="input-group" v-has-value>
                                        <input required="" v-model="name" type="text" name="teamNameModal"
                                            autocomplete="off" class="input" maxlength="30">
                                        <label class="title-label">Team Name</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="col-lg-12">
                        <div class="form-group-modal">
                            <div class="permissions-section-title"
                                style="display: flex; align-items: center; gap: 15px;margin-bottom: 5px;">
                                Database Server
                                <span class="d-none" style="color: red; font-size: 14px; font-weight: normal;"
                                    id="validateCreateDatabase"><i class="fa-solid fa-circle-exclamation"></i> This
                                    select is required</span>
                            </div>
                            <div class="permissions-grid-2" id="DatabseSeverGrid">
                                <div v-if="loadingDatabases" style="padding:8px;color:#64748b">Loading databases...</div>
                                <template v-else>
                                    <div style="margin-bottom:8px;">
                                        <label class="permission-item">
                                            <input type="checkbox" v-model="selectAll" />
                                            <span class="perm-checkbox" aria-hidden></span>
                                            <span style="font-weight:600">All databases</span>
                                        </label>
                                    </div>
                                    <div v-for="db in databases" :key="db.id" style="margin-bottom:8px;">
                                        <label class="permission-item">
                                            <input type="checkbox" :value="db.id" v-model="selectedDatabaseIds" />
                                            <span class="perm-checkbox" aria-hidden></span>
                                            <span>{{ db.database_name || db.name || db.display_name }}</span>
                                        </label>
                                    </div>
                                    <div v-if="databases.length === 0" class="empty-state" style="padding:8px;color:#64748b">No databases found.</div>
                                </template>
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
import { watch, computed, ref } from 'vue'
import CustomSelect from './CustomSelect.vue'
import { API_GET_DATABASE } from '../api/paths'

import '../assets/css/components.css'

const props = defineProps({
    modelValue: { type: Boolean, default: false },
    mode: { type: String, default: '' },
    group: { type: Object, default: null },
    groups: { type: Array, default: () => [] }
})
const emit = defineEmits(['update:modelValue', 'saved'])

const name = ref('')
const description = ref('')
const selectedGroupId = ref(null)

const databases = ref([])
const selectedDatabaseIds = ref([])
const selectAll = ref(false)
const loadingDatabases = ref(false)

const fetchDatabases = async () => {
    loadingDatabases.value = true
    try {
        const res = await fetch(API_GET_DATABASE(), { credentials: 'include' })
        if (!res.ok) {
            console.error('Failed to fetch databases', res.status)
            databases.value = []
            return
        }
        const json = await res.json()
        // API may return a paginated object { results: [...] } or an array or { database: [...] }
        if (Array.isArray(json)) databases.value = json
        else if (Array.isArray(json.results)) databases.value = json.results
        else if (Array.isArray(json.database)) databases.value = json.database
        else databases.value = []
        // if editing a team, preload selectedDatabaseIds from props.group.maindatabase (if present)
        if (props.mode === 'editTeam' && props.group && Array.isArray(databases.value)) {
            try {
                const parsed = typeof props.group.maindatabase === 'string' ? JSON.parse(props.group.maindatabase) : props.group.maindatabase
                if (Array.isArray(parsed)) {
                    const nums = parsed.map(x => Number(x))
                    selectedDatabaseIds.value = databases.value.filter(d => nums.includes(Number(d.id))).map(d => d.id)
                    selectAll.value = databases.value.length > 0 && selectedDatabaseIds.value.length === databases.value.length
                }
            } catch (e) {
                // ignore parse errors
            }
        }
    } catch (err) {
        console.error('Error fetching databases', err)
        databases.value = []
    } finally {
        loadingDatabases.value = false
    }
}

// toggle selectAll
watch(selectAll, (val) => {
    if (val) selectedDatabaseIds.value = databases.value.map(d => d.id)
    else selectedDatabaseIds.value = []
})

// when modal opens for team create/edit, fetch databases
watch(() => props.modelValue, (val) => {
    if (val && (props.mode === 'createTeam' || props.mode === 'editTeam')) {
        fetchDatabases()
    }
})

watch(() => props.modelValue, (val) => {
    if (val && props.mode === 'editGroup' && props.group) {
        name.value = props.group.group_name || ''
        description.value = props.group.description || ''
    }
    if (val && props.mode === 'createGroup') {
        name.value = ''
        description.value = ''
    }
    if (val && props.mode === 'createTeam') {
        // reset team form
        name.value = ''
        description.value = ''
        selectedGroupId.value = null
        selectedDatabaseIds.value = []
        selectAll.value = false
    }
})

watch(() => props.group, (g) => {
    if (props.modelValue && props.mode === 'editGroup' && g) {
        name.value = g.group_name || ''
        description.value = g.description || ''
    }
    if (props.modelValue && (props.mode === 'editTeam') && g) {
        name.value = g.name || ''
        description.value = g.maindatabase || ''
        selectedGroupId.value = g.user_group_id || g.user_group || null
        // preload selectedDatabaseIds if databases already loaded
        try {
            const parsed = typeof g.maindatabase === 'string' ? JSON.parse(g.maindatabase) : g.maindatabase
            if (Array.isArray(parsed) && databases.value.length) {
                const nums = parsed.map(x => Number(x))
                selectedDatabaseIds.value = databases.value.filter(d => nums.includes(Number(d.id))).map(d => d.id)
                selectAll.value = databases.value.length > 0 && selectedDatabaseIds.value.length === databases.value.length
            }
        } catch (e) {
            // ignore parse errors
        }
    }
})

const groupOptions = computed(() => {
    return Array.isArray(props.groups) ? props.groups.map(g => ({ label: g.group_name, value: g.id })) : []
})

function close() {
    emit('update:modelValue', false)
}

function onSave() {
    let payload = { id: props.group?.id, group_name: name.value, description: description.value }
    if (props.mode === 'createTeam' || props.mode === 'editTeam') {
        // serialize selected database ids as array of strings to match backend format
        const maindb = Array.isArray(selectedDatabaseIds.value) ? selectedDatabaseIds.value.map(String) : []
        payload = { id: props.group?.id, name: name.value, maindatabase: JSON.stringify(maindb), user_group_id: selectedGroupId.value }
    }
    emit('saved', { mode: props.mode, data: payload })
    emit('update:modelValue', false)
}
</script>

<style scoped>
.modal-body {
    min-height: 60vh;
    overflow: auto
}

</style>