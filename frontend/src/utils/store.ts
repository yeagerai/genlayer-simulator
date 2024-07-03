import { useAccountsStore, useContractsStore, useTransactionsStore } from '@/stores'
import { db } from './db'
import { v4 as uuidv4 } from 'uuid'

export const setupStores = async () => {
  const contractsStore = useContractsStore()
  const accountsStore = useAccountsStore()
  const transactionsStore = useTransactionsStore()
  if (
    (await db.contractFiles.count()) === 0
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
      contractsStore.addContractFile(contract)
    }
  } else {
    contractsStore.contracts = await db.contractFiles.toArray()
  }

  contractsStore.deployedContracts = await db.deployedContracts.toArray()
  transactionsStore.transactions = await db.transactions.toArray()
  if ( accountsStore.privateKeys.length < 1) {
    accountsStore.generateNewAccount()
  } else {
    accountsStore.privateKeys = localStorage.getItem('accountsStore.privateKeys')
      ? ((localStorage.getItem('accountsStore.privateKeys') || '').split(',') as `0x${string}`[])
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
