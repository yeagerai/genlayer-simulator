import { defineStore } from 'pinia';
import { computed, inject, ref } from 'vue';
import type { IJsonRpcService } from '@/services';
import type { TransactionItem } from '@/types';
export const useTransactionsStore = defineStore('transactionsStore', () => {
  const $jsonRpc = inject<IJsonRpcService>('$jsonRpc');
  const pendingTransactions = computed<TransactionItem[]>(() =>
    transactions.value.filter((t) => t.status === 'PENDING'),
  );
  const processingQueue = ref<TransactionItem[]>([]);
  const transactions = ref<TransactionItem[]>([]);

  function addTransaction(tx: TransactionItem) {
    transactions.value.push(tx);
  }

  function removeTransaction(tx: TransactionItem) {
    transactions.value = transactions.value.filter((t) => t.txId !== tx.txId);
  }

  function updateTransaction(tx: any) {
    const index = transactions.value.findIndex((t) => t.txId === tx.id);
    console.log(`Updating transaction ${tx.id} at index ${index}`);
    if (index !== -1) {
      const current = transactions.value[index];
      transactions.value.splice(index, 1, {
        ...current,
        status: tx.status,
        data: tx,
      });
    }
  }

  async function getTransaction(txId: number) {
    return $jsonRpc?.getTransactionById(txId);
  }

  return {
    transactions,
    pendingTransactions,
    processingQueue,
    getTransaction,
    addTransaction,
    removeTransaction,
    updateTransaction,
  };
});
