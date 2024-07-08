import { useAccountsStore, useContractsStore, useTransactionsStore } from '@/stores'
import { db } from './db'
import { v4 as uuidv4 } from 'uuid'

// for old version and local storage
export const examplesNames = [
  'football_prediction_market.py',
  'llm_erc20.py',
  'storage.py',
  'user_storage.py',
  'wizard_of_coin.py'
]

export const setupStores = async () => {
  const contractsStore = useContractsStore()
  const accountsStore = useAccountsStore()
  const transactionsStore = useTransactionsStore()
  const contractFiles = await db.contractFiles.toArray()
  const filteredFiles = contractFiles.filter((c) => (c.example && !c.updatedAt ) || (!c.example && !c.updatedAt))
  
  if (filteredFiles.length === 0) {
    const contractsBlob = import.meta.glob('@/assets/examples/contracts/*.py', {
      query: '?raw',
      import: 'default'
    })
    for (const key of Object.keys(contractsBlob)) {
      const raw = await contractsBlob[key]()
      const name = key.split('/').pop() || 'ExampleContract.py'
      if(!contractFiles.some((c) => c.name === name)) {
        const contract = {
          id: uuidv4(),
          name,
          content: ((raw as string) || '').trim(),
          example: true
        }
        contractsStore.addContractFile(contract)
      }
    }
  } else {
    contractsStore.contracts = await db.contractFiles.toArray()
  }

  contractsStore.deployedContracts = await db.deployedContracts.toArray()
  transactionsStore.transactions = await db.transactions.toArray()
  if (accountsStore.accounts.length < 1) {
    await accountsStore.generateNewAccount()
  } else {
    accountsStore.accounts = localStorage.getItem('accountsStore.accounts')
      ? (localStorage.getItem('accountsStore.accounts') || '').split(',')
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
