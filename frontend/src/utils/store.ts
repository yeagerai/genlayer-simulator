import { useContractsFilesStore } from '@/stores'
import { db } from './db'
import { v4 as uuidv4 } from 'uuid'

export const setupStores = async () => {
  const contractsFilesStore = useContractsFilesStore()
  if ((await db.contractFiles.count()) === 0) {
    const contractsBlob = import.meta.glob('@/assets/examples/contracts/*.py', {
      query: '?raw',
      import: 'default'
    })
    for (const key of Object.keys(contractsBlob)) {
      const raw = await contractsBlob[key]()
      const name = key.split('/').pop() || 'ExampleContract.py'
      const contract = {
        id: uuidv4(),
        name,
        content: (raw as string || '').trim()
      }
      contractsFilesStore.addContractFile(contract)
    }
  } else {
    contractsFilesStore.contracts = await db.contractFiles.toArray()
  }

  contractsFilesStore.deployedContracts = await db.deployedContracts.toArray()
  contractsFilesStore.defaultContractStates = await db.defaultContractStates.toArray()
}
