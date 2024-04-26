import type { ContractFile, DefaultContractState, DeployedContract } from '@/types'
import { db } from '@/utils'
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

const upsertDefaultContractState = async (contract: DefaultContractState): Promise<void> => {
  const existingContract = await db.defaultContractStates
    .where('contractId')
    .equals(contract.contractId)
    .first()
  if (existingContract) {
    await db.defaultContractStates.where('contractId').equals(contract.contractId).modify(contract)
  } else {
    await db.defaultContractStates.add(contract)
  }
}

/**
 * A plugin for persisting the state of a Pinia store.
 *
 * @param {PiniaPluginContext} context - The context object containing the Pinia store.
 * @return {void} This function does not return anything.
 */
export function PersistStorePlugin(context: PiniaPluginContext): void {

  context.store.$onAction(({ store, name, args, after }) => {
    console.log(`Called Action "${name}" with params [${JSON.stringify(args)}].`)
    after(async (result) => {
      if (store.$id === 'contractsFiles') {
        switch (name) {
          case 'addContractFile':
            await db.contractFiles.add(args[0] as ContractFile)
            break
          case 'updateContractFile':
            await db.contractFiles.update(args[0] as string, args[1] as ContractFile)
            break
          case 'removeContractFile':
            await db.contractFiles.delete(args[0] as string)
            await db.deployedContracts
              .where('contractId')
              .equals(args[0] as string)
              .delete()
            await db.defaultContractStates
              .where('contractId')
              .equals(args[0] as string)
              .delete()
            break
          case 'openFile':
            localStorage.setItem('mainStore.currentContractId', args[0] as string)
            localStorage.setItem('mainStore.openedFiles', store.openedFiles.join(','))
            break
          case 'closeFile':
            localStorage.setItem('mainStore.currentContractId', store.currentContractId)
            localStorage.setItem('mainStore.openedFiles', store.openedFiles.join(','))
            break
          case 'addDeployedContract':
            await upsertDeployedContract(args[0] as DeployedContract)
            break
          case 'addDefaultContractState':
            await upsertDefaultContractState(args[0] as DefaultContractState)
            break
          case 'setCurrentContractId':
            localStorage.setItem('mainStore.currentContractId', args[0] as string)
            break
          default:
            break
        }
      }
      console.log('PersistStorePlugin:::', { name, args, result })
    })
  })
}
