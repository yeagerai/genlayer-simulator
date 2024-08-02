<script setup lang="ts">
import { ref, computed } from 'vue';
import { useContractsStore, useTransactionsStore } from '@/stores';
import { TrashIcon } from '@heroicons/vue/24/solid';
import TransactionItem from './TransactionItem.vue';
import PageSection from './PageSection.vue';
import EmptyListPlaceholder from '@/components/Simulator/EmptyListPlaceholder.vue';

const contractsStore = useContractsStore();
const transactionsStore = useTransactionsStore();

const transactions = computed(() =>
  transactionsStore.transactions.filter(
    (t) => t.localContractId === contractsStore.currentContractId,
  ),
);

const isClearTransactionsModalOpen = ref(false);

// FIXME: cherry pick persistency fix
const handleClearTransactions = () => {
  transactionsStore.processingQueue = transactionsStore.processingQueue.filter(
    (t) => t.localContractId !== contractsStore.currentContractId,
  );
  transactionsStore.transactions = transactionsStore.transactions.filter(
    (t) => t.localContractId !== contractsStore.currentContractId,
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
      >
        <TrashIcon class="h-4 w-4" />
        <ToolTip
          text="Clear Transactions List"
          :options="{ placement: 'bottom' }" /></GhostBtn
    ></template>

    <TransactionItem
      v-for="transaction in transactions"
      :key="transaction.txId"
      :transaction="transaction"
    />

    <EmptyListPlaceholder v-if="transactions.length === 0">
      No transactions yet.
    </EmptyListPlaceholder>
  </PageSection>

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
</template>
