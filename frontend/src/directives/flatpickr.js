// Vue 3 directive to attach flatpickr to inputs in a reusable way
// Usage: v-flatpickr="{ target: filters, key: 'from', options: { ... }, onChange: fn }"
//
// Thai:
// directive นี้สำหรับผูก flatpickr เข้ากับ input ใน Vue 3 แบบ reusable
// ตัวอย่างการใช้งาน: v-flatpickr="{ target: filters, key: 'from', options:{}, onChange: fn }"

export default {
  mounted(el, binding) {
    const fp = (typeof window !== 'undefined' && window.flatpickr) || (typeof flatpickr !== 'undefined' && flatpickr)
    if (!fp) return

    const raw = binding.value

    // Determine binding mode:
    // 1) object form: v-flatpickr="{ target: obj, key: 'from', options:{}, onChange: fn }"
    // 2) arg form: v-flatpickr:from="filters"  --> binding.arg === 'from', binding.value === filters (object)
    // 3) function form: v-flatpickr="(dates, str) => ..."  --> binding.value is a function called on change
    //
    // Thai:
    // ตรวจสอบรูปแบบการผูกที่ directive รองรับ:
    // 1) object form: ส่ง object ที่มี target/key/options/onChange
    // 2) arg form: ใช้ argument เป็นชื่อ property เช่น v-flatpickr:from="filters" (สั้นและแนะนำ)
    // 3) function form: ส่งฟังก์ชันเป็น binding เพื่อรับ event เมื่อวันที่เปลี่ยน
    const value = (raw && typeof raw === 'object') ? raw : {}
    const target = (binding.arg && raw && typeof raw === 'object') ? raw : (value.target || null)
    const key = binding.arg ? binding.arg : value.key
    const opts = Object.assign({ enableTime: true, dateFormat: 'Y-m-d H:i', time_24hr: true, defaultHour: 0, defaultMinute: 0 }, value.options || {})
    const userOnChange = (typeof raw === 'function') ? raw : value.onChange

    const instance = fp(el, opts)

    if (instance && instance.config && Array.isArray(instance.config.onChange)) {
      // Track whether the current value has been explicitly applied by the user
      let applied = !!(el && el.value)

      // create a small action bar appended to flatpickr's calendar container
      try {
        const actions = document.createElement('div')
        actions.className = 'flatpickr-actions'

        const actionBtn = document.createElement('button')
        actionBtn.type = 'button'
        actionBtn.className = 'flatpickr-action-btn'
        actionBtn.textContent = applied ? 'Clear' : 'Apply'
        actionBtn.dataset.state = applied ? 'clear' : 'apply'

        actions.appendChild(actionBtn)

        if (instance && instance.calendarContainer) {
          const timeContainer = instance.calendarContainer.querySelector('.flatpickr-time')
          const wrapper = document.createElement('div')
          wrapper.className = 'flatpickr-footer-group'

          if (timeContainer) {
            wrapper.classList.add('has-time')
            wrapper.appendChild(timeContainer)
          }
          wrapper.appendChild(actions)
          instance.calendarContainer.appendChild(wrapper)
        }

        const doApply = () => {
          const dateStr = el.value || (instance && instance.selectedDates && instance.selectedDates.length ? instance.formatDate(instance.selectedDates[0], instance.config.dateFormat) : '')
          if (target && key) try { target[key] = dateStr } catch(e){}
          applied = true
          actionBtn.textContent = 'Clear'
          actionBtn.dataset.state = 'clear'
          try { instance.close() } catch(e){}
        }

        const doClear = () => {
          try { instance.clear() } catch(e){}
          if (target && key) try { target[key] = '' } catch(e){}
          el.value = ''
          applied = false
          actionBtn.textContent = 'Apply'
          actionBtn.dataset.state = 'apply'
          try { instance.close() } catch(e){}
        }

        const onActionClick = (ev) => {
          ev && ev.stopPropagation()
          if (actionBtn.dataset.state === 'clear') doClear(); else doApply()
        }

        actionBtn.addEventListener('click', onActionClick)

        // update button state when user changes selection
        instance.config.onChange.push((selectedDates, dateStr) => {
          try {
            const parent = el && el.parentNode
            if (selectedDates && selectedDates.length) {
              parent && parent.classList.add('has-value')
            } else {
              parent && parent.classList.remove('has-value')
            }
          } catch (e) {}

          // when a new selection is made it becomes pending (needs Apply)
          if (selectedDates && selectedDates.length) {
            applied = false
            actionBtn.textContent = 'Apply'
            actionBtn.dataset.state = 'apply'
          }

          // If binding.value was a function, call it directly
          if (typeof userOnChange === 'function') {
            try { userOnChange(selectedDates, dateStr) } catch (e) {}
          }
        })

        // store references for cleanup
        el._flatpickrActionCleanup = () => {
          try { actionBtn.removeEventListener('click', onActionClick) } catch(e){}
          try { actions.remove() } catch(e){}
        }
      } catch (e) {
        // fail silently if action bar cannot be attached
      }
    }

    // initialize has-value when value present
    // Thai: ใส่คลาส has-value ให้กับ parent ถ้ามีค่าเริ่มต้นใน input
    try { if (el && el.value) el.parentNode && el.parentNode.classList.add('has-value') } catch(e){}

    // store instance for cleanup
    el._flatpickrInstance = instance
  },

  beforeUnmount(el) {
    try {
      if (el._flatpickrInstance && typeof el._flatpickrInstance.destroy === 'function') el._flatpickrInstance.destroy()
      if (el._flatpickrActionCleanup && typeof el._flatpickrActionCleanup === 'function') el._flatpickrActionCleanup()
    } catch (e) {}
    delete el._flatpickrInstance
  }
}
