import { useMainStore } from '@/stores'
import { db } from './db'
import { v4 as uuidv4 } from 'uuid'

export const setupStores = async () => {
  const mainStore = useMainStore()
  if (
    (await db.contractFiles.count()) === 0 &&
    !localStorage.getItem('mainStore.contractsModified')
  ) {
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
        content: ((raw as string) || '').trim()
      }
      mainStore.addContractFile(contract)
    }
  } else {
    mainStore.contracts = await db.contractFiles.toArray()
  }

  mainStore.deployedContracts = await db.deployedContracts.toArray()
  mainStore.defaultContractStates = await db.defaultContractStates.toArray()

  if (!mainStore.currentUserAddress) {
    const address = await mainStore.generateNewAccount()
    mainStore.currentUserAddress = address || ''
  }
}
