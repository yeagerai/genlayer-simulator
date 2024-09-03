<script setup lang="ts">
import { useContractQueries } from '@/hooks';
import { computed } from 'vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { type ContractMethod } from '@/types';
import ContractMethodItem from '@/components/Simulator/ContractMethodItem.vue';
import EmptyListPlaceholder from '@/components/Simulator/EmptyListPlaceholder.vue';

const { contractAbiQuery } = useContractQueries();

const { data, isPending, isError, error, isRefetching } = contractAbiQuery;

const readMethods = computed(() => {
  return data.value.abi
    .filter((method: ContractMethod) => method.type !== 'constructor')
    .filter((method: ContractMethod) => method.name.startsWith('get_'));
});
</script>

<template>
  <PageSection data-testid="contract-read-methods">
    <template #title
      >Read Methods
      <Loader v-if="isRefetching" :size="14" />
    </template>

    <ContentLoader v-if="isPending" />

    <Alert v-else-if="isError" error>
      {{ error?.message }}
    </Alert>

    <template v-else-if="data">
      <ContractMethodItem
        v-for="method in readMethods"
        :key="method.name"
        :method="method"
        methodType="read"
      />

      <EmptyListPlaceholder v-if="readMethods.length === 0">
        No read methods.
      </EmptyListPlaceholder>
    </template>
  </PageSection>
</template>
