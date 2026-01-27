import { getRuntime } from './runtimeConfig'

const ENV_API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

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

