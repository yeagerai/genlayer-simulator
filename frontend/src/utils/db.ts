import type { ContractFile, DeployedContract, TransactionItem } from '@/types'
import Dexie, { type Table } from 'dexie'

export class GenLayerSimulatorDB extends Dexie {
  contractFiles!: Table<ContractFile>
  deployedContracts!: Table<DeployedContract>
  transactions!: Table<TransactionItem>

  constructor() {
    super('genLayerSimulatorDB')
    this.version(2).stores({
      contractFiles: 'id, name, content, example, updatedAt',
      deployedContracts: '[contractId+address]',
      defaultContractStates: '[contractId+address]',
    })

    this.version(2).stores({
      contractFiles: 'id', // Primary key and indexed props
      deployedContracts: '[contractId+address]',
      defaultContractStates: null,
      transactions:
        '++id, type, status, contractAddress, localContractId, txId',
    })
  }
}

export const db = new GenLayerSimulatorDB()
