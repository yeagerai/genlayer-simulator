import { useContractsStore } from '@/stores'
import type { TransactionItem } from '@/types'
import type { App } from 'vue'

const queue: TransactionItem[] = []
export const TransactionsListenerPlugin = {
  install(app: App, { interval = 5000 }: { interval: number }) {
    const listener = async () => {
      const store = useContractsStore()

      const pendingTxs = store.transactions.filter(
        (tx: TransactionItem) =>
          tx.status === 'PENDING' && queue.findIndex((q) => q.txId !== tx.txId) === -1
      ) as TransactionItem[]
      if (pendingTxs.length > 0) {
        queue.push(...pendingTxs)
        const requests = queue.map((tx) => store.getTransaction(tx.txId))
        const results = await Promise.all(requests)
        queue.splice(0, queue.length)

        console.log(`There are ${pendingTxs.length} pending transactions`, results)
      }
    }
    setInterval(listener, interval)
  }
}
