import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import { useAuthStore } from '../stores/auth.store'

const routes = [
	{ path: '/', name: 'Home', component: Home },
	{ path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
	{ path: '/users', name: 'Users', component: () => import('../views/Users.vue').catch(() => ({ template: '<div>Users Page</div>' })) },
	{ path: '/dashboard', name: 'Dashboard', component: () => import('../views/Dashboard.vue').catch(() => ({ template: '<div>Dashboard Page</div>' })) },
	{ path: '/profile', name: 'Profile', component: () => import('../views/Profile.vue').catch(()=>({ template: '<div>Profile</div>' })) },
]

const router = createRouter({
	history: createWebHistory(),
	routes,
})

router.beforeEach((to, from, next) => {
	const authStore = useAuthStore()
	const isAuthenticated = !!authStore.token

	if (to.name !== 'Login' && !isAuthenticated) {
		next({ name: 'Login' })
	} else if (to.name === 'Login' && isAuthenticated) {
		next({ name: 'Home' })
	} else {
		next()
	}
})

export default router
