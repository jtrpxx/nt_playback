<template>
  <MainLayout>
    <div class="main-wrapper-container">
      <Breadcrumbs :items="[{ text: 'Home', to: '/' }, { text: 'Role & Permissions Configuration' }]" />
      <div class="card">
        <div class="card-body">
          <div class="d-flex align-items-start justify-content-between" style="margin-bottom: 6px">
            <div class="d-flex align-items-center">
              <div class="d-flex align-items-center justify-content-center me-1"
                style="width: 35px; height: 35px; background-color: #d9e2f6; border-radius: 10px !important">
                <i class="fas fa-shield-alt" style="color: #2b6cb0; font-size: 18px"></i>
              </div>
              <h5 class="card-title mb-2 mt-1">Base Roles</h5>
            </div>
          </div>

          <div class="roles-grid" id="baseRolesGrid">
            <div class="role-box" data-role="1" @click.stop="openEditRole(1, 'base')">
              <div class="role-box-header">
                <div class="role-box-icon">
                  <i class="fas fa-crown"></i>
                </div>
                <span class="role-box-badge">Click to edit</span>
              </div>
              <div class="role-box-name">Administrator</div>
              <div class="role-box-desc">Full system access</div>
            </div>
            <div class="role-box" data-role="2" @click.stop="openEditRole(2, 'base')">
              <div class="role-box-header">
                <div class="role-box-icon">
                  <i class="fas fa-clipboard-check"></i>
                </div>
                <span class="role-box-badge">Click to edit</span>
              </div>
              <div class="role-box-name">Auditor</div>
              <div class="role-box-desc">Read & audit access</div>
            </div>
            <div class="role-box" data-role="3" @click.stop="openEditRole(3, 'base')">
              <div class="role-box-header">
                <div class="role-box-icon">
                  <i class="fas fa-headset"></i>
                </div>
                <span class="role-box-badge">Click to edit</span>
              </div>
              <div class="role-box-name">Operator/Agent</div>
              <div class="role-box-desc">Standard operations</div>
            </div>
          </div>
        </div>
      </div>

      <div class="card card-custom-role">
        <div class="card-body">
          <div class="d-flex align-items-start justify-content-between" style="margin-bottom: 6px">
            <div class="d-flex align-items-center">
              <div class="d-flex align-items-center justify-content-center me-1"
                style="width: 35px; height: 35px; background-color: #d9e2f6; border-radius: 10px !important">
                <i class="fas fa-users-cog" style="color: #2b6cb0; font-size: 18px"></i>
              </div>
              <h5 class="card-title mb-2 mt-1">Custom Roles</h5>
            </div>
            <div style="display: flex; align-items: center; gap: 10px">
              <div data-v-2dc54a20="" class="search-group" style="width: 260px; position: relative">
                <i data-v-2dc54a20="" class="fa-solid fa-magnifying-glass search-icon"></i>
                <input data-v-2dc54a20="" v-model="searchQuery" type="text" class="form-control form-control-sm search-input"
                  placeholder="Search..." fdprocessedid="lf0zjn" />
              </div>
              <button type="button" class="btn-role btn-primary btn-sm" id="addRoleBtn" @click.stop="openCreateRole">
                <i class="fas fa-plus"></i>
                Add New Role
              </button>
            </div>
          </div>

          <div class="custom-roles-list" id="customRolesList">
            <div v-if="loading" class="empty-state" style="display:flex;align-items:center;justify-content:center;padding:24px;">
              <div>Loading...</div>
            </div>
            <template v-else>
              <div v-if="filteredRoles.length" class="custom-roles-container">
                  <div v-for="role in filteredRoles" :key="role.id" class="custom-role-item"
                    @click.stop="openEditRole(role.id, 'edit')">
                  <div class="custom-role-info">
                    <div class="custom-role-name">{{ role.name }}</div>
                    <span class="custom-role-perms">Permissions</span>
                  </div>
                  <div class="custom-role-actions">
                    <span class="role-box-badge">Click to edit</span>
                    <button type="button" class="group-delete-btn" @click.stop="deleteCustomRole(role.id)">
                      <i class="fas fa-trash" style="font-size: 12px;"></i>
                    </button>
                  </div>
                </div>
              </div>
              <div v-else class="empty-state">
                <i class="fa-solid fa-dove"></i>
                <p v-if="!userPermissionOther.length">No custom roles yet. Click "Add New Role" to create one.</p>
                <p v-else>No roles found matching your search.</p>
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
  <ModalConfiguration v-model="showBaseRoleModal" :role-id="selectedBaseRoleId" :role-name="selectedBaseRoleName" :mode="selectedModalMode" @role-created="onRoleCreated" @role-updated="onRoleUpdated" />
</template>
<script setup>
import MainLayout from '../layouts/MainLayout.vue';
import Breadcrumbs from '../components/Breadcrumbs.vue'
import { ref, onMounted, computed } from 'vue'
import { registerRequest } from '../utils/pageLoad'

import ModalConfiguration from '../components/ModalConfiguration.vue'
import { API_INDEX_ROLE, API_DELETE_ROLE } from '../api/paths'
import { getCookie, showToast } from '../assets/js/function-all'
import { ensureCsrf, getCsrfToken } from '../api/csrf'

const userPermissionOther = ref([])
const loading = ref(true)
const showBaseRoleModal = ref(false)
const selectedBaseRoleId = ref(null)
const selectedBaseRoleName = ref('')
const selectedModalMode = ref('base')
const searchQuery = ref('')

const filteredRoles = computed(() => {
  const q = (searchQuery.value || '').toLowerCase().trim()
  if (!q) return userPermissionOther.value
  return userPermissionOther.value.filter(r => (r.name || '').toLowerCase().includes(q))
})

const fetchIndexRoles = async () => {
  const task = (async () => {
    loading.value = true
    try {
      const res = await fetch(API_INDEX_ROLE(), { credentials: 'include' })
      if (!res.ok) {
        console.error('Failed to fetch roles', res.status)
        return
      }
      const json = await res.json()
      // prefer `user_permission_other` field, fallback to empty array
      userPermissionOther.value = Array.isArray(json.user_permission_other) ? json.user_permission_other : []
    } catch (e) {
      console.error('fetchIndexRoles error', e)
    }
    finally {
      loading.value = false
    }
  })()
  registerRequest(task)
  await task
}

onMounted(() => {
  fetchIndexRoles()
})

function openEditRole(id, mode = 'base') {
  console.log('openEditRole', id, mode)
  selectedBaseRoleId.value = id
  selectedModalMode.value = mode
  if (id === 1) selectedBaseRoleName.value = 'Edit Administrator'
  else if (id === 2) selectedBaseRoleName.value = 'Edit Auditor'
  else if (id === 3) selectedBaseRoleName.value = 'Edit Operator/Agent'
  else selectedBaseRoleName.value = 'Edit Role'
  showBaseRoleModal.value = true
}

function openCreateRole() {
  selectedBaseRoleId.value = null
  selectedBaseRoleName.value = 'Create New Role'
  selectedModalMode.value = 'create'
  showBaseRoleModal.value = true
}

async function deleteCustomRole(id) {
  try {
    if (!id) return
    const swalLib = (typeof Swal !== 'undefined' && Swal) || (typeof window !== 'undefined' && (window.Swal || window.Sweetalert2 || window.SweetAlert || window.sweetAlert))
    let result
    if (swalLib && typeof swalLib.fire === 'function') {
      result = await swalLib.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
      })
      if (!result || !result.isConfirmed) return
    } else {
      const ok = window.confirm("Are you sure? This action cannot be undone.")
      if (!ok) return
    }

    await ensureCsrf()
    const csrfToken = getCsrfToken()
    const url = API_DELETE_ROLE(id)
    const res = await fetch(url, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || ''
      },
      body: JSON.stringify({ role_id: id })
    })
    const j = res.ok ? await res.json() : null
    if (res.ok && j && j.status === 'success') {
      showToast(j.message || 'Deleted successfully', 'success')
      try {
        const idx = (userPermissionOther.value || []).findIndex(r => String(r.id) === String(id))
        if (idx !== -1) userPermissionOther.value.splice(idx, 1)
      } catch (e) {
        console.warn('List removal failed', e)
      }
    } else {
      showToast((j && j.message) || 'Failed to delete role', 'error')
    }
  } catch (e) {
    console.error('deleteCustomRole error', e)
    showToast('Failed to delete role', 'error')
  }
}

function onRoleCreated(role) {
  try {
    if (!role || !role.id) return
    // add to the beginning of the custom roles list
    userPermissionOther.value = [{ id: role.id, name: role.name, type: role.type || 'role_other' }].concat(userPermissionOther.value || [])
  } catch (e) { console.error('onRoleCreated handler error', e) }
}

function onRoleUpdated(role) {
  try {
    if (!role || !role.id) return
    const idx = (userPermissionOther.value || []).findIndex(r => String(r.id) === String(role.id))
    if (idx !== -1) {
      userPermissionOther.value[idx].name = role.name
    } else {
      // if not present, add to the start
      userPermissionOther.value = [{ id: role.id, name: role.name, type: role.type || 'role_other' }].concat(userPermissionOther.value || [])
    }
  } catch (e) { console.error('onRoleUpdated handler error', e) }
}

</script>

<style scoped>

</style>
