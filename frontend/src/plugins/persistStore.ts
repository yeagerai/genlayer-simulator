import type { ContractFile, DeployedContract } from '@/types'
import { db } from '@/utils'
import { liveQuery } from 'dexie'
import { type PiniaPluginContext } from 'pinia'

const initData = ({ store }: PiniaPluginContext) => {
  if (store.$id === 'contractsFiles') {
    const contractsObservable = liveQuery(() => db.contractFiles.toArray())
    const contracts = contractsObservable.subscribe({
      next: (c) => {
        store.$state.contracts = c
        contracts.unsubscribe()
      }
    })
  }
}

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
export function PersistStorePlugin(context: PiniaPluginContext): void {
  initData(context)
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
            break
          case 'openFile':
              localStorage.setItem('contractFiles.currentContractId', args[0] as string)
              localStorage.setItem('contractFiles.openedFiles', store.openedFiles.join(','))
              break
          case 'closeFile':
              localStorage.setItem('contractFiles.currentContractId', store.currentContractId)
              localStorage.setItem('contractFiles.openedFiles', store.openedFiles.join(','))
              break
          case 'addDeployedContract':
            await upsertDeployedContract(args[0] as DeployedContract)
            break
          default:
            break
        }
      }
      console.log('PersistStorePlugin:::', { name, args, result })
    })
  })
}
