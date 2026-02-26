// Vue 3 directive to attach flatpickr in range mode and write "start - end" to target
// Usage: v-flatrangepickr="{ target: obj, key: 'range', options: { ... }, onChange: fn }"
// Arg form: v-flatrangepickr:range="filters"
export default {
  mounted(el, binding) {
    const fp = (typeof window !== 'undefined' && window.flatpickr) || (typeof flatpickr !== 'undefined' && flatpickr)
    if (!fp) return

    const raw = binding.value
    const value = (raw && typeof raw === 'object') ? raw : {}
    const target = (binding.arg && raw && typeof raw === 'object') ? raw : (value.target || null)
    const key = binding.arg ? binding.arg : value.key
    // Default: date range only (no time shown). Backend times will be synthesized as 00:00 / 23:59.
    const opts = Object.assign({ mode: 'range', enableTime: false, dateFormat: 'Y-m-d', time_24hr: true, defaultHour: 0, defaultMinute: 0 }, value.options || {})
    const userOnChange = (typeof raw === 'function') ? raw : value.onChange

    const instance = fp(el, opts)

    if (instance && instance.config && Array.isArray(instance.config.onChange)) {
      instance.config.onChange.push((selectedDates) => {
        let displayOut = ''
        let displayStart = ''
        let displayEnd = ''
        // Backend-ready timestamps
        let backendStart = ''
        let backendEnd = ''

        if (Array.isArray(selectedDates) && selectedDates.length >= 2) {
          displayStart = instance.formatDate(selectedDates[0], 'Y-m-d')
          displayEnd = instance.formatDate(selectedDates[1], 'Y-m-d')
          displayOut = `${displayStart} - ${displayEnd}`
          backendStart = `${displayStart} 00:00`
          backendEnd = `${displayEnd} 23:59`
        } else if (selectedDates && selectedDates.length === 1) {
          displayStart = instance.formatDate(selectedDates[0], 'Y-m-d')
          displayEnd = displayStart
          displayOut = displayStart
          backendStart = `${displayStart} 00:00`
          backendEnd = `${displayEnd} 23:59`
        } else {
          displayOut = ''
        }

        if (target && key) {
          try { target[key] = displayOut } catch (e) {}
          try { target[`${key}_start`] = backendStart } catch (e) {}
          try { target[`${key}_end`] = backendEnd } catch (e) {}
        }
        try { el.value = displayOut } catch (e) {}

        if (typeof userOnChange === 'function') {
          try { userOnChange(selectedDates, { display: displayOut, start: backendStart, end: backendEnd }) } catch (e) {}
        }
      })
    }

    // store instance for cleanup
    el._flatpickrRangeInstance = instance
  },

  beforeUnmount(el) {
    try {
      if (el._flatpickrRangeInstance && typeof el._flatpickrRangeInstance.destroy === 'function') el._flatpickrRangeInstance.destroy()
    } catch (e) {}
    delete el._flatpickrRangeInstance
  }
}
