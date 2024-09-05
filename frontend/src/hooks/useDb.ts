import type { ContractFile, DeployedContract, TransactionItem } from '@/types';
import Dexie, { type Table } from 'dexie';

class GenLayerSimulatorDB extends Dexie {
  contractFiles!: Table<ContractFile>;
  deployedContracts!: Table<DeployedContract>;
  transactions!: Table<TransactionItem>;

  constructor() {
    super('genLayerSimulatorDB');

    this.version(2).stores({
      contractFiles: 'id',
      deployedContracts: '[contractId+address]',
      transactions:
        '++id, type, status, contractAddress, localContractId, txId',
    });

    this.version(3).stores({
      contractFiles: 'id',
      deployedContracts: '[contractId+address]',
      transactions:
        '++id, type, status, contractAddress, localContractId, hash',
    });
  }
}

export const useDb = () => {
  return new GenLayerSimulatorDB();
};
