import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import type { TransactionItem } from '@/types';
import { useRpcClient } from '@/hooks';

export const useTransactionsStore = defineStore('transactionsStore', () => {
  const rpcClient = useRpcClient();
  const pendingTransactions = computed<TransactionItem[]>(() =>
    transactions.value.filter((t) => t.status === 'PENDING'),
  );
  const processingQueue = ref<TransactionItem[]>([]);
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
      console.trace('updateTransaction', tx); // Temporary logging to debug always-PENDING transactions
    }
  }

  async function getTransaction(hash: string) {
    return rpcClient.getTransactionByHash(hash);
  }

  function clearTransactionsForContract(contractId: string) {
    processingQueue.value = processingQueue.value.filter(
      (t) => t.localContractId !== contractId,
    );

    transactions.value = transactions.value.filter(
      (t) => t.localContractId !== contractId,
    );
  }

  async function setTransactionAppeal(tx_address: string) {
    rpcClient.setTransactionAppeal(tx_address);
  }

  return {
    transactions,
    pendingTransactions,
    processingQueue,
    getTransaction,
    addTransaction,
    removeTransaction,
    updateTransaction,
    clearTransactionsForContract,
    setTransactionAppeal,
  };
});
