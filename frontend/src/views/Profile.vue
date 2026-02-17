<template>
    <MainLayout>
        <div class="main-wrapper container-fluid-home py-3">
            <Breadcrumbs :items="[{ text: 'Home', to: '/' }, { text: 'Profile' }]" />

            <div class="row col-lg-12">
                <div class="col-lg-12">
                    <div class="card">
                        <div class="card-body" style="height: calc(100vh - 158px);">
                            <!-- Header -->
                            <div class="d-flex align-items-center" style="margin-bottom: 20px;">
                                <div class="d-flex align-items-center justify-content-center me-1"
                                    style="width:35px;height:35px;background-color: #D9E2F6;border-radius: 10px !important;">
                                    <i class="fa-solid fa-circle-user" style="color:#2b6cb0;font-size:18px"></i>
                                </div>
                                <h5 class="card-title mb-2 mt-1">Profile</h5>
                            </div>

                            <!-- Tabs -->
                            <ul class="nav nav-tabs mb-4">
                                <li class="nav-item">
                                    <a class="nav-link" :class="{ active: activeTab === 'personal' }" href="#" @click.prevent="activeTab = 'personal'">Personal info</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" :class="{ active: activeTab === 'password' }" href="#" @click.prevent="activeTab = 'password'">Password</a>
                                </li>
                            </ul>

                            <!-- Tab Content -->
                            <div class="tab-content">
                                <!-- Personal Info -->
                                <div v-if="activeTab === 'personal'" class="tab-pane fade show active">
                                    <div v-if="loading" class="text-center py-4">Loading...</div>
                                    <div v-else class="profile-info ps-2">
                                        <div class="row mb-3">
                                            <div class="col-md-1 fw-bold text-secondary">Username</div>
                                            <div class="col-md-11 text-profile-info">{{ userProfile.username }}</div>
                                        </div>
                                        <div class="row mb-3">
                                            <div class="col-md-1 fw-bold text-secondary">Full Name</div>
                                            <div class="col-md-11 text-profile-info">{{ userProfile.first_name }} {{ userProfile.last_name }}</div>
                                        </div>
                                        <div class="row mb-3">
                                            <div class="col-md-1 fw-bold text-secondary">Email</div>
                                            <div class="col-md-11 text-profile-info">{{ userProfile.email || '-' }}</div>
                                        </div>
                                        <div class="row mb-3">
                                            <div class="col-md-1 fw-bold text-secondary">Phone</div>
                                            <div class="col-md-11 text-profile-info">{{ userProfile.phone || '-' }}</div>
                                        </div>
                                        <div class="row mb-3">
                                            <div class="col-md-1 fw-bold text-secondary">Role</div>
                                            <div class="col-md-11 text-profile-info">
                                                <span :class="['role-badge', (['administrator', 'auditor', 'operator'].includes((userProfile.role || '').toLowerCase()) ? (userProfile.role || '').toLowerCase() : 'other')]">
                                                  {{ userProfile.role || '-' }}
                                                </span>
                                            </div>
                                        </div>
                                        <div class="row mb-3">
                                            <div class="col-md-1 fw-bold text-secondary">Group</div>
                                            <div class="col-md-11 text-profile-info">{{ userProfile.group_name || '-' }} </div> 
                                        </div>
                                        <div class="row mb-3">
                                            <div class="col-md-1 fw-bold text-secondary">Team</div>
                                            <div class="col-md-11 text-profile-info">{{ userProfile.team_name || '-' }} </div>
                                        </div>
                                        <div class="row mb-3">
                                            <div class="col-md-1 fw-bold text-secondary">Database Server</div>
                                            <div class="col-md-11 text-profile-info">{{ userProfile.db_name || '-' }}</div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Password -->
                                <div v-if="activeTab === 'password'" class="tab-pane fade show active">
                                    <form @submit.prevent="submitPasswordChange" class="col-md-6 ps-2">
                                        <div class="input-group mb-3" v-has-value>
                                            <input :type="showOldPass ? 'text' : 'password'" v-model="passwordForm.old_password" class="input" required>
                                            <button type="button" class="toggle-visibility" @click="showOldPass = !showOldPass">
                                                <i :class="showOldPass ? 'fa-regular fa-eye-slash' : 'fa-regular fa-eye'"></i>
                                            </button>
                                            <label class="title-label">Old Password</label>
                                        </div>
                                        <div class="input-group mb-3" v-has-value>
                                            <input :type="showNewPass ? 'text' : 'password'" v-model="passwordForm.new_password" class="input" required minlength="8">
                                            <button type="button" class="toggle-visibility" @click="showNewPass = !showNewPass">
                                                <i :class="showNewPass ? 'fa-regular fa-eye-slash' : 'fa-regular fa-eye'"></i>
                                            </button>
                                            <label class="title-label">New Password</label>
                                            <div v-show="errors.password" class="validate"><i class="fa-solid fa-circle-exclamation"></i> {{ typeof errors.password === 'string' ? errors.password : '' }}</div>
                                        </div>
                                        <div class="input-group mb-3" v-has-value>
                                            <input :type="showConfirmPass ? 'text' : 'password'" v-model="passwordForm.confirm_password" class="input" required>
                                            <button type="button" class="toggle-visibility" @click="showConfirmPass = !showConfirmPass">
                                                <i :class="showConfirmPass ? 'fa-regular fa-eye-slash' : 'fa-regular fa-eye'"></i>
                                            </button>
                                            <label class="title-label">Confirm New Password</label>
                                            <div v-if="passwordError" class="validate"><i class="fa-solid fa-circle-exclamation"></i> {{ passwordError }}</div>
                                        </div>
                                        <button class="btn btn-primary" type="button" @click="submit" style="font-size: 10px;">
                                            <i class="fas fa-save"></i>
                                          Save Changes
                                        </button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </MainLayout>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import MainLayout from '../layouts/MainLayout.vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'
import { useAuthStore } from '../stores/auth.store'
import { API_GET_USER_PROFILE } from '../api/paths'
import { getCsrfToken } from '../api/csrf'
import { showToast } from '../assets/js/function-all'



const authStore = useAuthStore()
const activeTab = ref('personal')
const loading = ref(false)
const submitting = ref(false)
const userProfile = ref({})

// Password form state
const passwordForm = reactive({ old_password: '', new_password: '', confirm_password: '' })
const passwordError = ref('')
const showOldPass = ref(false)
const showNewPass = ref(false)
const showConfirmPass = ref(false)

// validation state (similar to UserForm.vue)
const errors = reactive({ password: false, confirmPassword: false })
const hasError = ref(false)

// watch new password for length and update confirm match
watch(() => passwordForm.new_password, (val) => {
    if (!val || String(val).trim() === '') {
        errors.password = false
    } else if (String(val).length < 8) {
        errors.password = 'Password must be at least 8 characters long'
    } else {
        errors.password = false
    }
    // also validate confirm when present
    if (passwordForm.confirm_password && String(passwordForm.confirm_password).trim() !== '') {
        if (val !== passwordForm.confirm_password) {
            errors.confirmPassword = 'Passwords do not match'
            passwordError.value = 'Passwords do not match'
        } else {
            errors.confirmPassword = false
            passwordError.value = ''
        }
    }
    hasError.value = !!(errors.password || errors.confirmPassword)
})

// watch confirm password for match
watch(() => passwordForm.confirm_password, (val) => {
    if (!val || String(val).trim() === '') { errors.confirmPassword = false; passwordError.value = ''; hasError.value = !!errors.password; return }
    if (passwordForm.new_password !== val) {
        errors.confirmPassword = 'Passwords do not match'
        passwordError.value = 'Passwords do not match'
    } else {
        errors.confirmPassword = false
        passwordError.value = ''
    }
    hasError.value = !!(errors.password || errors.confirmPassword)
})

onMounted(() => { fetchProfile() })

async function fetchProfile() {
    const userId = authStore.user?.id
    if (!userId) return
    loading.value = true
    try {
        const res = await fetch(API_GET_USER_PROFILE(userId), { credentials: 'include' })
        if (res.ok) {
            const json = await res.json()
            const up = json.user_profile || {}
            const u = up.user || {}
            const team = up.team || {}
            const group = team.user_group || {}
            const role = json.selected_role_type || 'User'
            const db_name = (up.team.maindatabase_name || []).join(', ');


            userProfile.value = {
                username: u.username || '',
                first_name: u.first_name || '',
                last_name: u.last_name || '',
                email: u.email || '',
                phone: up.phone || '',
                group_name: group.group_name || '',
                team_name: team.name || '',
                role: role,
                db_name: db_name
            }
        }
    } catch (e) { console.error('Fetch profile error', e) } finally { loading.value = false }
}

// async function submitPasswordChange() {
//     passwordError.value = ''
//     if (passwordForm.new_password !== passwordForm.confirm_password) {
//         passwordError.value = 'New passwords do not match.'
//         return
//     }
//     if (passwordForm.new_password.length < 8) {
//         passwordError.value = 'Password must be at least 8 characters.'
//         return
//     }
//     submitting.value = true
//     try {
//         const csrfToken = getCsrfToken()
//         const res = await fetch(API_CHANGE_PASSWORD(), {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken || '' },
//             body: JSON.stringify({
//                 old_password: passwordForm.old_password,
//                 new_password: passwordForm.new_password,
//                 confirm_password: passwordForm.confirm_password
//             })
//         })
//         const json = await res.json()
//         if (res.ok && json.status === 'success') {
//             showToast('Password changed successfully', 'success')
//             passwordForm.old_password = ''; passwordForm.new_password = ''; passwordForm.confirm_password = ''
//         } else {
//             showToast(json.message || 'Failed to change password', 'error')
//         }
//     } catch (e) {
//         console.error('Change password error', e)
//         showToast('An error occurred', 'error')
//     } finally { submitting.value = false }
// }
</script>

<style scoped>
.nav-tabs .nav-link {
    color: #6c757d;
    cursor: pointer;
        font-size: 12px;
    margin-top: 4px;
}
.nav-tabs .nav-link.active {
    color: #416fd6;
    font-weight: 600;
    border-bottom: 2px solid #416fd6;
}
.profile-info .row {
    border-bottom: 1px solid #f0f0f0;
    padding-bottom: 12px;
    margin-bottom: 12px !important;
}
.profile-info .row:last-child {
    border-bottom: none;
}
.form-label {
    font-size: 12px;
}
.text-secondary {
    font-size: 12px;
}
.text-profile-info{
  font-size: 12px;
}

/* Password visibility toggle styles */
.input-group { position: relative; }
.input-group .input { padding-right: 40px; }
.input-group .toggle-visibility {
    position: absolute;
    right: 8px;
    top: 17px;
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
</style>