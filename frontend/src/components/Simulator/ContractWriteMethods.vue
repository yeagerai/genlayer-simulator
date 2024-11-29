<script setup lang="ts">
import { useContractQueries } from '@/hooks';
import { computed } from 'vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { type ContractMethod } from '@/types';
import ContractMethodItem from '@/components/Simulator/ContractMethodItem.vue';
import EmptyListPlaceholder from '@/components/Simulator/EmptyListPlaceholder.vue';

const props = defineProps<{
  leaderOnly: boolean;
}>();

const { contractAbiQuery } = useContractQueries();

const { data, isPending, isError, error, isRefetching } = contractAbiQuery;

const writeMethods = computed(() => {
  return Object.entries(
    data.value.methods as { [key: string]: ContractMethod },
  ).filter((x) => !x[1].readonly);
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
        :name="method[0]"
        :key="method[0]"
        :method="method[1]"
        methodType="write"
        :leaderOnly="props.leaderOnly"
      />

      <EmptyListPlaceholder v-if="writeMethods.length === 0">
        No read methods.
      </EmptyListPlaceholder>
    </template>
  </PageSection>
</template>
