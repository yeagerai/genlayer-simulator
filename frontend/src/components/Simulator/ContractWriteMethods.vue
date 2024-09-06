<script setup lang="ts">
import { useContractQueries } from '@/hooks';
import { computed } from 'vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { type ContractMethod } from '@/types';
import ContractMethodItem from '@/components/Simulator/ContractMethodItem.vue';
import EmptyListPlaceholder from '@/components/Simulator/EmptyListPlaceholder.vue';

const { contractAbiQuery } = useContractQueries();

const { data, isPending, isError, error, isRefetching } = contractAbiQuery;

const writeMethods = computed(() => {
  return data.value.abi
    .filter((method: ContractMethod) => method.type !== 'constructor')
    .filter(
      (method: ContractMethod) =>
        !method.name.startsWith('get_') && !method.name.startsWith('_'),
    );
});
</script>

<template>
  <PageSection>
    <template #title
      >Write Methods

      <Loader v-if="isRefetching" :size="14" />
    </template>

    <ContentLoader v-if="isPending" />

    <Alert v-else-if="isError" error>
      {{ error?.message }}
    </Alert>

    <template v-else-if="data">
      <ContractMethodItem
        v-for="method in writeMethods"
        :key="method.name"
        :method="method"
        methodType="write"
      />

      <EmptyListPlaceholder v-if="writeMethods.length === 0">
        No read methods.
      </EmptyListPlaceholder>
    </template>
  </PageSection>
</template>
