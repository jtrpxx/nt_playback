import { defineStore } from 'pinia'
import { ref } from 'vue'
import { API_LOGIN, API_HOME_INDEX } from '../api/paths'
import { ensureCsrf } from '../api/csrf'

export const useAuthStore = defineStore('auth', () => {
	// Initialize state from localStorage to enable persistence
	const user = ref(JSON.parse(localStorage.getItem('user')))
	// console.log('Initial user from localStorage:', user.value)
	const token = ref(localStorage.getItem('token'))
    const permissions = ref(JSON.parse(localStorage.getItem('permissions') || '[]'))

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
			// store whatever user info the login returned (may include id)
			if (data && data.username) setUser({ username: data.username, id: data.id || null })
			// ensure we have profile (id) and permissions
			// fetch permissions after login
			try { await fetchPermissions() } catch (e) { console.error('fetchPermissions', e) }
			// Ensure CSRF token is fetched and cached after successful login
			try { await ensureCsrf() } catch (e) {}
			return true
		} catch (error) {
			console.error('Login error:', error)
			clear()
			return false
		}
	}


	async function fetchPermissions() {
		try {
			// ensure we have user id by fetching home index (contains user_profile)
			try {
				const profileResp = await fetch(API_HOME_INDEX(), { credentials: 'include' })
				if (profileResp.ok) {
					const pjson = await profileResp.json()
					if (pjson && pjson.user_profile) {
						const up = pjson.user_profile
						// merge id into user state
						if (up.id) {
							const current = user.value || {}
							setUser(Object.assign({}, current, { id: up.id, username: up.username }))
						}
					}
				}
			} catch (e) {
				console.error('fetch user profile failed', e)
			}

			const resp = await fetch('/api/my-permissions/', { credentials: 'include' })
			if (!resp.ok) return
			const payload = await resp.json()
			const perms = payload.permissions || []
			permissions.value = perms
			localStorage.setItem('permissions', JSON.stringify(perms))
		} catch (e) {
			console.error('Error fetching permissions', e)
		}
	}

	function hasPermission(name) {
		// root user bypass
		try {
			if (user.value && user.value.id === 1) return true
		} catch (e) {}
		if (!permissions.value) return false
		return permissions.value.includes(name)
	}

	return { user, token, permissions, setUser, setToken, clear, fullName, login, fetchPermissions, hasPermission }
})
