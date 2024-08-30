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
    transactions.value.push(tx);
  }

  function removeTransaction(tx: TransactionItem) {
    transactions.value = transactions.value.filter((t) => t.txId !== tx.txId);
  }

  function updateTransaction(tx: any) {
    const index = transactions.value.findIndex((t) => t.txId === tx.id);
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
    return rpcClient.getTransactionById(txId);
  }

  function clearTransactionsForContract(contractId: string) {
    processingQueue.value = processingQueue.value.filter(
      (t) => t.localContractId !== contractId,
    );

    transactions.value = transactions.value.filter(
      (t) => t.localContractId !== contractId,
    );
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
  };
});
