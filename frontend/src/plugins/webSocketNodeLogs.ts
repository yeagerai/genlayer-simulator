import { webSocketClient } from '@/utils'
import { type PiniaPluginContext } from 'pinia'

export function webSocketNodeLogsPlugin(context: PiniaPluginContext): void {
  webSocketClient.on('status_update', (event) => {
    if(context.store.$id === 'mainStore') {
      context.store.nodeLogs.push({ date: new Date().toISOString(), message: event.message })
    }
    
  })
}
