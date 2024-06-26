import { useAccountsStore, useContractsStore } from '@/stores'
import { db } from './db'
import { v4 as uuidv4 } from 'uuid'

export const setupStores = async () => {
  const contracts = useContractsStore()
  const accounts = useAccountsStore()
  // await db.contractFiles.clear()
  // localStorage.setItem('mainStore.contractsModified', '')
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
      contracts.addContractFile(contract)
    }
  } else {
    contracts.contracts = await db.contractFiles.toArray()
  }

  contracts.deployedContracts = await db.deployedContracts.toArray()
  if ( accounts.accounts.length < 1) {
    await accounts.generateNewAccount()
  } else {
    accounts.accounts = localStorage.getItem('accountsStore.accounts') ?  (localStorage.getItem('accountsStore.accounts') || '').split(',') : []
  }
}


export const getContractFileName = (name: string) => {
  const tokens = name.split('.')
  if (tokens.length > 0) {
    return `${tokens[0]}.gpy`
  }
  return `${name}.gpy`
}