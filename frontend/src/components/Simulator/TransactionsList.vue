<script setup lang="ts">
import { ref } from 'vue';
import type { TransactionItem as TransactionItemType } from '@/types';
import { TrashIcon } from '@heroicons/vue/24/solid';
import TransactionItem from './TransactionItem.vue';
import PageSection from './PageSection.vue';
import EmptyListPlaceholder from '@/components/Simulator/EmptyListPlaceholder.vue';

const props = defineProps<{
  transactions: TransactionItemType[];
}>();

const emit = defineEmits(['clear-transactions']);

const isClearTransactionsModalOpen = ref(false);

const handleClearTransactions = () => {
  emit('clear-transactions');
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
      v-for="transaction in props.transactions"
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
