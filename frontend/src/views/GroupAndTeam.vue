<template>
    <MainLayout>
        <div class="main-wrapper container-fluid-home py-3" style="display:flex; flex-direction:column; height:100%;">
            <Breadcrumbs :items="[{ text: 'Home', to: '/' }, { text: 'Group & Team Configuration' }]" />
            <div class="row row-container">
                <div class="col-lg-6">
                    <div class="card">
                        <div class="card-body">
                            <div class="d-flex align-items-start justify-content-between" style="margin-bottom: 6px">
                                <div class="d-flex align-items-center">
                                    <div class="d-flex align-items-center justify-content-center me-1"
                                        style="width: 35px; height: 35px; background-color: #d9e2f6; border-radius: 10px !important">
                                        <i class="fa-solid fa-user-group" style="color: #2b6cb0; font-size: 18px"></i>
                                    </div>
                                    <h5 class="card-title mb-2 mt-1">Group List</h5>
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
                                        Add New Group
                                    </button>
                                </div>
                            </div>
                            <!-- Content Group here. -->
                            <div class="custom-roles-list" id="customRolesList">
                                <template v-if="loading">
                                    <div class="container-overlay" style="height: 487px;">
                                        <div class="overlay-box">Loading...</div>
                                    </div>
                                </template>
                                <template v-else>
                                    <div v-if="groups.length">
                                        <div v-if="filteredGroups.length" class="group-list">
                                            <div v-for="group in filteredGroups" :key="group.id" :class="['group-card-item', { active: selectedGroupId === group.id }]"
                                                @click.stop="selectGroup(group)">
                                                <div class="group-card-main">
                                                    <div class="group-card-header">
                                                        <span class="group-card-title">{{ group.group_name }}</span>
                                                        <span class="group-card-group-badge">
                                                            <template
                                                                v-if="groupTeamsMap[group.id] && groupTeamsMap[group.id].length">
                                                                <span v-for="(t, idx) in groupTeamsMap[group.id]"
                                                                    :key="t.id">
                                                                    {{ t.name }}<span
                                                                        v-if="idx < groupTeamsMap[group.id].length - 1">,
                                                                    </span>
                                                                </span>
                                                            </template>
                                                            <template v-else>
                                                                Unassigned
                                                            </template>
                                                        </span>
                                                    </div>
                                                    <div class="group-card-desc">
                                                        {{ group.description || 'No description provided for this group.' }}
                                                    </div>
                                                </div>

                                                <div class="group-card-actions">
                                                    <button class="group-edit-btn" @click.stop="openEditGroup(group.id)">
                                                        Click to edit
                                                    </button>
                                                    <button type="button" class="group-delete-btn" @click.stop="deleteGroup(group.id)">
                                                        <i class="fas fa-trash" style="font-size: 12px;"></i>
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                        <div v-else class="empty-state">
                                            <i class="fa-solid fa-dove"></i>
                                            <p>This group not found.</p>
                                        </div>
                                    </div>

                                    <div v-else class="empty-state">
                                        <i class="fas fa-user-plus"></i>
                                        <p>No groups yet. Click "Add New Group" to create one.</p>
                                    </div>
                                </template>
                            </div>

                        </div>
                    </div>
                </div>

                <div class="col-lg-6">
                    <div class="card">
                        <div class="card-body">
                            <div class="d-flex align-items-start justify-content-between" style="margin-bottom: 6px">
                                <div class="d-flex align-items-center">
                                    <div class="d-flex align-items-center justify-content-center me-1"
                                        style="width: 35px; height: 35px; background-color: #d9e2f6; border-radius: 10px !important">
                                        <i class="fa-solid fa-people-group" style="color: #2b6cb0; font-size: 18px"></i>
                                    </div>
                                    <h5 class="card-title mb-2 mt-1">Team List</h5>
                                </div>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <div class="search-group" style="width:260px; position:relative;">
                                        <i class="fa-solid fa-magnifying-glass search-icon"></i>
                                        <input v-model="teamSearchQuery" type="text"
                                            class="form-control form-control-sm search-input"
                                            placeholder="Search..." @input="onTypingTeam" @keyup.enter="onSearchTeam" />
                                    </div>
                                    <button class="btn-role btn-primary btn-sm" id="addTeamBtn"
                                        @click.stop="openCreateTeam">
                                        <i class="fas fa-plus"></i>
                                        Add New Team
                                    </button>
                                </div>
                            </div>
                            <!-- Content for Team here. -->
                            <div class="custom-roles-list" id="customTeamList">
                                <div v-if="!selectedGroupId" class="empty-state">
                                    <i class="fa-solid fa-dove"></i>
                                    <p>Select a group to view teams.</p>
                                </div>

                                <template v-else>
                                    <template v-if="loading">
                                        <div class="container-overlay" style="height: 487px;">
                                            <div class="overlay-box">Loading...</div>
                                        </div>
                                    </template>
                                    <template v-else>
                                        <div v-if="filteredTeams.length" class="group-list">
                                            <div v-for="team in filteredTeams" :key="team.id" class="group-card-item">
                                                <div class="group-card-main">
                                                    <div class="group-card-header">
                                                        <span class="group-card-title">{{ team.name }}</span>
                                                        <span class="group-card-team-badge">{{ selectedGroupName || team.group_name }}</span>
                                                    </div>
                                                </div>

                                                <div class="group-card-actions">
                                                    <button class="group-edit-btn" @click.stop="openEditTeam(team.id)">
                                                        Click to edit
                                                    </button>
                                                    <button type="button" class="group-delete-btn" @click.stop="deleteTeam(team.id)">
                                                        <i class="fas fa-trash" style="font-size: 12px;"></i>
                                                    </button>
                                                </div>
                                            </div>
                                        </div>

                                        <div v-else>
                                            <div v-if="groupTeamsMap[selectedGroupId] && groupTeamsMap[selectedGroupId].length" class="empty-state">
                                                <i class="fa-solid fa-dove"></i>
                                                <p>This team not found.</p>
                                            </div>
                                            <div v-else class="empty-state">
                                                <i class="fas fa-user-plus"></i>
                                                <p>No teams for this group.</p>
                                            </div>
                                        </div>
                                    </template>
                                </template>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </MainLayout>
    <ModalGroup v-model="showGroupModal" :mode="selectedModalMode" :group="editGroup" :groups="groups" @saved="onGroupSaved" />

</template>

<script setup>
import MainLayout from '../layouts/MainLayout.vue';
import Breadcrumbs from '../components/Breadcrumbs.vue'
import ModalGroup from '../components/ModalGroup.vue'
import { ref, onMounted, computed } from 'vue'
import { registerRequest } from '../utils/pageLoad'
import { API_GROUP_INDEX, API_TEAM_INDEX, API_GET_TEAM_BY_GROUP } from '../api/paths'

const searchQuery = ref('')
const teamSearchQuery = ref('')
const selectedGroupId = ref(null)

const groups = ref([])
const teams = ref([])
const groupTeamsMap = ref({})
const loading = ref(false)

const showGroupModal = ref(false)
const selectedModalMode = ref('create')
const editGroup = ref(null)

const filteredGroups = computed(() => {
    const q = (searchQuery.value || '').toLowerCase().trim()
    if (!q) return groups.value
    return groups.value.filter(g => (g.group_name || '').toLowerCase().includes(q))
})

const buildGroupTeamsMap = (groupList, teamList) => {
    const map = {}
    for (const g of groupList) map[g.id] = []
    for (const t of teamList) {
        const gid = t.user_group_id || t.user_group || t.user_group_id_id || t.user_group_id
        if (gid != null && map[gid]) map[gid].push(t)
    }
    return map
}

const fetchIndexGroup = async () => {
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
        } catch (error) {
            console.error('Error fetching groups:', error)
        } finally {
            loading.value = false
        }
    })()
    registerRequest(task)
    await task
}

const filteredTeams = computed(() => {
    const gid = selectedGroupId.value
    if (!gid) return []
    const list = Array.isArray(groupTeamsMap.value[gid]) ? groupTeamsMap.value[gid] : []
    const q = (teamSearchQuery.value || '').toLowerCase().trim()
    if (!q) return list
    return list.filter(t => (t.name || '').toLowerCase().includes(q))
})

const selectedGroupName = computed(() => {
    const gid = selectedGroupId.value
    if (!gid) return ''
    const g = groups.value.find(x => (x.id == gid))
    return g ? g.group_name : ''
})


onMounted(() => {
    fetchIndexGroup()
})

function onTyping() {
    // debounce could be added later
}

function onSearch() {
    // no-op since computed handles filtering
}

const loadingTeamsByGroup = ref(false)

function selectGroup(group) {
    // Toggle: deselect if same group clicked
    if (selectedGroupId.value === group.id) {
        selectedGroupId.value = null
        teamSearchQuery.value = ''
        return
    }

    selectedGroupId.value = group.id
    teamSearchQuery.value = ''

    if (Array.isArray(groupTeamsMap.value[group.id]) && groupTeamsMap.value[group.id].length) {
        return
    }

    registerRequest(task)
}

function openCreateGroup() {
    selectedModalMode.value = 'createGroup'
    showGroupModal.value = true
}

function openEditGroup(id) {
    const g = groups.value.find(x => x.id == id)
    editGroup.value = g ? { id: g.id, group_name: g.group_name, description: g.description } : { id }
    selectedModalMode.value = 'editGroup'
    showGroupModal.value = true
}

function deleteGroup(id) {
    console.log('deleteGroup', id)
}

function onTypingTeam() {
    // debounce could be added later
}

function onSearchTeam() {
    // no-op since computed handles filtering
}

function openCreateTeam() {
    selectedModalMode.value = 'createTeam'
    showGroupModal.value = true
}

function openEditTeam(id) {
    const t = teams.value.find(x => x.id == id)
    if (t) {
        editGroup.value = {
            id: t.id,
            name: t.name,
            maindatabase: t.maindatabase,
            user_group_id: t.user_group_id || t.user_group || null,
            group_name: groups.value.find(g => g.id == (t.user_group_id || t.user_group))?.group_name || ''
        }
    } else {
        editGroup.value = { id }
    }
    selectedModalMode.value = 'editTeam'
    showGroupModal.value = true
}

function deleteTeam(id) {
    console.log('deleteTeam', id)
}

function onGroupSaved(payload) {
    // payload: { mode, data }
    if (!payload || !payload.data) return
    const { mode, data } = payload
    if (mode === 'editGroup') {
        const idx = groups.value.findIndex(g => g.id == data.id)
        if (idx !== -1) {
            groups.value[idx] = { ...groups.value[idx], group_name: data.group_name, description: data.description }
            // update groupTeamsMap key if name changed (team badges)
        }
    } else if (mode === 'createGroup') {
        // naive local insert; real app should use backend response
        const newId = data.id || Date.now()
        groups.value.unshift({ id: newId, group_name: data.group_name, description: data.description, status: 1 })
        groupTeamsMap.value = { ...groupTeamsMap.value, [newId]: [] }
    }
}
</script>

<style scoped>
.row-container {
    flex: 1 1 auto;
}
.container-fluid-home {
    padding-right: calc(var(--bs-gutter-x) * 0.95);
    box-sizing: border-box;
}
.group-list {
    max-height: calc(100vh - 260px);
    margin-top: 3px;
    padding-right: 4px;
}

.group-card-desc {
    font-size: 10px;
}

.group-card-item.active {
    border-color: #416fd6;
    box-shadow: 0 10px 20px rgba(65, 111, 214, 0.1);
    transform: translateY(-2px);
}

.custom-roles-list::-webkit-scrollbar-track {
    margin-top: 4px;
}
</style>
