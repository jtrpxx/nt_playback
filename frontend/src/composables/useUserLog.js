import { ref, reactive, computed, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth.store'
import { registerRequest } from '../utils/pageLoad'
import { API_GET_USER_ALL, API_GET_LOG_USER } from '../api/paths'
import { exportTableToFormat } from '../assets/js/function-all'

export function useUserLog() {
    const route = useRoute()
    const authStore = useAuthStore()

    const searchQuery = ref('')
    let searchTimeout = null
    let userFilterTimeout = null

    const exportOpen = ref(false)
    const exportWrap = ref(null)
    
    const perPageOptions = [50, 100, 500, 1000]
    const perPage = ref(50)
    const currentPage = ref(1)
    
    const filters = reactive({ name: '', action: '', start_date: '', end_date: '' })
    const userOptions = ref([])
    const actionOptions = ref([
        { label: 'All Actions', value: 'all' },
        { label: 'Change User Status', value: 'Change User Status' },
        { label: 'Create Columns', value: 'Create Columns' },
        { label: 'Create Config Group', value: 'Create Config Group' },
        { label: 'Create Config Team', value: 'Create Config Team' },
        { label: 'Create Custom Role', value: 'Create Custom Role' },
        { label: 'Create Favorite', value: 'Create Favorite' },
        { label: 'Create Favorite Search', value: 'Create Favorite Search' },
        { label: 'Created User', value: 'Created User' },
        { label: 'Delete Config Group', value: 'Delete Config Group' },
        { label: 'Delete Config Team', value: 'Delete Config Team' },
        { label: 'Delete Custom Role', value: 'Delete Custom Role' },
        { label: 'Delete Favorite', value: 'Delete Favorite' },
        { label: 'Delete User', value: 'Delete User' },
        { label: 'Edit Favorite', value: 'Edit Favorite' },
        { label: 'Login', value: 'Login' },
        { label: 'Play audio', value: 'Play audio' },
        { label: 'Save file', value: 'Save file' },
        { label: 'Update Config Group', value: 'Update Config Group' },
        { label: 'Update Config Team', value: 'Update Config Team' },
        { label: 'Update Custom Role', value: 'Update Custom Role' },
        { label: 'Update Favorite Search', value: 'Update Favorite Search' },
        { label: 'Update User', value: 'Update User' }
    ])

    const startInput = ref(null)
    const endInput = ref(null)
    const searchInputRef = ref(null)

    const perWrap = ref(null)
    const perDropdownOpen = ref(false)

    const records = ref([])
    const totalItems = ref(0)
    const loading = ref(false)
    const expanded = ref(new Set())

    const columns = [
        { key: 'index', label: '#', isIndex: true, width: '5%' },
        { key: 'username', label: 'Username', width: '15%' },
        { key: 'full_name', label: 'Full Name', width: '15%' },
        { key: 'action', label: 'Action', width: '5%' },
        { key: 'status', label: 'Status', width: '5%' },
        { key: 'detail', label: 'Description', tooltip: true, width: '20%', },
        { key: 'ip_address', label: 'IP Address', width: '10%' },
        { key: 'timestamp', label: 'Timestamp', width: '10%', },
        { key: 'client_type', label: 'Client type', width: '15%' }
    ]

    const type = computed(() => {
        const p = route.path || ''
        if (p === '/logs/system') return 'system'
        if (p === '/logs/audit') return 'audit'
        return 'user'
    })

    const cardTitle = computed(() => {
        const p = route.path || ''
        if (p === '/logs/system') return 'System log'
        if (p === '/logs/audit') return 'Audit log'
        return 'User Logs'
    })

    const requiredPermission = computed(() => {
        const p = route.path || ''
        if (p === '/logs/system') return 'System Logs'
        if (p === '/logs/audit') return 'Audit Logs'
        return 'User Logs'
    })

    const canView = computed(() => authStore.hasPermission(requiredPermission.value))

    const totalPages = computed(() => Math.max(1, Math.ceil(totalItems.value / perPage.value)))
    const startIndex = computed(() => (currentPage.value - 1) * perPage.value)
    const paginatedRecords = computed(() => records.value)

    const fetchData = async () => {
        loading.value = true
        try {
            if (!canView.value) {
                loading.value = false
                records.value = []
                totalItems.value = 0
                return
            }
            const start = (currentPage.value - 1) * perPage.value
            const params = new URLSearchParams()
            params.set('draw', 1)
            params.set('start', start)
            params.set('length', perPage.value)
            params.set('search[value]', searchQuery.value || '')
            if (filters.name && filters.name !== 'all') params.set('name', filters.name)
            if (filters.action && filters.action !== 'all') params.set('action', filters.action)
            if (filters.start_date) params.set('start_date', filters.start_date)
            if (filters.end_date) params.set('end_date', filters.end_date)

            const res = await fetch(`${API_GET_LOG_USER(type.value)}?${params.toString()}`, { credentials: 'include' })
            if (!res.ok) throw new Error('Failed to fetch')
            const json = await res.json()
            records.value = json.data || json.user_management || []
            totalItems.value = json.recordsFiltered ?? json.recordsTotal ?? (Array.isArray(records.value) ? records.value.length : 0)
        } catch (e) {
            console.error('fetchData error', e)
        } finally {
            loading.value = false
        }
    }

    const fetchUsers = async () => {
        if (!canView.value) return
        try {
            const params = new URLSearchParams()
            params.set('draw', 1)
            params.set('start', 0)
            params.set('length', 1000)
            params.set('type', type.value)
            if (filters.action && filters.action !== 'all') params.set('action', filters.action)
            if (filters.start_date) params.set('start_date', filters.start_date)
            if (filters.end_date) params.set('end_date', filters.end_date)
            const res = await fetch(`${API_GET_USER_ALL()}?${params.toString()}`, { credentials: 'include' })
            if (!res.ok) throw new Error('Failed to fetch users')
            const json = await res.json()
            const list = json.data || []
            const opts = [{ label: 'All Users', value: 'all' }]
            for (const p of list) {
                const u = p.user ? p.user : p
                const uname = u?.username || ''
                const fullname = `${u?.first_name || ''} ${u?.last_name || ''}`.trim()
                const label = fullname ? `${uname} (${fullname})` : uname
                opts.push({ label, value: uname })
            }
            userOptions.value = opts
        } catch (e) {
            console.error('fetchUsers error', e)
        }
    }

    const onTyping = () => {
        currentPage.value = 1
        if (searchTimeout) clearTimeout(searchTimeout)
        searchTimeout = setTimeout(() => {
            fetchData()
            searchTimeout = null
        }, 450)
    }

    const setPerPage = (opt) => {
        perPage.value = opt
        perDropdownOpen.value = false
    }

    const changePage = async (p) => {
        if (p < 1) p = 1
        if (p > totalPages.value) p = totalPages.value
        currentPage.value = p
        await fetchData()
    }

    const onDocClick = (e) => {
        if (perWrap.value && !perWrap.value.contains(e.target)) perDropdownOpen.value = false
        if (exportWrap.value && !exportWrap.value.contains(e.target)) exportOpen.value = false
    }

    const onRowEdit = (row) => { console.log('edit row', row) }
    const onRowDelete = (row) => { console.log('delete row', row) }

    const clearSearchQuery = () => {
        searchQuery.value = ''
        if (searchTimeout) { clearTimeout(searchTimeout); searchTimeout = null }
        currentPage.value = 1
        fetchData()
        nextTick(() => {
            if (searchInputRef.value && typeof searchInputRef.value.focus === 'function') searchInputRef.value.focus()
        })
    }

    const resetFilters = () => {
        try {
            filters.name = []
            filters.action = []
            filters.start_date = ''
            filters.end_date = ''

            if (startInput.value && startInput.value._flatpickrInstance) {
                startInput.value._flatpickrInstance.clear()
            }
            if (endInput.value && endInput.value._flatpickrInstance) {
                endInput.value._flatpickrInstance.clear()
            }

            currentPage.value = 1
            fetchUsers()
            fetchData()
        } catch (e) {
            console.error('resetFilters error', e)
        }
    }

    const toggleExport = () => {
        exportOpen.value = !exportOpen.value
    }

    const onExportFormat = (format) => {
        if (!canView.value) return
        exportTableToFormat(format, cardTitle.value, {
            rows: paginatedRecords.value || [],
            columns: columns || [],
            startIndex: startIndex.value || 0,
            fileNamePrefix: cardTitle.value
        })
    }

    watch(filters, () => {
        if (userFilterTimeout) clearTimeout(userFilterTimeout)
        userFilterTimeout = setTimeout(() => {
            fetchUsers()
            currentPage.value = 1
            fetchData()
            userFilterTimeout = null
        }, 350)
    }, { deep: true })

    onMounted(() => {
        registerRequest(fetchData())
        fetchUsers()
        document.addEventListener('click', onDocClick)
    })

    onBeforeUnmount(() => {
        document.removeEventListener('click', onDocClick)
    })

    const state = {
        authStore,
        searchQuery,
        exportOpen,
        exportWrap,
        perPageOptions,
        perPage,
        currentPage,
        filters,
        userOptions,
        actionOptions,
        startInput,
        endInput,
        searchInputRef,
        perWrap,
        perDropdownOpen,
        records,
        totalItems,
        loading,
        expanded,
        columns,
        type,
        cardTitle,
        requiredPermission,
        canView,
        totalPages,
        startIndex,
        paginatedRecords
    }

    const actions = {
        onTyping,
        setPerPage,
        changePage,
        onRowEdit,
        onRowDelete,
        clearSearchQuery,
        resetFilters,
        toggleExport,
        onExportFormat,
        fetchData,
        fetchUsers
    }

    return {
        ...state,
        ...actions
    }
}
