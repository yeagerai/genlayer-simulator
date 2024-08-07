<script setup lang="ts">
import { ref } from 'vue';
import JsonViewer from '@/components/JsonViewer/json-viewer.vue';
import { useUIStore } from '@/stores';
import type { TransactionItem } from '@/types';

const uiStore = useUIStore();

defineProps<{
  transaction: TransactionItem;
}>();

const isDetailsModalOpen = ref(false);
</script>

<template>
  <div
    class="flex cursor-pointer items-center justify-between rounded-sm p-1 hover:bg-gray-100 dark:hover:bg-zinc-700"
    @click="isDetailsModalOpen = true"
  >
    #{{ transaction.txId }}
    <div class="flex items-center justify-between p-1">
      <VueSpinnerOval
        size="15"
        v-if="transaction.status !== 'FINALIZED'"
        :color="uiStore.mode === 'light' ? '#1a3851' : 'white'"
      />
      <span class="ml-1 text-xs font-semibold">{{ transaction.status }}</span>
    </div>

    <Modal :open="isDetailsModalOpen" @close="isDetailsModalOpen = false" wide>
      <template #title>Transaction #{{ transaction.txId }}</template>

      <div class="flex flex-col">
        <div class="mt-2 flex flex-col">
          <p class="text-md mb-1 font-semibold">
            Status: {{ transaction.status }}
          </p>
        </div>

        <div class="mt-2 flex flex-col">
          <p class="text-md mb-1 font-semibold">Ouput:</p>
          <JsonViewer
            class="overflow-y-auto rounded-md p-2"
            :value="transaction.data || {}"
            :theme="uiStore.mode === 'light' ? 'light' : 'dark'"
            :expand="true"
            sort
          />
        </div>
      </div>
    </Modal>
  </div>
</template>
