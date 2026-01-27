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
                                        :options="groupOptions" placeholder="Select Group..." name="groupModal" />
                                </div>
                            </div>
                        </div>

                        <div class="col-lg-12">
                            <div class="form-group-modal">
                                <div class="form-group-modal">
                                    <div class="input-group" v-has-value>
                                        <input required="" v-model="description" type="text" name="teamNameModal"
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
                                <label
                                    style="font-size: 14px; font-weight: normal; cursor: pointer; display: flex; align-items: center; gap: 5px; margin-bottom: 0; margin-left: auto;">
                                    <input type="checkbox" id="selectAllDatabases"> All database
                                </label>
                            </div>
                            <div class="permissions-grid-2" id="DatabseSeverGrid">
                                <!-- {% if database %}
                                    {% for database in database %}
                                    <div style="margin-bottom: 8px;">
                                        <label style="display: flex;align-items: center;gap: 10px;padding: 12px 14px;background: #fff;border: 1px solid #e2e8f0;border-radius: 10px;cursor: pointer;transition: all 0.2s;">
                                            <input type="checkbox" name="database_ids" value="{{ database.id }}">
                                            <span>{{ database.database_name }}</span>
                                        </label>
                                    </div>
                                    {% endfor %}
                                {% endif %} -->
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
                    <div class="permissions-grid-2" id="teamGrid">
                        <div class="col-lg-12">
                            <div class="form-group-modal">
                                <div class="input-group" v-has-value>
                                    <input required="" v-model="name" type="text" name="teamNameModal"
                                        autocomplete="off" class="input" maxlength="30">
                                    <label class="title-label">Team name</label>
                                </div>
                            </div>
                        </div>

                        <div class="col-lg-12">
                            <div class="form-group-modal">
                                <label class="form-label-modal">Group</label>
                                <div class="input-group">
                                    <CustomSelect v-model="selectedGroupId" :options="groupOptions"
                                        placeholder="Select group" name="groupSelectEdit" />
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

</template>
<script setup>
import { watch, computed, ref } from 'vue'
import CustomSelect from './CustomSelect.vue'
import { API_GET_DATABASE } from '../api/paths'

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

watch(() => props.modelValue, (val) => {
    if (val && props.mode === 'editGroup' && props.group) {
        name.value = props.group.group_name || ''
        description.value = props.group.description || ''
    }
    if (val && props.mode === 'createGroup') {
        name.value = ''
        description.value = ''
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
        payload = { id: props.group?.id, name: name.value, maindatabase: description.value, user_group_id: selectedGroupId.value }
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