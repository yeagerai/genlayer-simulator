import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { TransactionItem } from '@/types';
import { useRpcClient, useWebSocketClient } from '@/hooks';

// TODO: get client session id to persist so that events get passed when reloading

export const useTransactionsStore = defineStore('transactionsStore', () => {
  const rpcClient = useRpcClient();
  // const webSocketClient = useWebSocketClient();
  const transactions = ref<TransactionItem[]>([]);

  function addTransaction(tx: TransactionItem) {
    transactions.value.unshift(tx); // Push on top in case there's no date property yet
  }

  function removeTransaction(tx: TransactionItem) {
    transactions.value = transactions.value.filter((t) => t.hash !== tx.hash);
  }

  function updateTransaction(tx: any) {
    const index = transactions.value.findIndex((t) => t.hash === tx.hash);
    if (index !== -1) {
      const current = transactions.value[index];

      transactions.value.splice(index, 1, {
        ...current,
        status: tx.status,
        data: tx,
      });
    } else {
      // Temporary logging to debug always-PENDING transactions
      console.warn('Transaction not found', tx);
      console.trace('updateTransaction', tx);
    }
  }

  function refreshPendingTransactions() {
    const pendingTxs = transactions.value.filter(
      (tx: TransactionItem) => tx.status !== 'FINALIZED',
    ) as TransactionItem[];

    pendingTxs.forEach(async (tx) => {
      const newTx = await getTransaction(tx.hash);
      updateTransaction(newTx);
    });
  }

  async function getTransaction(hash: string) {
    return rpcClient.getTransactionByHash(hash);
  }

  function clearTransactionsForContract(contractId: string) {
    transactions.value = transactions.value.filter(
      (t) => t.localContractId !== contractId,
    );
  }

  return {
    transactions,
    getTransaction,
    addTransaction,
    removeTransaction,
    updateTransaction,
    clearTransactionsForContract,
    refreshPendingTransactions,
  };
});
