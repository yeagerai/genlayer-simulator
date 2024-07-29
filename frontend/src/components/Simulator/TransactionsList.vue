<script setup lang="ts">
import { ref } from 'vue';
import JsonViewer from '@/components/JsonViewer/json-viewer.vue';
import { useUIStore } from '@/stores';
import type { TransactionItem } from '@/types';
import { TrashIcon } from '@heroicons/vue/24/solid';

const props = defineProps<{
  transactions: TransactionItem[];
}>();
const emit = defineEmits(['clear-transactions']);
const uiStore = useUIStore();
const selectedTransaction = ref<TransactionItem | null>(null);
const clearTransactionsModalOpen = ref(false);

const openClearTransactionsModal = () => {
  clearTransactionsModalOpen.value = true;
};

const closeClearTransactionsModal = () => {
  clearTransactionsModalOpen.value = false;
};

const handleSelectTransaction = (transaction: any) => {
  selectedTransaction.value = transaction;
};

const handleClearTransactions = () => {
  emit('clear-transactions');
  setTimeout(() => {
    closeClearTransactionsModal();
  }, 500);
};

const handleCloseModal = () => {
  selectedTransaction.value = null;
};
</script>
<template>
  <div
    class="mt-6 flex w-full items-center justify-between bg-slate-100 px-2 py-2 dark:bg-zinc-700"
    id="tutorial-tx-response"
  >
    <h5 class="text-sm">Latest Transactions</h5>
    <button @click="openClearTransactionsModal" v-if="transactions.length > 0">
      <ToolTip
        text="Clear Transactions List"
        :options="{ placement: 'bottom' }"
      />
      <TrashIcon class="mr-1 h-4 w-4" />
    </button>
  </div>
  <div class="flex flex-col p-2">
    <div
      class="mt-2 flex max-h-[98%] w-full snap-y snap-start flex-col-reverse overflow-y-auto overscroll-contain scroll-smooth text-xs"
    >
      <div
        class="flex flex-col p-1"
        v-for="transaction in props.transactions"
        :key="transaction.txId"
      >
        <div
          class="flex cursor-pointer items-center justify-between text-primary hover:bg-slate-100 dark:text-white"
          @click="handleSelectTransaction(transaction)"
        >
          #{{ transaction.txId }}
          <div class="flex items-center justify-between p-1">
            <VueSpinnerOval
              size="15"
              v-if="transaction.status !== 'FINALIZED'"
              :color="uiStore.mode === 'light' ? '#1a3851' : 'white'"
            />
            <span class="ml-1 text-xs font-semibold">{{
              transaction.status
            }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
  <Modal :open="!!selectedTransaction" @close="handleCloseModal">
    <div class="flex flex-col">
      <div class="flex justify-between">
        <div class="text-xl">Transaction details</div>
        <div class="text-primary dark:text-white">
          ID: {{ selectedTransaction?.txId }}
        </div>
      </div>
      <div class="mt-2 flex flex-col p-2">
        <p class="text-md font-semibold">Status:</p>

        <div class="w-full overflow-y-auto bg-slate-100 p-2">
          {{ selectedTransaction?.status }}
        </div>
      </div>
      <div class="mt-2 flex flex-col p-2">
        <p class="text-md font-semibold">Ouput:</p>
        <div class="max-h-64 w-full overflow-y-auto bg-slate-100 p-2">
          <JsonViewer
            class="ml-2"
            :value="selectedTransaction?.data || {}"
            :theme="uiStore.mode === 'light' ? 'light' : 'dark'"
            :expand="true"
            sort
          />
        </div>
      </div>
    </div>
  </Modal>
  <Modal
    :open="clearTransactionsModalOpen"
    @close="closeClearTransactionsModal"
  >
    <div class="flex flex-col">
      <div class="flex justify-between">
        <div class="text-xl">Clear Transactions List</div>
      </div>
      <div class="mt-4 flex justify-between bg-slate-100 p-2 font-bold">
        Are you sure you want to clear the transactions list?
      </div>
    </div>
    <div class="mt-4 flex w-full flex-col">
      <Btn @click="handleClearTransactions"> Clear Transactions List </Btn>
    </div>
  </Modal>
</template>
<style></style>
