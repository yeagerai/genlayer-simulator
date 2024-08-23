import {
  useAccountsStore,
  useContractsStore,
  useTransactionsStore,
  useNodeStore,
} from '@/stores';
import { useDb } from '@/hooks';
import { v4 as uuidv4 } from 'uuid';
import type { Address } from '@/types';

export const useSetupStores = () => {
  const setupStores = async () => {
    const contractsStore = useContractsStore();
    const accountsStore = useAccountsStore();
    const transactionsStore = useTransactionsStore();
    const nodeStore = useNodeStore();
    const db = useDb();

    console.log('populate');
    contractsStore.contracts = await db.contractFiles.toArray();
    transactionsStore.transactions = await db.transactions.toArray();

    nodeStore.getValidatorsData();

    // TODO: persist with plugin + move init to store
    if (accountsStore.privateKeys.length < 1) {
      accountsStore.generateNewAccount();
    } else {
      accountsStore.privateKeys = localStorage.getItem(
        'accountsStore.privateKeys',
      )
        ? ((localStorage.getItem('accountsStore.privateKeys') || '').split(
            ',',
          ) as Address[])
        : [];
    }
  };

  return {
    setupStores,
  };
};
