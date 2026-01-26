import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

//JS
import './assets/js/flatpickr.min.js'
import './assets/js/jquery-3.6.0.min.js'

import flatpickrDirective from './directives/flatpickr.js'
import hasValueDirective from './directives/hasValue.js'

// css
import './assets/css/base.css'
import './assets/css/bootstrap.min.css'
import './assets/css/components.css'
import './assets/css/all.min.css'
import './assets/css/flatpickr.min.css'
import './assets/css/datatable.css'




const app = createApp(App)
app.use(createPinia())
app.use(router)
app.directive('flatpickr', flatpickrDirective)
app.directive('has-value', hasValueDirective)
app.mount('#app')