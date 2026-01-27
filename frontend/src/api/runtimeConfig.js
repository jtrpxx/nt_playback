let _runtimeConfig = null

export async function loadRuntimeConfig() {
  try {
    const res = await fetch('/config.json', { cache: 'no-store' })
    if (!res.ok) {
      _runtimeConfig = {}
      return _runtimeConfig
    }
    _runtimeConfig = await res.json()
  } catch (e) {
    _runtimeConfig = {}
  }
  return _runtimeConfig
}

export function getRuntime(key, fallback) {
  if (_runtimeConfig && Object.prototype.hasOwnProperty.call(_runtimeConfig, key)) {
    return _runtimeConfig[key]
  }
  return fallback
}

export default {
  loadRuntimeConfig,
  getRuntime,
}
