import { useMainStore } from '@/stores'
import { db } from './db'
import { v4 as uuidv4 } from 'uuid'


export const setupStores = async () => {
  const mainStore = useMainStore()
  const contracts = await db.contractFiles.toArray()
  if (
    (contracts.filter((c) => c.example && !c.updatedAt).map((c) => c.id).length) === 0 ) {
      
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
        content: ((raw as string) || '').trim(),
        example: true
      }
      mainStore.addContractFile(contract)
    }
  } else {
    mainStore.contracts = await db.contractFiles.toArray()
  }

  mainStore.deployedContracts = await db.deployedContracts.toArray()
  if (mainStore.accounts.length < 1) {
    await mainStore.generateNewAccount()
  } else {
    mainStore.accounts = localStorage.getItem('mainStore.accounts')
      ? (localStorage.getItem('mainStore.accounts') || '').split(',')
      : []
  }
}

export const getContractFileName = (name: string) => {
  const tokens = name.split('.')
  if (tokens.length > 0) {
    return `${tokens[0]}.gpy`
  }
  return `${name}.gpy`
}
