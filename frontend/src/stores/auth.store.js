import { defineStore } from 'pinia'
import { ref } from 'vue'
import { API_LOGIN } from '../api/paths'
import { ensureCsrf } from '../api/csrf'

export const useAuthStore = defineStore('auth', () => {
	// Initialize state from localStorage to enable persistence
	const user = ref(JSON.parse(localStorage.getItem('user')))
	// console.log('Initial user from localStorage:', user.value)
	const token = ref(localStorage.getItem('token'))

	function setUser(payload) {
		user.value = payload
		if (payload) {
			localStorage.setItem('user', JSON.stringify(payload))
		} else {
			localStorage.removeItem('user')
		}
	}

	function setToken(t) {
		token.value = t
		if (t) {
			localStorage.setItem('token', t)
		} else {
			localStorage.removeItem('token')
		}
	}

	function clear() {
		// Clear from both state and localStorage
		setUser(null)
		setToken(null)
	}

	const fullName = () => {
		if (!user.value) return null
		// Adjusted to prioritize username as it's what the new backend provides
		return user.value.username || null
	}

	async function login(username, password) {
		try {
			// Corrected URL to match the new backend endpoint at /login/
			const response = await fetch(API_LOGIN(), {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ username, password })
			})

			if (!response.ok) {
				throw new Error(`Login failed with status: ${response.status}`)
			}

			const data = await response.json()
			setToken(data.access)
			setUser({ username: data.username })
			// Ensure CSRF token is fetched and cached after successful login
			try { await ensureCsrf() } catch (e) {}
			return true
		} catch (error) {
			console.error('Login error:', error)
			clear()
			return false
		}
	}

	return { user, token, setUser, setToken, clear, fullName, login }
})
