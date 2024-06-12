import type { NodeLog } from '@/types'
import { webSocketClient } from '@/utils'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useNodeStore = defineStore('nodeStore', () => {
  const logs = ref<NodeLog[]>([])
  const listenWebsocket = ref<boolean>(true)
  
  if (!webSocketClient.connected) webSocketClient.connect()
  webSocketClient.on('status_update', (event) => {
    if (listenWebsocket.value) {
      logs.value.push({ date: new Date().toISOString(), message: event.message })
    }
  })
  return { logs }
})
