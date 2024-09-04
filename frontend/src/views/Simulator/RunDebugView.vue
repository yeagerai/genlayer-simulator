<script setup lang="ts">
import ConstructorParameters from '@/components/Simulator/ConstructorParameters.vue';
import ContractReadMethods from '@/components/Simulator/ContractReadMethods.vue';
import ContractWriteMethods from '@/components/Simulator/ContractWriteMethods.vue';
import TransactionsList from '@/components/Simulator/TransactionsList.vue';
import { useContractQueries } from '@/hooks';
import MainTitle from '@/components/Simulator/MainTitle.vue';
import { ref, watch } from 'vue';
import { useContractsStore, useNodeStore } from '@/stores';
import ContractInfo from '@/components/Simulator/ContractInfo.vue';

const contractsStore = useContractsStore();
const { isDeployed, address, contract } = useContractQueries();
const nodeStore = useNodeStore();

const isDeploymentOpen = ref(!isDeployed.value);

// Hide constructors by default when contract is already deployed
const setConstructorVisibility = () => {
  isDeploymentOpen.value = !isDeployed.value;
};

watch(
  [() => contract.value?.id, () => isDeployed.value, () => address.value],
  setConstructorVisibility,
);
</script>

<template>
  <div class="flex max-h-[93vh] w-full flex-col overflow-y-auto">
    <MainTitle data-testid="run-debug-page-title">Run and Debug</MainTitle>

    <template
      v-if="contractsStore.currentContract && contractsStore.currentContractId"
    >
      <ContractInfo
        :showNewDeploymentButton="!isDeploymentOpen"
        @openDeployment="isDeploymentOpen = true"
      />

      <template v-if="nodeStore.hasAtLeastOneValidator">
        <ConstructorParameters
          id="tutorial-how-to-deploy"
          v-if="isDeploymentOpen"
          @deployedContract="isDeploymentOpen = false"
        />

        <ContractReadMethods v-if="isDeployed" id="tutorial-read-methods" />
        <ContractWriteMethods v-if="isDeployed" id="tutorial-write-methods" />
        <TransactionsList id="tutorial-tx-response" />
      </template>
    </template>

    <div
      v-else
      class="flex w-full flex-col bg-slate-100 px-2 py-2 dark:dark:bg-zinc-700"
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
