<template>
    <MainLayout>
        <div class="main-wrapper container-fluid-home py-3">
            <Breadcrumbs
                :items="[{ text: 'Home', to: '/' }, { text: 'User Management', to: '/user-management' }, { text: 'Add User' }]" />

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
                                                onclick="clearUserInfo()" style=" position:relative;">
                                                <i class="fas fa-eraser" style="margin-right: 6px;"></i> Clear
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                <div class="permissions-grid-1">
                                    <div class="input-group" v-has-value>
                                        <input required="" type="text" name="username"
                                            autocomplete="off" class="input" maxlength="50">
                                        <label class="title-label">Username</label>
                                    </div>
                                </div>

                                <div class="permissions-grid-2">
                                    <div class="input-group" v-has-value>
                                        <input required="" type="text" name="password"
                                            autocomplete="off" class="input" maxlength="50">
                                        <label class="title-label">Password</label>
                                    </div>
                                    <div class="input-group" v-has-value>
                                        <input required="" type="text" name="confirmPassword"
                                            autocomplete="off" class="input" maxlength="50">
                                        <label class="title-label">Confirm Password</label>
                                    </div>
                                    <div class="input-group" v-has-value>
                                        <input required="" type="text" name="firstName"
                                            autocomplete="off" class="input" maxlength="50">
                                        <label class="title-label">First Name</label>
                                    </div>
                                    <div class="input-group" v-has-value>
                                        <input required="" type="text" name="lastName"
                                            autocomplete="off" class="input" maxlength="50">
                                        <label class="title-label">Last Name</label>
                                    </div>
                                    <div class="input-group" v-has-value>
                                        <input required="" type="text" name="email"
                                            autocomplete="off" class="input" maxlength="50">
                                        <label class="title-label">Email</label>
                                    </div>
                                    <div class="input-group" v-has-value>
                                        <input required="" type="text" name="phone"
                                            autocomplete="off" class="input" maxlength="50">
                                        <label class="title-label">Phone</label>
                                    </div>
                                    <div class="input-group">
                                        <CustomSelect class="select-search " v-model="selectedGroupId"
                                            :options="groupOptions" placeholder="Select Group..." name="groupModal" />
                                    </div>
                                    <div class="input-group" :class="{ 'select-disabled': !selectedGroupId }">
                                        <CustomSelect class="select-search" v-model="selectedTeamId"
                                            :options="teamOptions" placeholder="Select Team..." name="teamModal" />
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

                                <div class="role-cards" id="roleCards">
                                    <label class="role-card">
                                        <input type="checkbox" name="role" value="administrator">
                                        <div class="role-icon"><i class="fas fa-crown"></i></div>
                                        <div class="role-name">Administrator</div>
                                        <div class="role-desc">Full system access</div>
                                    </label>
                                    <label class="role-card">
                                        <input type="checkbox" name="role" value="auditor">
                                        <div class="role-icon"><i class="fas fa-clipboard-check"></i></div>
                                        <div class="role-name">Auditor</div>
                                        <div class="role-desc">Read & audit access</div>
                                    </label>
                                    <label class="role-card">
                                        <input type="checkbox" name="role" value="operator">
                                        <div class="role-icon"><i class="fas fa-headset"></i></div>
                                        <div class="role-name">Operator</div>
                                        <div class="role-desc">Standard operations</div>
                                    </label>
                                </div>

                                <div class="custom-role-row" style="display: flex; gap: 12px; align-items: stretch;">
                                    <div class="custom-dropdown" id="otherRoleDropdown" style="flex: 1;">
                                        <div class="dropdown-selected">
                                            <span class="dropdown-text">Select Custom Role</span>
                                            <i class="fas fa-chevron-down dropdown-arrow"></i>
                                        </div>
                                        <div class="dropdown-options">
                                            <!-- Options will be loaded from localStorage -->
                                        </div>
                                        <input type="hidden" name="otherRole" id="otherRoleInput">
                                    </div>
                                    <button class="customize-btn" type="button" onclick="clearCustomRole()"
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
                                        <button type="button" class="btn-role btn-secondary" onclick="resetDatabase()"
                                            style="margin-right: 6px">
                                            <i class="fas fa-undo"></i>
                                            Reset to Default
                                        </button>
                                        <button class="customize-btn" type="button" onclick="clearDatabaseScope()">
                                            <i class="fas fa-eraser" style="margin-right: 6px;"></i> Clear
                                        </button>
                                    </div>
                                </div>

                                <div class="database-grid">
                                    <label class="db-card">
                                        <input type="checkbox" value="all">
                                        <span class="db-checkbox"></span>
                                        <span class="db-name">All Databases</span>
                                    </label>
                                    <label class="db-card" v-for="db in databases" :key="db.id">
                                        <input type="checkbox" :value="db.id">
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
                            <div class="d-flex align-items-start justify-content-between" style="margin-bottom: 18px;">
                                <div class="d-flex align-items-center">
                                    <div class="d-flex align-items-center justify-content-center me-1"
                                        style="width:35px;height:35px;background-color: #D9E2F6;border-radius: 10px !important;">
                                        <i class="fas fa-key" style="color:#2b6cb0;font-size:18px"></i>
                                    </div>
                                    <h5 class="card-title mb-2 mt-1">Permissions</h5>
                                </div>
                                <div class="d-flex align-items-center">
                                    <div>
                                        <button class="customize-btn" type="button" id="clearUserInfoBtn"
                                            onclick="clearUserInfo()" style=" position:relative;">
                                            <i class="fas fa-eraser" style="margin-right: 6px;"></i> Clear
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div class="permissions-grid" id="permissionsGrid">
                                <label class="permission-item disabled">
                                    <input type="checkbox" data-permission="system-access" disabled>
                                    <span class="perm-checkbox"></span>
                                    <span class="perm-label">System Access</span>
                                </label>
                                <label class="permission-item disabled">
                                    <input type="checkbox" data-permission="access-audio-records" disabled>
                                    <span class="perm-checkbox"></span>
                                    <span class="perm-label">Access Audio Records</span>
                                </label>
                                <label class="permission-item disabled">
                                    <input type="checkbox" data-permission="audio-playback" disabled>
                                    <span class="perm-checkbox"></span>
                                    <span class="perm-label">Audio Playback</span>
                                </label>
                                <label class="permission-item disabled">
                                    <input type="checkbox" data-permission="download-audio" disabled>
                                    <span class="perm-checkbox"></span>
                                    <span class="perm-label">Download Audio</span>
                                </label>
                                <label class="permission-item disabled">
                                    <input type="checkbox" data-permission="manage-system-users" disabled>
                                    <span class="perm-checkbox"></span>
                                    <span class="perm-label">Manage System Users</span>
                                </label>
                                <label class="permission-item disabled">
                                    <input type="checkbox" data-permission="add-users" disabled>
                                    <span class="perm-checkbox"></span>
                                    <span class="perm-label">Add Users</span>
                                </label>
                                <label class="permission-item disabled">
                                    <input type="checkbox" data-permission="edit-users" disabled>
                                    <span class="perm-checkbox"></span>
                                    <span class="perm-label">Edit Users</span>
                                </label>
                                <label class="permission-item disabled">
                                    <input type="checkbox" data-permission="role-settings" disabled>
                                    <span class="perm-checkbox"></span>
                                    <span class="perm-label">Role Settings</span>
                                </label>
                                <label class="permission-item disabled">
                                    <input type="checkbox" data-permission="group-settings" disabled>
                                    <span class="perm-checkbox"></span>
                                    <span class="perm-label">Group Settings</span>
                                </label>
                                <label class="permission-item disabled">
                                    <input type="checkbox" data-permission="team-settings" disabled>
                                    <span class="perm-checkbox"></span>
                                    <span class="perm-label">Team Settings</span>
                                </label>
                                <label class="permission-item disabled">
                                    <input type="checkbox" data-permission="access-system-logs" disabled>
                                    <span class="perm-checkbox"></span>
                                    <span class="perm-label">Access System Logs</span>
                                </label>
                                <label class="permission-item disabled">
                                    <input type="checkbox" data-permission="access-audit-logs" disabled>
                                    <span class="perm-checkbox"></span>
                                    <span class="perm-label">Access Audit Logs</span>
                                </label>
                                <label class="permission-item disabled">
                                    <input type="checkbox" data-permission="export-reports" disabled>
                                    <span class="perm-checkbox"></span>
                                    <span class="perm-label">Export Reports</span>
                                </label>
                            </div>

                            <div class="button-group">
                                <button class="btn btn-primary" type="button" onclick="createUser()">
                                    <i class="fas fa-check"></i>
                                    Create User
                                </button>
                                <button class="btn btn-secondary" onclick="window.location.href='user-management.html'">
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

import MainLayout from '../layouts/MainLayout.vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'
import TableTemplate from '../components/TableTemplate.vue'
import CustomSelect from '../components/CustomSelect.vue'
import { registerRequest } from '../utils/pageLoad'
import { API_GROUP_INDEX, API_GET_DATABASE } from '../api/paths'

import '../assets/css/add-user.css'

const loading = ref(false)
const selectedGroupId = ref(null)

const groups = ref([])
const teams = ref([])
const groupTeamsMap = ref({})
const databases = ref([])

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
        value: g.id || g.user_group_id || g.user_group,
        label: g.group_name || g.group || g.name || g.user_group || ''
    }))
})


const selectedTeamId = ref(null)

const teamOptions = computed(() => {
    const gid = selectedGroupId.value
    if (!gid) return []
    return teams.value
        .filter(t => (t.user_group_id || t.user_group || t.user_group_id_id || t.user_group_id) == gid)
        .map(t => ({ value: t.id || t.user_team_id || t.id, label: t.name || t.team_name || t.name }))
})

// clear team when group changes
watch(selectedGroupId, (val) => {
    selectedTeamId.value = null
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
            // fetch database list
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
onMounted(() => {
    fetchData()
})
</script>

<style scoped>
.customize-btn {
    margin-left: auto;
    padding: 6px 16px;
    background: transparent;
    border: 1px solid #416fd6;
    border-radius: 20px;
    color: #416fd6;
    font-size: 13px;
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

/* Ensure page/container scrolls with content and grids wrap instead of overflowing */
.main-content {
    flex: 1 1 auto;
    padding: 83.5px 0px 16px 0px;
}
.main-wrapper {
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    /* keep the page scrollable within the viewport minus header area */
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

/* Make individual db/permission items shrink and wrap neatly */
.db-card,
.permission-item {
    box-sizing: border-box;
    flex: 0 1 220px;
    min-width: 180px;
}

/* Ensure cards don't hide overflow inside */
.card {
    overflow: visible;
}
</style>