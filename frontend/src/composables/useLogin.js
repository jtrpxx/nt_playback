import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth.store'
import { useRouter } from 'vue-router'
import { showToast } from '../assets/js/function-all'

export function useLogin() {
  const router = useRouter()
  const authStore = useAuthStore()

  const passwordVisible = ref(false)
  const form = reactive({
    username: '',
    password: '',
    rememberMe: false
  })

  const handleLogin = async () => {
    const success = await authStore.login(form.username, form.password)
    if (success) {
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
      try { showToast('Login failed. Please check your username and password.', 'error') } catch (e) { }
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

  const state = {
    passwordVisible,
    form
  }

  const actions = {
    handleLogin
  }

  return {
    ...state,
    ...actions
  }
}