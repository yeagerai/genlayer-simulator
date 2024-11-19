import { useTransactionsStore } from '@/stores';
import type { TransactionItem } from '@/types';
import { useWebSocketClient } from '@/hooks';

export function useTransactionListener() {
  const transactionsStore = useTransactionsStore();
  const webSocketClient = useWebSocketClient();
  // Track the latest request timestamp for each transaction
  const latestRequestTimes = new Map<string, number>();

  function init() {
    webSocketClient.on(
      'transaction_status_updated',
      handleTransactionStatusUpdate,
    );
  }

  async function getTransaction(hash: string, requestTime: number) {
    // console.log(`🔄 Fetching transaction ${hash}`);
    const result = await transactionsStore.getTransaction(hash);

    // Only process the result if this is still the latest request for this hash
    if (latestRequestTimes.get(hash) === requestTime) {
      // console.log(`✅ Fetched status: ${result.status}`);
      return result;
    } else {
      // console.log(`⏭️ Skipping outdated result for ${hash}`);
      return null;
    }
  }

  async function handleTransactionStatusUpdate(eventData: any) {
    const { hash, new_status } = eventData.data;
    console.log(`📥 Received update for hash: ${new_status}`);

    const requestTime = Date.now();
    latestRequestTimes.set(hash, requestTime);

    const newTx = await getTransaction(hash, requestTime);

    if (!newTx) return;

    // console.log(`📤 Processing update for hash: ${hash}`, newTx);

    // console.log('newTx', newTx.status);
    if (!newTx) {
      console.warn('Server tx not found for local tx:', newTx);
      transactionsStore.removeTransaction(newTx);
      return;
    }

    const currentTx = transactionsStore.transactions.find(
      (t: TransactionItem) => t.hash === hash,
    );

    if (!currentTx) {
      console.warn('Current tx not found:', hash);
      // This happens regularly when local transactions get cleared (e.g. user clears all txs or deploys new contract instance)
      return;
    }

    transactionsStore.updateTransaction(newTx);
  }

  return {
    init,
  };
}
