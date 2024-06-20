<script setup lang="ts">
import Modal from '@/components/ModalComponent.vue'
import { ref } from 'vue';
import JsonViewer from '@/components/JsonViewer/json-viewer.vue'
import { useUIStore } from '@/stores';
import type { TransactionItem } from '@/types';

const props = defineProps<{
  transactions: TransactionItem[]
}>()
const uiStore = useUIStore()
const selectedTransaction = ref<TransactionItem | null>(null)

const handleSelectTransaction = (transaction: any) => {
  selectedTransaction.value = transaction
}

const handleCloseModal = () => {
  selectedTransaction.value = null
}

</script>
<template>
  <div class="flex flex-col px-2 mt-6 py-2 w-full bg-slate-100 dark:bg-zinc-700" id="tutorial-tx-response">
    <h5 class="text-sm">Latest Transactions</h5>
  </div>
  <div class="flex flex-col p-2">
    <div
      class="flex flex-col text-xs w-full max-h-[98%] overflow-y-auto mt-2 scroll-smooth overscroll-contain snap-y  snap-start">
      <div class="flex flex-col p-1" v-for="transaction in props.transactions" :key="transaction.txId">
        <div class="flex cursor-pointer dark:text-white text-primary hover:bg-slate-100 items-center justify-between"
          @click="handleSelectTransaction(transaction)">#{{
        transaction.txId }} <div class="p-1 justify-between flex items-center">
            <VueSpinnerOval size="15" v-if="transaction.status !== 'FINALIZED'"
              :color="uiStore.mode === 'light' ? '#1a3851' : 'white'" />
            <span class="text-xs ml-1 font-semibold">{{ transaction.status }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
  <Modal :open="!!selectedTransaction" @close="handleCloseModal">
    <div class="flex flex-col">
      <div class="flex justify-between">
        <div class="text-xl">Transaction details</div>
        <div class=" dark:text-white text-primary">ID: {{ selectedTransaction?.txId }}</div>
      </div>
      <div class="flex flex-col p-2 mt-2">
        <p class="text-md font-semibold">Status:</p>

        <div class="p-2 w-full bg-slate-100 overflow-y-auto">
          {{ selectedTransaction?.status }}
        </div>
      </div>
      <div class="flex flex-col p-2 mt-2">
        <p class="text-md font-semibold">Ouput:</p>
        <div class="p-2 max-h-64 w-full bg-slate-100 overflow-y-auto">
          <JsonViewer class="ml-2" :value="selectedTransaction?.data || {}"
            :theme="uiStore.mode === 'light' ? 'light' : 'dark'" :expand="true" sort />
        </div>
      </div>
    </div>
  </Modal>
</template>
<style></style>
