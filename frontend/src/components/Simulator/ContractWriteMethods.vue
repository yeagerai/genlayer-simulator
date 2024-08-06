<script setup lang="ts">
import { useContractQueries } from '@/hooks/useContractQueries';
import { computed } from 'vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { type ContractMethod } from '@/types';
import ContractMethodItem from '@/components/Simulator/ContractMethodItem.vue';
import EmptyListPlaceholder from '@/components/Simulator/EmptyListPlaceholder.vue';

const { contractAbiQuery } = useContractQueries();

const { data, isLoading  } = contractAbiQuery;

const writeMethods = computed(() => {
  return Object.entries(data.value.methods)
    .filter((m) => !m[0].startsWith('_') && !m[0].startsWith('get_'))
    .map(([methodName, method]) => ({
      methodName,
      method: method as ContractMethod,
    }));
});
</script>

<template>
  <PageSection v-if="data">
    <template #title>Write Methods</template>

    <div v-if="isLoading">Loading...</div>

    <ContractMethodItem
      v-for="method in writeMethods"
      :key="method.methodName"
      :methodName="method.methodName"
      :method="method.method"
      methodType="write"
    />

    <EmptyListPlaceholder v-if="writeMethods.length === 0">
      No read methods.
    </EmptyListPlaceholder>
  </PageSection>
</template>
