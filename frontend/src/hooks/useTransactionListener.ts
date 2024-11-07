import { useContractsStore, useTransactionsStore } from '@/stores';
import type { TransactionItem } from '@/types';
import { useWebSocketClient } from '@/hooks';

export function useTransactionListener() {
  const contractsStore = useContractsStore();
  const transactionsStore = useTransactionsStore();
  const webSocketClient = useWebSocketClient();

  function init() {
    webSocketClient.on(
      'transaction_status_updated',
      handleTransactionStatusUpdate,
    );
  }

  async function handleTransactionStatusUpdate(eventData: any) {
    const newTx = await transactionsStore.getTransaction(eventData.data.hash);

    if (!newTx) {
      console.warn('Server tx not found for local tx:', newTx);
      transactionsStore.removeTransaction(newTx);
      return;
    }

    const currentTx = transactionsStore.transactions.find(
      (t: TransactionItem) => t.hash === eventData.data.hash,
    );

    if (!currentTx) {
      // This happens regularly when local transactions get cleared (e.g. user clears all txs or deploys new contract instance)
      return;
    }

    transactionsStore.updateTransaction(newTx);
  }

  return {
    init,
  };
}
