import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
	const user = ref(null)
	const token = ref(null)

	function setUser(payload) {
		user.value = payload
	}

	function setToken(t) {
		token.value = t
	}

	function clear() {
		user.value = null
		token.value = null
	}

	const fullName = () => {
		if (!user.value) return null
		const parts = [user.value.firstName, user.value.lastName].filter(Boolean)
		return parts.join(' ') || user.value.username || null
	}

	async function login(username, password) {
		try {
			// TODO: ตรวจสอบ URL นี้กับ urls.py ใน Django ของคุณ
			// ถ้าใช้ SimpleJWT ปกติจะเป็น http://localhost:8000/api/token/
			const response = await fetch('http://localhost:8000/api/token/', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ username, password })
			})

			if (!response.ok) throw new Error('Login failed')

			const data = await response.json()
			setToken(data.access || data.token) // ปรับตาม key ที่ backend ส่งมา
			return true
		} catch (error) {
			console.error('Login error:', error)
			return false
		}
	}

	return { user, token, setUser, setToken, clear, fullName, login }
})
