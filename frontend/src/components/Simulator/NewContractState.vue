<script setup lang="ts">
import ContractDeployment from '@/components/Simulator/ContractDeployment.vue';
import ContractReadMethods from '@/components/Simulator/ContractReadMethods.vue';
import ContractWriteMethods from '@/components/Simulator/ContractWriteMethods.vue';
import TransactionsList from '@/components/Simulator/TransactionsList.vue';
// import AccountSelect from '@/components/Simulator/AccountSelect.vue'; //
import { useContractQueries } from '@/hooks/useContractQueries';
import PageSection from './PageSection.vue';
import { CheckCircleIcon } from '@heroicons/vue/24/outline';
import EmptyListPlaceholder from './EmptyListPlaceholder.vue';

// TODO: add account select
// TODO: constructor form
// TODO: methods form

// FIXME: deployment should replace contract, not clear the store
// FIXME: add notification for deployment start...
const {
  schema,
  contractSchemaQuery,
  deployContract,
  contractAbiQuery,
  // constructorInputs,
  isDeployed,
  isDeploying,
  address,
  contract,
} = useContractQueries();
</script>

<template>
  <!-- <AccountSelect /> -->
  <PageSection>
    <template #title
      >Contract
      <div class="opacity-50">{{ contract?.name }}</div></template
    >

    <div v-if="isDeployed">
      <CheckCircleIcon class="h-4 w-4 text-green-500" />
      Deployed at:
      <div class="truncate text-xs">
        {{ address }}
        <ToolTip :text="address" />
      </div>
    </div>
  </PageSection>

  <ContractDeployment />
  <ContractReadMethods />
  <ContractWriteMethods />
  <TransactionsList />
</template>
