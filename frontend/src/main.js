import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useAuthStore } from './stores/auth.store.js'
import App from './App.vue'
import router from './router'
import { loadRuntimeConfig } from './api/runtimeConfig'
import { ensureCsrf } from './api/csrf'

//JS
import './assets/js/flatpickr.min.js'
import './assets/js/jquery-3.6.0.min.js'

import flatpickrDirective from './directives/flatpickr.js'
import hasValueDirective from './directives/hasValue.js'

// css
import './assets/css/base.css'
import './assets/css/bootstrap.min.css'
import './assets/css/components.css'
import './assets/css/all.min.css'
import './assets/css/flatpickr.min.css'
import './assets/css/datatable.css'




;(async () => {
	await loadRuntimeConfig()
	const app = createApp(App)
	const pinia = createPinia()
	app.use(pinia)
	app.use(router)
	app.directive('flatpickr', flatpickrDirective)
	app.directive('has-value', hasValueDirective)
	// fetch permissions on startup if user present
	try {
		const auth = useAuthStore()
		if (auth.user) await auth.fetchPermissions()
	} catch (e) {
		console.error('Error fetching permissions on startup', e)
	}

	// ensure CSRF token is available for subsequent POST requests
	try {
		await ensureCsrf()
	} catch (e) {
		console.warn('ensureCsrf failed on startup', e)
	}

	// Wrap global fetch to detect backend redirects to login (301/302 or /login?next=)
	try {
		const originalFetch = window.fetch.bind(window)
		window.fetch = async (...args) => {
			const response = await originalFetch(...args)
			try {
				const respUrl = (response && response.url) ? String(response.url) : ''
				const location = (response && response.headers) ? (response.headers.get('Location') || response.headers.get('location') || '') : ''
				const isRedirectStatus = response && (response.status === 301 || response.status === 302)
				const looksLikeLogin = respUrl.includes('/login') || location.includes('/login') || respUrl.includes('/login?next=') || location.includes('/login?next=')
				const auth = useAuthStore()
				if (isRedirectStatus || looksLikeLogin || (response && (response.status === 401 || response.status === 403))) {
					try {
						// call centralized logout if available
						if (auth && typeof auth.logout === 'function') {
							await auth.logout()
						} else {
							try { auth.clear && auth.clear() } catch (e) {}
							try { router.push('/login') } catch (e) { try { window.location.href = '/login' } catch (ee) {} }
						}
					} catch (e) {
						try { window.location.href = '/login' } catch (ee) {}
					}
				}
			} catch (e) { /* ignore parse errors */ }
			return response
		}
	} catch (e) { console.warn('Failed to wrap fetch', e) }

	app.mount('#app')
})()