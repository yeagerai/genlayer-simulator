import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Notifications from '@kyvg/vue3-notification'

import App from './App.vue'
import router from './router'
import { createToolTipPlugin } from './plugins'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(
  createToolTipPlugin({
    arrow: true
  })
)
app.use(Notifications)

app.mount('#app')
