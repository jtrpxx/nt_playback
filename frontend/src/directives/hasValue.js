// Directive v-has-value
// - When attached to an input or its wrapper (.input-group), it keeps the
//   parent `.input-group` updated with `has-value` class based on the field value.
// - This ensures floating labels ('.title-label') move to the floated position
//   when the input has content, matching behavior of :valid or focus.
//
// Thai:
// directive นี้จะคอยตรวจสอบค่าใน input และสลับคลาส `has-value` ให้กับ
// parent (เช่น `.input-group`) เมื่อมีค่าหรือเมื่อมีการพิมพ์ เพื่อให้ label
// ลอยอยู่ในตำแหน่งที่ถูกต้องเมื่อช่องมีค่า

export default {
  mounted(el) {
    // If the directive is used directly on an input, use it; otherwise find an input inside
    const input = el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT'
      ? el
      : el.querySelector('input, textarea, select')
    if (!input) return

    const parent = (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT') ? el.parentNode : el

    const update = () => {
      try {
        const val = input.value
        const has = val !== null && String(val).trim() !== ''
        parent.classList.toggle('has-value', has)
      } catch (e) {
        // ignore
      }
    }

    // update on input and change
    input.addEventListener('input', update)
    input.addEventListener('change', update)

    // initialize
    update()

    el._hasValue_cleanup = () => {
      input.removeEventListener('input', update)
      input.removeEventListener('change', update)
    }
  },

  beforeUnmount(el) {
    if (el._hasValue_cleanup) {
      try { el._hasValue_cleanup() } catch (e) {}
      delete el._hasValue_cleanup
    }
  }
}
