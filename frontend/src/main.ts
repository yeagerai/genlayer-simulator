import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Notifications from '@kyvg/vue3-notification'
import App from './App.vue'
import router from './router'
import { PersistStorePlugin, createToolTipPlugin } from '@/plugins'
import { setupDB } from '@/utils'
import { seedStores } from '@/utils/store'

const app = createApp(App)


const pinia = createPinia()
// give the plugin to pinia
pinia.use(PersistStorePlugin)

app.use(pinia)
app.use(router)
app.use(
  createToolTipPlugin({
    arrow: true
  })
)
app.use(Notifications)

app.mount('#app')

setupDB().then(() => {
  seedStores()
})
