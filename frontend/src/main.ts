import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Notifications from '@kyvg/vue3-notification'
import App from './App.vue'
import router from './router'
import { persistStorePlugin, createToolTipPlugin } from '@/plugins'
import { setupStores } from '@/utils'
import { JsonRprService } from './services/JsonRpcService'
import JsonViewer from "vue3-json-viewer";
// if you used v1.0.5 or latster ,you should add import "vue3-json-viewer/dist/index.css"
import "vue3-json-viewer/dist/index.css";

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
app.provide('$jsonRpc', new JsonRprService())
app.use(JsonViewer)
app.mount('#app')
setupStores()
