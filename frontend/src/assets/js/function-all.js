export function getCookie(name) {
    if (!name || typeof document === 'undefined') return null
    const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')
    return v ? v.pop() : null
}
export function showToast(titleOrMessage, maybeTypeOrMessage = '', maybeType) {
  try {
    const types = ['success', 'error', 'info', 'warning']
    let title = ''
    let message = ''
    let type = 'success'

    if (maybeType !== undefined) {
      // called as showToast(title, message, type)
      title = String(titleOrMessage || '')
      message = String(maybeTypeOrMessage || '')
      type = String(maybeType || 'success')
    } else {
      if (types.includes(String(maybeTypeOrMessage))) {
        // called as showToast(message, type)
        title = ''
        message = String(titleOrMessage || '')
        type = String(maybeTypeOrMessage)
      } else {
        // called as showToast(title, message) or showToast(message)
        title = String(titleOrMessage || '')
        message = String(maybeTypeOrMessage || '')
        type = 'success'
      }
    }

    const el = document.createElement('div')
    el.className = `toast ${type || ''}`

    const icon = document.createElement('div')
    icon.className = 'icon'
    // ensure glyph color is white for visibility against colored backgrounds
    icon.style.color = '#fff'
    // small vertical nudge to better center glyphs
    // mark icon as decorative for screen readers
    icon.setAttribute('aria-hidden', 'true')
    // set glyph per type; use Font Awesome for error for a consistent X mark
    const glyphMap = {
      success: { char: '✓' },
      error: { fa: 'fa-solid fa-xmark' },
      info: { char: 'ℹ' },
      warning: { char: '!' }
    }
    const map = glyphMap[type] || glyphMap.success
    if (map.fa) {
      icon.innerHTML = `<i class="${map.fa}" aria-hidden="true" style="margin-top: 2px;"></i>`
    } else {
      icon.textContent = map.char
    }

    const content = document.createElement('div')
    content.className = 'content'
    if (title) {
      const t = document.createElement('div')
      t.className = 'title'
      t.textContent = title
      content.appendChild(t)
    }
    if (message) {
      const m = document.createElement('div')
      m.className = 'message'
      m.textContent = message
      content.appendChild(m)
    }

    el.appendChild(icon)
    el.appendChild(content)
    // insert at top so newest is on top
    const first = document.body.querySelector('.toast')
    if (first) document.body.insertBefore(el, first)
    else document.body.appendChild(el)

    // show toast and set up timed hide/remove with progress bar and hover-pause
    requestAnimationFrame(() => el.classList.add('show'))

    const hideDelay = 3200 // ms until hide
    const removeDelay = 3800 // ms until DOM removal

    // add progress bar element
    const progressWrap = document.createElement('div')
    progressWrap.className = 'toast-progress'
    const progressBar = document.createElement('div')
    progressBar.className = 'toast-progress-bar'
    progressWrap.appendChild(progressBar)
    el.appendChild(progressWrap)

    let remaining = hideDelay
    let progStart = Date.now()
    let progDuration = remaining
    let hideTimeout = null
    let removeTimeout = null
    let rafId = null

    function rafLoop() {
      const now = Date.now()
      const elapsed = now - progStart
      const pct = Math.max(0, Math.min(100, ((progDuration - elapsed) / progDuration) * 100))
      progressBar.style.width = pct + '%'
      if (elapsed < progDuration) rafId = requestAnimationFrame(rafLoop)
    }

    function startTimers(ms) {
      // set up hide and remove timeouts relative to now
      hideTimeout = setTimeout(() => {
        el.classList.remove('show')
      }, ms)
      const removeAfter = ms + (removeDelay - hideDelay)
      removeTimeout = setTimeout(() => { try { el.remove() } catch (e) {} }, removeAfter)
      // start progress
      progStart = Date.now()
      progDuration = Math.max(1, ms)
      if (rafId) cancelAnimationFrame(rafId)
      rafId = requestAnimationFrame(rafLoop)
    }

    // begin
    startTimers(remaining)

    // pause on hover: clear timers and stop RAF
    el.addEventListener('mouseenter', () => {
      if (hideTimeout) { clearTimeout(hideTimeout); hideTimeout = null }
      if (removeTimeout) { clearTimeout(removeTimeout); removeTimeout = null }
      if (rafId) { cancelAnimationFrame(rafId); rafId = null }
      const now = Date.now()
      const elapsed = now - progStart
      remaining = Math.max(0, progDuration - elapsed)
    })

    // resume on mouseleave
    el.addEventListener('mouseleave', () => {
      startTimers(remaining)
    })
  } catch (e) { console.warn('showToast failed', e) }
}

export function notification (title, text, icon, showCancelButton){

}