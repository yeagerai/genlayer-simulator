<script setup lang="ts">
import { ref, computed } from 'vue';
import { useContractsStore, useTransactionsStore } from '@/stores';
import { TrashIcon } from '@heroicons/vue/24/solid';
import TransactionItem from './TransactionItem.vue';
import PageSection from './PageSection.vue';
import EmptyListPlaceholder from '@/components/Simulator/EmptyListPlaceholder.vue';

const contractsStore = useContractsStore();
const transactionsStore = useTransactionsStore();

const transactions = computed(() => {
  const contractTransactions = transactionsStore.transactions.filter(
    (t) => t.localContractId === contractsStore.currentContractId,
  );

  const transactionsOrderedById = contractTransactions
    .slice()
    .sort((a, b) => b.txId - a.txId);

  return transactionsOrderedById;
});

const isClearTransactionsModalOpen = ref(false);

const handleClearTransactions = () => {
  transactionsStore.clearTransactionsForContract(
    contractsStore.currentContractId ?? '',
  );

  isClearTransactionsModalOpen.value = false;
};
</script>

<template>
  <PageSection data-testid="latest-transactions">
    <template #title>Transactions</template>
    <template #actions
      ><GhostBtn
        v-if="transactions.length > 0"
        @click="isClearTransactionsModalOpen = true"
        v-tooltip="'Clear Transactions List'"
      >
        <TrashIcon class="h-4 w-4" /></GhostBtn
    ></template>

    <TransactionItem
      v-for="transaction in transactions"
      :key="transaction.txId"
      :transaction="transaction"
    />

    <EmptyListPlaceholder v-if="transactions.length === 0">
      No transactions yet.
    </EmptyListPlaceholder>

    <ConfirmationModal
      :open="isClearTransactionsModalOpen"
      @close="isClearTransactionsModalOpen = false"
      @confirm="handleClearTransactions"
      buttonText="Clear Transactions"
      dangerous
    >
      <template #title>Clear Transaction List</template>
      <template #description
        >Are you sure you want to clear all transactions?</template
      >
    </ConfirmationModal>
  </PageSection>
</template>
