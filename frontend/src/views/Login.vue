<template>
  <div class="login-root" style="background-color: #F9FAFB;">
    <div class="login-card">

    <div class="login-header">
      <img src="/src/assets/images/logo-nichtel.png" alt="logo" class="logo" />
      <h1 class="app-title">NT Audio Search</h1>
      <div class="app-sub">Centralized Search and Playback System</div>
    </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-left">
          <div class="input-group" style="margin-bottom: 12.2px;" v-has-value>
            <input v-model="form.username" required type="text" name="username" autocomplete="off" class="input"
              maxlength="30">
            <label class="title-label">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                stroke="#64748b" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"
                focusable="false">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>Username
            </label>
          </div>

          <div class="input-group" v-has-value>
            <input v-model="form.password" required :type="passwordVisible ? 'text' : 'password'" name="password"
              autocomplete="off" class="input" maxlength="30">
            <button type="button" class="toggle-visibility" @click="passwordVisible = !passwordVisible"
              aria-label="Toggle password visibility">
              <i :class="passwordVisible ? 'fa-regular fa-eye-slash' : 'fa-regular fa-eye'"></i>
            </button>
            <label class="title-label">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                stroke="#64748b" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"
                focusable="false">
                <rect x="3" y="11" width="18" height="10" rx="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>Password
            </label>
          </div>

          <div class="checkbox-left">
            <input type="checkbox" id="remember" v-model="form.rememberMe" />
            <label for="remember">Remember</label>
          </div>
        </div>

        <div class="form-bottom">
          <button type="submit" class="btn-submit"><i class="fa-solid fa-arrow-right-to-bracket"></i> Login</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth.store'
import { useRouter } from 'vue-router'
import { showToast } from '../assets/js/function-all'

const router = useRouter()
const authStore = useAuthStore()

const passwordVisible = ref(false)
const form = reactive({
  username: '',
  password: '',
  rememberMe: false
})

const handleLogin = async () => {
  const result = await authStore.login(form.username, form.password)
  if (result && result.success) {
    // persist or remove saved credentials based on rememberMe
    try {
      if (form.rememberMe) {
        localStorage.setItem('remember_credentials', JSON.stringify({ username: form.username, password: form.password }))
      } else {
        localStorage.removeItem('remember_credentials')
      }
    } catch (e) { }
    try { showToast(`Welcome! ${authStore.user?.username || ''}`, 'success') } catch (e) { }
    router.push('/')
  } else {
    try { showToast(result.message || 'Login failed. Please check your username and password.', 'error') } catch (e) { }
  }
}

onMounted(() => {
  try {
    const raw = localStorage.getItem('remember_credentials')
    if (raw) {
      const obj = JSON.parse(raw)
      if (obj && obj.username) form.username = obj.username
      if (obj && obj.password) form.password = obj.password
      form.rememberMe = true
    }
  } catch (e) { }
})
</script>

<style scoped>
.login-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 16px;
}

.login-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  margin-bottom: 28px
}

.logo {
  width: 64px;
  height: auto
}

.app-title {
  font-size: 22px;
  margin: 0;
  color: #0f172a
}

.app-sub {
  font-size: 13px;
  color: #64748b
}

.login-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
  padding: 28px
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 18px
}

.form-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%
}

.checkbox-left {
  display: flex;
  align-items: center;
  position: relative;
  margin-top: 6px
}

.checkbox-left input[type="checkbox"] {
  position: absolute;
  opacity: 0;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
  border: 0;
  padding: 0;
  margin: 0
}

.checkbox-left label {
  position: relative;
  padding-left: 16px;
  cursor: pointer;
  color: #1e293b;
  font-weight: 500;
  user-select: none;
  font-size: 10px;
}

.checkbox-left label::before {
  content: '';
  position: absolute;
  left: 1px;
  top: 50%;
  transform: translateY(-50%);
  width: 12px;
  height: 12px;
  border-radius: 4px;
  border: 1px solid #cbd5e1;
  background: #fff;
  box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.02);
  transition: all .12s ease
}

.checkbox-left input[type="checkbox"]:checked+label::before {
  background: #2563eb;
  border-color: #2563eb
}

.checkbox-left label::after {
  content: '';
  position: absolute;
  left: 5px;
  top: 50%;
  transform: translateY(-50%) rotate(45deg);
  width: 4px;
  height: 8px;
  border: solid transparent;
  border-width: 0 2px 2px 0;
  opacity: 0;
  transition: opacity .12s ease
}

.checkbox-left input[type="checkbox"]:checked+label::after {
  border-color: #fff;
  opacity: 1
}

.checkbox-left input[type="checkbox"]:focus+label::before {
  box-shadow: 0 0 0 5px rgba(37, 99, 235, 0.12)
}

@media (max-width:600px) {
  .checkbox-left label {
    font-size: 13px;
    padding-left: 22px
  }

  .checkbox-left label::before {
    width: 14px;
    height: 14px
  }

  .checkbox-left label::after {
    left: 4px
  }
}

.btn-submit {
  display: block;
  margin: 0 auto;
  padding: 14px 32px;
  min-width: 260px;
  max-width: 100%;
  width: auto;
  font-size: 16px;
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 25px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.18);
  transition: transform .12s ease, box-shadow .12s ease;
}

.btn-submit:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(37, 99, 235, 0.22);
}

.input-group {
  position: relative;
  width: 300px;
}

.input {
  width: 100%;
  padding: 12px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #fff;
  border-radius: 25px;
}

.title-label svg {
  width: 16px;
  height: 16px;
  margin-right: 8px;
  vertical-align: middle;
  color: inherit;
}

.toggle-visibility {
  position: absolute;
  right: 8px;
  top: 3px;
  color: #64748b;
  border: none;
  background: transparent;
  cursor: pointer
}

@media (max-width:600px) {
  .login-card {
    padding: 20px
  }

  .input-group {
    width: 100%
  }

  .btn-submit {
    min-width: unset;
    padding: 12px 18px;
    width: 100%
  }
}
</style>
