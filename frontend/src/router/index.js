import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Role from '../views/Role.vue'
import { useAuthStore } from '../stores/auth.store'

const routes = [
	{ path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
	{ path: '/', name: 'Home', component: Home },
	{ path: '/user-management', name: 'UserManagement', component: () => import('../views/UserManagement.vue') },
	{ path: '/configuration/role', name: 'role', component: Role },
	{ path: '/configuration/group', name: 'Group', component: () => import('../views/GroupAndTeam.vue') },
	{ path: '/configuration/users', name: 'Users', component: () => import('../views/Users.vue') },
	{ path: '/user-management/add', name: 'AddUser', component: () => import('../views/AddUser.vue') },
	{ path: '/user-management/edit/:id', name: 'EditUser', component: () => import('../views/EditUser.vue') },
	{ path: '/profile', name: 'Profile', component: () => import('../views/Profile.vue') },
	{ path: '/logs/system', name: 'SystemLogs', component: () => import('../views/UserLog.vue') },
	{ path: '/logs/audit', name: 'AuditLogs', component: () => import('../views/UserLog.vue') },
	{ path: '/setting/column/audio-record', name: 'SettingColumnAudioRecord', component: () => import('../views/SetColumnAudioRecord.vue') },

	{ path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('../views/NotFound.vue') },

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
