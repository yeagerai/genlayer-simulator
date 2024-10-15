import { useContractsStore, useTransactionsStore } from '@/stores';
import type { TransactionItem } from '@/types';
import type { App } from 'vue';

const ENABLE_LOGS = false;

export const TransactionsListenerPlugin = {
  install(_app: App, { interval = 5000 }: { interval: number }) {
    const contractsStore = useContractsStore();
    const transactionsStore = useTransactionsStore();

    const listener = async () => {
      const pendingTxs = transactionsStore.transactions.filter(
        (tx: TransactionItem) =>
          tx.status !== 'FINALIZED' &&
          transactionsStore.processingQueue.findIndex(
            (q) => q.hash !== tx.hash,
          ) === -1,
      ) as TransactionItem[];

      transactionsStore.processingQueue.push(...pendingTxs);
      if (transactionsStore.processingQueue.length > 0) {
        for (const item of transactionsStore.processingQueue) {
          const tx = await transactionsStore.getTransaction(item.hash);
          if (!tx) {
            // Remove the transaction from the processing queue and storage if not found
            transactionsStore.processingQueue =
              transactionsStore.processingQueue.filter(
                (t) => t.hash !== item.hash,
              );
            transactionsStore.removeTransaction(item);
          } else {
            const currentTx = transactionsStore.processingQueue.find(
              (t) => t.hash === tx?.hash,
            );
            transactionsStore.updateTransaction(tx);
            transactionsStore.processingQueue =
              transactionsStore.processingQueue.filter(
                (t) => t.hash !== tx?.hash,
              );
            // if finalized and is contract add to the contract store dpeloyed
            if (tx?.status === 'FINALIZED' && currentTx?.type === 'deploy') {
              if (ENABLE_LOGS) {
                console.log('New deployed contract', currentTx);
              }

              contractsStore.addDeployedContract({
                contractId: currentTx.localContractId,
                address: tx.data.contract_address,
                defaultState: '{}',
              });
              currentTx.data.contractAddress = tx.data.contractAddress;
            }
          }
        }

        if (ENABLE_LOGS) {
          console.log(`There are ${pendingTxs.length} pending transactions`);
        }
      }
    };
    setInterval(listener, interval);
  },
};
