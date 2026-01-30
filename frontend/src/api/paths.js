import { getRuntime } from './runtimeConfig'

const ENV_API_BASE = import.meta.env.VITE_API_BASE || 'http://172.27.96.1:8000'

export const getApiBase = () => getRuntime('VITE_API_BASE', ENV_API_BASE)

// หน้า Home
export const API_HOME_INDEX = () => `${getApiBase()}/api/home/index/`

export const API_AUDIO_LIST = () => `${getApiBase()}/api/audio/list/`

// หน้า Login
export const API_LOGIN = () => `${getApiBase()}/login/`

// หน้า Role
export const API_INDEX_ROLE = () => `${getApiBase()}/api/role/index/`

export const API_GET_DETAILS_ROLE = () => `${getApiBase()}/api/role/get-details/`

// หน้า  Group
export const API_GROUP_INDEX = () => `${getApiBase()}/api/group/index/`
export const API_TEAM_INDEX = () => `${getApiBase()}/api/team/index/`
export const API_GET_TEAM_BY_GROUP = (groupId) => `${getApiBase()}/api/group/get/team-by-group/${groupId}/`
export const API_GET_DATABASE = () => `${getApiBase()}/api/get/database/`

// หน้า  User Management
export const API_GET_USER = () => `${getApiBase()}/api/get/user/`
export const API_USER_MANAGEMENT_CHANGE_STATUS = (id) => `${getApiBase()}/api/user-management/change-status/${id}/`

// หน้า log user
export const API_GET_LOG_USER = (type) => `${getApiBase()}/api/log-user/get-log/${type}/`

// หน้า Add User
export const API_GET_ALL_ROLES_PERMISSIONS = () => `${getApiBase()}/api/add-user/get-all-roles-permissions/`
// Get user profile for edit (expects user_id)
export const API_GET_USER_PROFILE = (id) => `${getApiBase()}/api/user-management/get-profile/${id}/`
