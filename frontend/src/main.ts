import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Notifications from '@kyvg/vue3-notification'
import VueTour from "v3-tour";
import "v3-tour/dist/vue-tour.css";
import App from './App.vue'
import router from './router'
import { persistStorePlugin, createToolTipPlugin } from '@/plugins'
import { setupStores } from '@/utils'

const app = createApp(App)
const pinia = createPinia()

pinia.use(persistStorePlugin)
app.use(pinia)

app.use(router)
app.use(
  createToolTipPlugin({
    arrow: true
  })
)
app.use(Notifications)
app.use(VueTour)
app.mount('#app')
setupStores()
