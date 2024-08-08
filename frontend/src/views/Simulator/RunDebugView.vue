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
import { debounce } from 'vue-debounce';

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

const handleCallContractMethod = async ({
  method,
  params,
}: {
  method: string;
  params: any[];
}) => {
  const result = await contractsStore.callContractMethod({
    localContractId: contractsStore.deployedContract?.contractId || '',
    method: `${method}`,
    params,
  });
  if (!result) {
    notify({
      title: 'Error',
      text: 'Error calling contract method',
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

const handleClearTransactions = () => {
  transactionsStore.processingQueue.forEach((t) => {
    if (t.localContractId === contractsStore.currentContractId) {
      transactionsStore.removeTransaction(t);
    }
  });
  transactionsStore.transactions.forEach((t) => {
    if (t.localContractId === contractsStore.currentContractId) {
      transactionsStore.removeTransaction(t);
    }
  });
};

const debouncedGetConstructorInputs = debounce(
  () => contractsStore.getConstructorInputs(),
  3000,
);

watch(
  () => contractsStore.deployedContract?.contractId,
  (newValue) => {
    if (newValue) {
      contractsStore.getCurrentContractAbi();
    }
  },
);

watch(
  () => contractsStore.currentContract?.id,
  (newValue, oldValue) => {
    if (newValue && newValue !== oldValue) {
      contractsStore.getConstructorInputs();
    }
  },
);

watch(
  () => contractsStore.currentContract?.content,
  (newValue, oldValue) => {
    if (
      newValue &&
      newValue !== oldValue &&
      !contractsStore.loadingConstructorInputs
    ) {
      debouncedGetConstructorInputs();
    }
  },
);
watch(
  () => contractsStore.currentErrorConstructorInputs,
  (newValue, oldValue) => {
    if (newValue && newValue !== oldValue) {
      notify({
        title: 'Error',
        text: 'Error getting the contract schema',
        type: 'error',
      });
    }
  },
);

onMounted(async () => {
  await contractsStore.getConstructorInputs();
  if (contractsStore.deployedContract) {
    contractsStore.getCurrentContractAbi();
  }
  deploymentSubscription = contractsStore.$onAction(
    ({ name, store, args, after }) => {
      if (name === 'addDeployedContract' && store.$id === contractsStore.$id) {
        after(() => {
          notify({
            title: 'Contract deployed',
            text: `to ${args[0]?.address}`,
            type: 'success',
          });
        });
      }
    },
  );
});

onUnmounted(() => {
  if (deploymentSubscription) {
    deploymentSubscription();
  }
});
</script>

<template>
  <div class="flex max-h-[93vh] w-full flex-col overflow-y-auto">
    <div class="flex w-full flex-col p-2">
      <h3 class="text-xl">Run and Debug</h3>
    </div>
    <div
      class="flex flex-col overflow-y-auto"
      v-if="!!contractsStore.currentContractId"
    >
      <div class="flex flex-col">
        <div
          class="flex w-full flex-col bg-slate-100 px-2 py-2 dark:bg-zinc-700"
        >
          <div class="text-sm">Intelligent Contract:</div>
          <div data-testid="current-contract-name" class="text-xs text-neutral-800 dark:text-neutral-200">
            {{ contractsStore.currentContract?.name }}
          </div>
        </div>
        <ConstructorParameters
          :inputs="contractsStore.currentConstructorInputs"
          :loading="contractsStore.loadingConstructorInputs"
          :error="contractsStore.currentErrorConstructorInputs"
          @deploy-contract="handleDeployContract"
          :deploying="contractsStore.deployingContract"
        />
      </div>
      <div class="flex flex-col">
        <div class="flex flex-col" v-show="contractsStore.deployedContract">
          <ContractState
            :abi="contractsStore.currentDeployedContractAbi"
            :contract-state="contractsStore.currentContractState"
            :deployed-contract="contractsStore.deployedContract"
            :get-contract-state="handleGetContractState"
            :calling-state="contractsStore.callingContractState"
          />
        </div>

        <div class="flex flex-col" v-show="contractsStore.deployedContract">
          <ExecuteTransactions
            :abi="contractsStore.currentDeployedContractAbi"
            @call-method="handleCallContractMethod"
            :calling-method="contractsStore.callingContractMethod"
          />
        </div>
        <TransactionsList
          :transactions="contractTransactions"
          @clear-transactions="handleClearTransactions"
        />
      </div>
    </div>

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
