import { getRuntime } from './runtimeConfig'
import { getCookie } from '../assets/js/function-all'
import { API_GET_CSRF } from './paths'

let _csrfToken = null

export function getCsrfToken() {
  if (_csrfToken) return _csrfToken
  try {
    return getCookie('csrftoken')
  } catch (e) {
    return null
  }
}

export function setCsrfToken(t) {
  _csrfToken = t
}

export async function ensureCsrf() {
  if (_csrfToken) return _csrfToken
  try {
    const r = await fetch(API_GET_CSRF(), { credentials: 'include' })
    if (!r.ok) return null
    const j = await r.json()
    const token = (j && j.csrfToken) ? j.csrfToken : getCookie('csrftoken')
    _csrfToken = token
    return _csrfToken
  } catch (e) {
    return getCookie('csrftoken')
  }
}

export default {
  ensureCsrf,
  getCsrfToken,
  setCsrfToken
}
