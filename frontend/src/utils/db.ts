import type { ContractFile, DeployedContract } from '@/types'
import Dexie, { type Table } from 'dexie'

export class GenLayerSimulatorDB extends Dexie {
  contractFiles!: Table<ContractFile>
  deployedContracts!: Table<DeployedContract>

  constructor() {
    super('genLayerSimulatorDB')
    this.version(1).stores({
      contractFiles: 'id', 
      deployedContracts: '[contractId+address]',
      defaultContractStates: '[contractId+address]'
    })
  }
}

export const db = new GenLayerSimulatorDB()
