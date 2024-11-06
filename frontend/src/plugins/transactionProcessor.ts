import { useContractsStore, useTransactionsStore } from '@/stores';
import type { TransactionItem } from '@/types';
import type { App } from 'vue';
import { useWebSocketClient } from '@/hooks';

export const TransactionsListenerPlugin = {
  install(_app: App) {
    const contractsStore = useContractsStore();
    const transactionsStore = useTransactionsStore();
    const webSocketClient = useWebSocketClient();

    webSocketClient.on(
      'transaction_status_updated',
      handleTransactionStatusUpdate,
    );

    async function handleTransactionStatusUpdate(eventData: any) {
      const newTx = await transactionsStore.getTransaction(eventData.data.hash);

      if (!newTx) {
        transactionsStore.removeTransaction(newTx);
        return;
      }

      const currentTx = transactionsStore.transactions.find(
        (t: TransactionItem) => t.hash === eventData.data.hash,
      );

      transactionsStore.updateTransaction(newTx);

      if (newTx?.status === 'FINALIZED' && currentTx?.type === 'deploy') {
        contractsStore.addDeployedContract({
          contractId: currentTx.localContractId,
          address: newTx.data.contract_address,
          defaultState: '{}',
        });
        currentTx.data.contractAddress = newTx.data.contractAddress;
      }
    }
  },
};
