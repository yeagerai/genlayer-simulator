import type { ContractFile, TransactionItem } from '@/types';
import Dexie, { type Table } from 'dexie';

class GenLayerSimulatorDB extends Dexie {
  contractFiles!: Table<ContractFile>;
  transactions!: Table<TransactionItem>;

  constructor() {
    super('genLayerSimulatorDB');

    this.version(2).stores({
      contractFiles: 'id',
      deployedContracts: '[contractId+address]',
      transactions:
        '++id, type, status, contractAddress, localContractId, txId',
    });

    // TODO: migrate to version 3
    this.version(3).stores({
      contractFiles: 'id',
      transactions:
        '++id, type, status, contractAddress, localContractId, txId',
    });
  }
}

export const useDb = () => {
  return new GenLayerSimulatorDB();
};
