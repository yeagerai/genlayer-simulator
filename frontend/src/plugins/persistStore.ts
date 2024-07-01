import type { ContractFile, DeployedContract, TransactionItem } from '@/types'
import { db, getContractFileName } from '@/utils'
import { type PiniaPluginContext } from 'pinia'

/**
 * Upserts a deployed contract into the database.
 *
 * @param {DeployedContract} contract - The contract to upsert.
 * @return {Promise<void>} A Promise that resolves once the contract is upserted.
 */
const upsertDeployedContract = async (contract: DeployedContract): Promise<void> => {
  const existingContract = await db.deployedContracts
    .where('contractId')
    .equals(contract.contractId)
    .first()
  if (existingContract) {
    await db.deployedContracts.where('contractId').equals(contract.contractId).modify(contract)
  } else {
    await db.deployedContracts.add(contract)
  }
}

/**
 * A plugin for persisting the state of a Pinia store.
 *
 * @param {PiniaPluginContext} context - The context object containing the Pinia store.
 * @return {void} This function does not return anything.
 */
export function persistStorePlugin(context: PiniaPluginContext): void {
  context.store.$onAction(({ store, name, args, after }) => {
    console.log(`Called Action "${name}" with params [${JSON.stringify(args)}].`)
    after(async (result) => {
      if (store.$id === 'contractsStore') {
        switch (name) {
          case 'addContractFile':
            await db.contractFiles.add({
              ...(args[0] as ContractFile),
              name: getContractFileName(args[0].name)
            })
            break
          case 'updateContractFile':
            await db.contractFiles.update(args[0] as string, args[1] as ContractFile)
            break
          case 'removeContractFile':
            await db.contractFiles.delete(args[0])
            await db.deployedContracts
              .where('contractId')
              .equals(args[0] as string)
              .delete()
            break
          case 'openFile':
            localStorage.setItem('contractsStore.currentContractId', args[0] as string)
            localStorage.setItem('contractsStore.openedFiles', store.openedFiles.join(','))
            break
          case 'closeFile':
            localStorage.setItem('contractsStore.currentContractId', store.currentContractId)
            localStorage.setItem('contractsStore.openedFiles', store.openedFiles.join(','))
            break
          case 'addDeployedContract':
            await upsertDeployedContract(args[0] as DeployedContract)
            break
          case 'setCurrentContractId':
            localStorage.setItem('contractsStore.currentContractId', args[0] as string)
            break

          case 'removeDeployedContract':
            await db.deployedContracts
              .where('contractId')
              .equals(args[0] as string)
              .delete()
            break
          default:
            break
        }
      } else if (store.$id === 'accountsStore') {
        switch (name) {
          case 'generateNewAccount':
            localStorage.setItem('accountsStore.privateKeys', store.accounts.join(','))
            localStorage.setItem('accountsStore.currentPrivateKey', store.currentPrivateKey)
            break
          default:
            break
        }
      } else if (store.$id === 'transactionsStore') {
        switch (name) {
          case 'addTransaction':
            await db.transactions.add(args[0])
            break
          case 'removeTransaction':
            await db.transactions
              .where('txId')
              .equals(args[0] as string)
              .delete()
            break
          case 'updateTransaction':
            await db.transactions
              .where('txId')
              .equals((args[0] as any).id)
              .modify({ data: args[0], status: args[0].status })
            break
          default:
            break
        }
      }
      console.log('PersistStorePlugin:::', { name, args, result })
    })
  })
}
