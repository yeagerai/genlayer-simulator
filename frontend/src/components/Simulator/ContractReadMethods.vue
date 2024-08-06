<script setup lang="ts">
import { useContractQueries } from '@/hooks/useContractQueries';
import { computed } from 'vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { type ContractMethod } from '@/types';
import ContractMethodItem from '@/components/Simulator/ContractMethodItem.vue';
import EmptyListPlaceholder from '@/components/Simulator/EmptyListPlaceholder.vue';

const { contractAbiQuery } = useContractQueries();

const { data, isLoading } = contractAbiQuery;

const readMethods = computed(() => {
  return Object.entries(data.value.methods)
    .filter((m) => m[0].startsWith('get_'))
    .map(([methodName, method]) => ({
      methodName,
      method: method as ContractMethod, // Explicitly type 'method' as 'ContractMethod'
    }));
});
</script>

<template>
  <PageSection v-if="data">
    <template #title>Read Methods</template>

    <div v-if="isLoading">Loading...</div>

    <ContractMethodItem
      v-for="method in readMethods"
      :key="method.methodName"
      :methodName="method.methodName"
      :method="method.method"
      methodType="read"
    />

    <EmptyListPlaceholder v-if="readMethods.length === 0">
      No read methods.
    </EmptyListPlaceholder>
  </PageSection>
</template>
