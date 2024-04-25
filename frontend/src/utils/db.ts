import type { ContractFile, DefaultContractState, DeployedContract } from '@/types'
import Dexie, { type Table } from 'dexie'
const contractsBlob = import.meta.glob('@/assets/examples/contracts/*.py', { as: 'raw' })
import { v4 as uuidv4 } from 'uuid'

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

export async function setupDB() {
  if ((await db.contractFiles.count()) === 0) {
    for (const key of Object.keys(contractsBlob)) {
      const raw = await contractsBlob[key]()
      const name = key.split('/').pop()?.split('.')[0] || 'ExampleContract'
      await db.contractFiles.add({
        id: uuidv4(),
        name,
        content: raw?.trim()
      })
    }
  }
}
