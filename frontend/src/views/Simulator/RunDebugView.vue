<script setup lang="ts">
import {
  useAccountsStore,
  useContractsStore,
  useTransactionsStore,
} from '@/stores';
import { computed, onMounted, onUnmounted, watch } from 'vue';
import { notify } from '@kyvg/vue3-notification';
import ContractState from '@/components/Simulator/ContractState.vue';
import ExecuteTransactions from '@/components/Simulator/ExecuteTransactions.vue';
import TransactionsList from '@/components/Simulator/TransactionsList.vue';
import ConstructorParameters from '@/components/Simulator/ConstructorParameters.vue';
import ContractMethodItem from '@/components/Simulator/ContractMethodItem.vue';
import { debounce } from 'vue-debounce';
import PageSection from '@/components/Simulator/PageSection.vue';
import type { ContractMethod } from '@/types';
import { InputTypesMap } from '@/utils';
import EmptyListPlaceholder from '@/components/Simulator/EmptyListPlaceholder.vue';
import NewContractState from '@/components/Simulator/NewContractState.vue';
import MainTitle from '@/components/Simulator/MainTitle.vue';

const contractsStore = useContractsStore();
const accountsStore = useAccountsStore();
const transactionsStore = useTransactionsStore();

let deploymentSubscription: () => void;
const contractTransactions = computed(() =>
  transactionsStore.transactions.filter(
    (t) => t.localContractId === contractsStore.currentContractId,
  ),
);

const handleGetContractState = async (
  contractAddress: string,
  method: string,
  methodArguments: string[],
) => {
  try {
    await contractsStore.getContractState(
      contractAddress,
      method,
      methodArguments,
    );
  } catch (error) {
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error getting contract state',
      type: 'error',
    });
  }
};

const handleDeployContract = async ({
  params: constructorParams,
}: {
  params: { [k: string]: string };
}) => {
  try {
    await contractsStore.deployContract({
      constructorParams,
    });
    notify({
      title: 'OK',
      text: 'Started deploying the contract',
      type: 'success',
    });
  } catch (err) {
    notify({
      title: 'Error',
      text: (err as Error)?.message || 'Error deploying contract',
      type: 'error',
    });
  }
};

// const handleClearTransactions = () => {
//   transactionsStore.processingQueue.forEach((t) => {
//     if (t.localContractId === contractsStore.currentContractId) {
//       transactionsStore.removeTransaction(t);
//     }
//   });
//   transactionsStore.transactions.forEach((t) => {
//     if (t.localContractId === contractsStore.currentContractId) {
//       transactionsStore.removeTransaction(t);
//     }
//   });
// };

// const debouncedGetConstructorInputs = debounce(
//   () => contractsStore.getConstructorInputs(),
//   3000,
// );

// watch(
//   () => contractsStore.deployedContract?.contractId,
//   (newValue) => {
//     if (newValue) {
//       contractsStore.getCurrentContractAbi();
//     }
//   },
// );

// watch(
//   () => contractsStore.currentContract?.id,
//   (newValue, oldValue) => {
//     if (newValue && newValue !== oldValue) {
//       contractsStore.getConstructorInputs();
//     }
//   },
// );

// watch(
//   () => contractsStore.currentContract?.content,
//   (newValue, oldValue) => {
//     if (
//       newValue &&
//       newValue !== oldValue &&
//       !contractsStore.loadingConstructorInputs
//     ) {
//       debouncedGetConstructorInputs();
//     }
//   },
// );
// watch(
//   () => contractsStore.currentErrorConstructorInputs,
//   (newValue, oldValue) => {
//     if (newValue && newValue !== oldValue) {
//       notify({
//         title: 'Error',
//         text: 'Error getting the contract schema',
//         type: 'error',
//       });
//     }
//   },
// );

// onMounted(async () => {
//   // await contractsStore.getConstructorInputs();
//   // if (contractsStore.deployedContract) {
//   //   contractsStore.getCurrentContractAbi();
//   // }
//   // TODO: re-implement this smh
//   deploymentSubscription = contractsStore.$onAction(
//     ({ name, store, args, after }) => {
//       if (name === 'addDeployedContract' && store.$id === contractsStore.$id) {
//         after(() => {
//           notify({
//             title: 'Contract deployed',
//             text: `to ${args[0]?.address}`,
//             type: 'success',
//           });
//         });
//       }
//     },
//   );
// });

// onUnmounted(() => {
//   if (deploymentSubscription) {
//     deploymentSubscription();
//   }
// });

// const readMethods = computed(() => {
//   return Object.entries(
//     contractsStore.currentDeployedContractAbi?.methods || {},
//   )
//     .filter((m) => m[0].startsWith('get_'))
//     .map(([methodName, method]) => ({
//       methodName,
//       method,
//     }));
// });

// const writeMethods = computed(() => {
//   return Object.entries(
//     contractsStore.currentDeployedContractAbi?.methods || {},
//   )
//     .filter((m) => !m[0].startsWith('_') && !m[0].startsWith('get_'))
//     .map(([methodName, method]) => ({
//       methodName,
//       method,
//     }));
// });
</script>

<template>
  <div class="flex max-h-[93vh] w-full flex-col overflow-y-auto">
    <MainTitle>Run and Debug</MainTitle>

    <NewContractState
      v-if="contractsStore.currentContract && contractsStore.currentContractId"
    />

    <div
      class="flex w-full flex-col bg-slate-100 px-2 py-2 dark:dark:bg-zinc-700"
      v-else
    >
      <div class="text-sm">
        Please first select an intelligent contract in the
        <RouterLink
          :to="{ name: 'contracts' }"
          class="text-primary underline dark:text-white"
        >
          Files list.
        </RouterLink>
      </div>
    </div>
  </div>
</template>
