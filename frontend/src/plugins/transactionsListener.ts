import { useContractsStore, useTransactionsStore } from '@/stores'
import type { TransactionItem } from '@/types'
import { notify } from '@kyvg/vue3-notification'
import type { App } from 'vue'

export const TransactionsListenerPlugin = {
  install(_app: App, { interval = 5000 }: { interval: number }) {
    const contractsStore = useContractsStore()
    const transactionsStore = useTransactionsStore()

    const listener = async () => {
      const pendingTxs = transactionsStore.transactions.filter(
        (tx: TransactionItem) =>
          tx.status !== 'FINALIZED' &&
          transactionsStore.processingQueue.findIndex((q) => q.txId !== tx.txId) === -1
      ) as TransactionItem[]

      transactionsStore.processingQueue.push(...pendingTxs)
      if (transactionsStore.processingQueue.length > 0) {
        const requests = transactionsStore.processingQueue.map((tx) =>
          transactionsStore.getTransaction(tx.txId)
        )
        const results = await Promise.all(requests)
        results.forEach((tx) => {
          const currentTx = transactionsStore.processingQueue.find((t) => t.txId === tx?.data?.id)
          transactionsStore.updateTransaction(tx?.data)
          transactionsStore.processingQueue = transactionsStore.processingQueue.filter(
            (t) => t.txId !== tx?.data?.id
          )
          // if finalized and is contract add to the contract store dpeloyed
          if (tx?.data?.status === 'FINALIZED' && currentTx?.type === 'deploy') {
            contractsStore.addDeployedContract({
              contractId: currentTx.localContractId,
              address: currentTx.contractAddress,
              defaultState: '{}'
            })
          }
        })
        console.log(`There are ${pendingTxs.length} pending transactions`, results)
      }
    }
    setInterval(listener, interval)
  }
}
