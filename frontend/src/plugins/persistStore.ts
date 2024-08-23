import type { ContractFile } from '@/types';
import { type PiniaPluginContext } from 'pinia';
import { useDb, useFileName } from '@/hooks';

const ENABLE_LOGS = false;
const db = useDb();
const { cleanupFileName } = useFileName();

// TODO: either update and test or find another solution for persisting the store
/**
 * A plugin for persisting the state of a Pinia store.
 *
 * @param {PiniaPluginContext} context - The context object containing the Pinia store.
 * @return {void} This function does not return anything.
 */
export function persistStorePlugin(context: PiniaPluginContext): void {
  context.store.$onAction(({ store, name, args, after }) => {
    if (ENABLE_LOGS) {
      console.log(
        `Called Action "${name}" with params [${JSON.stringify(args)}].`,
      );
    }

    after(async (result) => {
      if (store.$id === 'contractsStore') {
        switch (name) {
          case 'addContractFile':
            await db.contractFiles.add({
              ...(args[0] as ContractFile),
              name: cleanupFileName(args[0].name),
            });
            break;
          case 'updateContractFile':
            await db.contractFiles.update(args[0] as string, {
              ...(args[1] as ContractFile),
            });
            break;
          case 'removeContractFile':
            await db.contractFiles.delete(args[0]);
            break;
          case 'openFile':
            await db.contractFiles.update(args[0].id, {
              ...(args[0] as ContractFile),
            });
            break;
          default:
            break;
        }
      } else if (store.$id === 'accountsStore') {
        switch (name) {
          case 'generateNewAccount':
          case 'removeAccount':
          case 'setCurrentAccount':
            localStorage.setItem(
              'accountsStore.privateKeys',
              store.privateKeys.join(','),
            );
            localStorage.setItem(
              'accountsStore.currentPrivateKey',
              store.currentPrivateKey,
            );
            break;
          default:
            break;
        }
      } else if (store.$id === 'transactionsStore') {
        switch (name) {
          case 'addTransaction':
            await db.transactions.add(args[0]);
            break;
          case 'removeTransaction':
            await db.transactions
              .where('txId')
              .equals((args[0] as any).txId)
              .delete();
            break;
          case 'updateTransaction':
            await db.transactions
              .where('txId')
              .equals((args[0] as any).id)
              .modify({ data: args[0], status: args[0].status });
            break;
          case 'clearTransactionsForContract':
            await db.transactions
              .where('localContractId')
              .equals(args[0])
              .delete();
            break;
          default:
            break;
        }
      }

      if (ENABLE_LOGS) {
        console.log('PersistStorePlugin:::', { name, args, result });
      }
    });
  });
}
