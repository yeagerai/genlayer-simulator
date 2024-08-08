import { useContractsStore, useTransactionsStore } from '@/stores';
import type { TransactionItem } from '@/types';
import type { App } from 'vue';

export const TransactionsListenerPlugin = {
  install(_app: App, { interval = 5000 }: { interval: number }) {
    const contractsStore = useContractsStore();
    const transactionsStore = useTransactionsStore();

    const listener = async () => {
      const pendingTxs = transactionsStore.transactions.filter(
        (tx: TransactionItem) =>
          tx.status !== 'FINALIZED' &&
          transactionsStore.processingQueue.findIndex(
            (q) => q.txId !== tx.txId,
          ) === -1,
      ) as TransactionItem[];

      transactionsStore.processingQueue.push(...pendingTxs);
      if (transactionsStore.processingQueue.length > 0) {
        for (const item of transactionsStore.processingQueue) {
          const tx = await transactionsStore.getTransaction(item.txId);
          if (!tx?.data) {
            // Remove the transaction from the processing queue and storage if not found
            transactionsStore.processingQueue =
              transactionsStore.processingQueue.filter(
                (t) => t.txId !== item.txId,
              );
            transactionsStore.removeTransaction(item);
          } else {
            const currentTx = transactionsStore.processingQueue.find(
              (t) => t.txId === tx?.data?.id,
            );
            transactionsStore.updateTransaction(tx?.data);
            transactionsStore.processingQueue =
              transactionsStore.processingQueue.filter(
                (t) => t.txId !== tx?.data?.id,
              );
            // if finalized and is contract add to the contract store dpeloyed
            if (
              tx?.data?.status === 'FINALIZED' &&
              currentTx?.type === 'deploy'
            ) {
              contractsStore.addDeployedContract({
                contractId: currentTx.localContractId,
                address: currentTx.contractAddress,
                defaultState: '{}',
              });
            }
          }
        }

        console.log(`There are ${pendingTxs.length} pending transactions`);
      }
    };
    setInterval(listener, interval);
  },
};
