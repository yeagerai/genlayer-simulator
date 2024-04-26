import type { ContractFile, DefaultContractState, DeployedContract } from '@/types'
import Dexie, { type Table } from 'dexie'

export class GenLayerSimulatorDB extends Dexie {
  contractFiles!: Table<ContractFile>
  deployedContracts!: Table<DeployedContract>
  defaultContractStates!: Table<DefaultContractState>

  constructor() {
    super('genLayerSimulatorDB')
    this.version(1).stores({
      contractFiles: 'id', // Primary key and indexed props
      deployedContracts: '[contractId+address]',
      defaultContractStates: '[contractId+address]'
    })
  }
}

export const db = new GenLayerSimulatorDB()
