<script setup lang="ts">
import { ref, computed } from 'vue';
import type { TransactionItem } from '@/types';
import TransactionStatusBadge from '@/components/Simulator/TransactionStatusBadge.vue';
import { useTimeAgo } from '@vueuse/core';
import ModalSection from '@/components/Simulator/ModalSection.vue';

const props = defineProps<{
  transaction: TransactionItem;
}>();

const isDetailsModalOpen = ref(false);

const timeThreshold = 6; // Number of hours after which the date should be displayed instead of time ago

const dateText = computed(() => {
  const currentDate = Date.now(); // Get the current timestamp in milliseconds
  const transactionDate = new Date(props.transaction.data.created_at).getTime(); // Convert transaction date to a timestamp
  const twelveHoursInMilliseconds = timeThreshold * 60 * 60 * 1000;

  if (currentDate - transactionDate > twelveHoursInMilliseconds) {
    return new Date(transactionDate).toLocaleString(); // Return formatted date string
  } else {
    return useTimeAgo(transactionDate).value; // Return time ago string (e.g., "3 hours ago")
  }
});

const leaderReceipt = computed(() => {
  return props.transaction?.data?.consensus_data?.leader_receipt;
});
</script>

<template>
  <div
    class="flex cursor-pointer items-center justify-between rounded p-0.5 pl-1 hover:bg-gray-100 dark:hover:bg-zinc-700"
    @click="isDetailsModalOpen = true"
  >
    <div class="text-xs font-medium">#{{ transaction.txId }}</div>

    <div class="flex items-center justify-between gap-2 p-1">
      <Loader :size="15" v-if="transaction.status !== 'FINALIZED'" />

      <div class="text-xs">
        {{
          transaction.type === 'method'
            ? transaction.data.data?.function_name
            : 'Deploy'
        }}
      </div>

      <TransactionStatusBadge>
        {{ transaction.status }}
      </TransactionStatusBadge>
    </div>

    <Modal :open="isDetailsModalOpen" @close="isDetailsModalOpen = false" wide>
      <div class="flex flex-row items-center justify-between gap-2">
        <div class="flex flex-col text-lg font-semibold">
          Transaction #{{ transaction.txId }}
          <span class="text-sm font-medium text-gray-400">
            {{
              transaction.type === 'method'
                ? 'Method Call'
                : 'Contract Deployment'
            }}
          </span>
        </div>

        <span class="text-[12px]">
          {{ dateText }}
        </span>
      </div>

      <div class="flex flex-col gap-4">
        <div class="mt-2 flex flex-col">
          <p
            class="text-md mb-1 flex flex-row items-center gap-2 font-semibold"
          >
            Status:
            <Loader :size="15" v-if="transaction.status !== 'FINALIZED'" />
            <TransactionStatusBadge>
              {{ transaction.status }}
            </TransactionStatusBadge>
          </p>
        </div>

        <ModalSection v-if="transaction.data.data">
          <template #title>Input</template>

          <pre
            class="overflow-hidden rounded bg-gray-200 p-1 text-xs text-gray-600 dark:bg-zinc-800 dark:text-gray-300"
            >{{ transaction.data.data }}</pre
          >
        </ModalSection>

        <ModalSection v-if="leaderReceipt">
          <template #title>
            Execution
            <TransactionStatusBadge
              :class="
                leaderReceipt.execution_result === 'ERROR'
                  ? '!bg-red-500'
                  : '!bg-green-500'
              "
            >
              {{ leaderReceipt.execution_result }}
            </TransactionStatusBadge>
          </template>

          <span class="text-sm font-semibold">Leader:</span>

          <div class="flex flex-row items-start gap-4 text-xs">
            <div>
              <div>
                <span class="font-medium">Gas used:</span>
                {{ leaderReceipt.gas_used }}
              </div>
              <div>
                <span class="font-medium"
                  >Stake: {{ leaderReceipt.node_config.stake }}</span
                >
              </div>
            </div>

            <div>
              <div>
                <span class="font-medium">Model:</span>
                {{ leaderReceipt.node_config.model }}
              </div>
              <div>
                <span class="font-medium">Provider:</span>
                {{ leaderReceipt.node_config.provider }}
              </div>
            </div>
          </div>
        </ModalSection>

        <ModalSection v-if="transaction.data.consensus_data">
          <template #title>Validators</template>

          <div
            class="divide-y overflow-hidden rounded border dark:border-gray-600"
          >
            <div
              class="flex flex-row items-center justify-between p-2 text-xs font-semibold dark:border-gray-600"
            >
              <div>Address</div>
              <div>Vote</div>
            </div>

            <div
              v-for="(vote, address) in transaction.data.consensus_data.votes"
              :key="address"
              class="flex flex-row items-center justify-between p-2 text-xs dark:border-gray-600"
            >
              <div>
                {{ address }}
              </div>
              <div>
                {{ vote }}
              </div>
            </div>
          </div>
        </ModalSection>

        <ModalSection v-if="leaderReceipt?.eq_outputs?.leader">
          <template #title>Equivalence Principle Output</template>

          <pre
            class="overflow-scroll rounded bg-gray-200 p-1 text-xs text-gray-600 dark:bg-zinc-800 dark:text-gray-300"
            >{{ leaderReceipt?.eq_outputs?.leader }}</pre
          >
        </ModalSection>
      </div>
    </Modal>
  </div>
</template>
