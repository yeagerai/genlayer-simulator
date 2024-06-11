import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Notifications from '@kyvg/vue3-notification'
import App from './App.vue'
import router from './router'
import { persistStorePlugin, createToolTipPlugin, webSocketNodeLogsPlugin } from '@/plugins'
import { RpcClient, setupStores } from '@/utils'
import { JsonRpcService } from './services/JsonRpcService'
import { VueSpinnersPlugin } from 'vue3-spinners'

const app = createApp(App)
const pinia = createPinia()

pinia.use(persistStorePlugin).use(webSocketNodeLogsPlugin)
app.use(pinia)

app.use(router)
app.use(
  createToolTipPlugin({
    arrow: true
  })
)
app.use(Notifications)
app.provide('$jsonRpc', new JsonRpcService(new RpcClient()))
app.use(VueSpinnersPlugin)
app.mount('#app')
setupStores()
