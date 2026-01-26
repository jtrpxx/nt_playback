const pending = new Set()

export function registerRequest(promise) {
  if (!promise || typeof promise.then !== 'function') return
  pending.add(promise)
  promise.finally(() => {
    pending.delete(promise)
    if (pending.size === 0) {
      window.dispatchEvent(new Event('pageload:idle'))
    }
  })
}

export function whenIdle() {
  return new Promise((resolve) => {
    if (pending.size === 0) return resolve()
    const handler = () => {
      window.removeEventListener('pageload:idle', handler)
      resolve()
    }
    window.addEventListener('pageload:idle', handler)
  })
}
