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
import { ref, watch } from 'vue';
import { PlusIcon } from '@heroicons/vue/16/solid';
import { shortenAddress } from '@/utils';
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

const showDeployment = ref(!isDeployed.value);

// Hide constructors by default when contract is already deployed
const setConstructorVisibility = () => {
  showDeployment.value = !isDeployed.value;
};

watch(
  [() => contract.value?.id, () => isDeployed.value, () => address.value],
  setConstructorVisibility,
);
</script>

<template>
  <!-- <AccountSelect /> -->
  <PageSection>
    <template #title
      >Contract
      <div class="opacity-50">{{ contract?.name }}</div></template
    >

    <div v-if="isDeployed" class="flex flex-row items-center gap-1 text-xs">
      <CheckCircleIcon class="h-4 w-4 shrink-0 text-emerald-400" />

      Deployed at

      <div class="font-semibold">
        {{ shortenAddress(address) }}
      </div>

      <CopyTextButton :text="address" />
    </div>

    <EmptyListPlaceholder v-else>Not deployed yet.</EmptyListPlaceholder>

    <Btn
      secondary
      tiny
      class="inline-flex w-auto shrink grow-0"
      v-if="!showDeployment"
      @click="showDeployment = true"
    >
      <PlusIcon class="h-4 w-4 shrink-0" />
      New Deployment
    </Btn>
  </PageSection>

  <ContractDeployment v-if="showDeployment" />
  <ContractReadMethods />
  <ContractWriteMethods />
  <TransactionsList />
</template>
