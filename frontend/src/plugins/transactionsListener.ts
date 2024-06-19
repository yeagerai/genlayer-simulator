import { type PiniaPluginContext } from 'pinia'

export function transactionsListenerPlugin(context: PiniaPluginContext): void {
  context.store.$subscribe((mutation, state) => {
    if (mutation.storeId === 'contractsStore') {
      console.log('Transactions Listener:::', { mutation, state })
      // persist to db
    }
  })
}
