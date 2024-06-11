<script setup lang="ts">
import Modal from '@/components/ModalComponent.vue'
import { ref } from 'vue';
import JsonViewer from '@/components/JsonViewer/json-viewer.vue'
import { useUIStore } from '@/stores';
const props = defineProps<{
  transactions: any[]
}>()
const uiStore = useUIStore()
const selectedTransaction = ref<any>(null)

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
      class="flex flex-col text-xs w-full max-h-[98%] overflow-y-auto px-1 mt-2 scroll-smooth overscroll-contain snap-y  snap-start">
      <div class="flex flex-col m-1" v-for="transaction in props.transactions" :key="transaction.id">
        <div class="flex cursor-pointer  dark:text-white text-primary hover:underline" @click="handleSelectTransaction(transaction)">{{
        transaction.id }}</div>
      </div>
    </div>
  </div>
  <Modal :open="!!selectedTransaction" @close="handleCloseModal">
    <div class="flex flex-col">
      <div class="flex justify-between">
        <div class="text-xl">Transaction details</div>
        <div class=" dark:text-white text-primary">ID: {{ selectedTransaction?.id }}</div>
      </div>
      <div class="flex flex-col p-2 mt-2">
        <p class="text-md font-semibold">Status:</p>

        <div class="p-2 w-full bg-slate-100 overflow-y-auto">
          {{ selectedTransaction?.status }}
        </div>
        <div class="flex flex-col p-2 mt-2" v-if="selectedTransaction?.message">
        <p class="text-md font-semibold">Message:</p>

        <div class="p-2 w-full bg-slate-100 overflow-y-auto">
          {{ selectedTransaction?.message }}
        </div>
      </div>
      </div>
      <div class="flex flex-col p-2 mt-2">
        <p class="text-md font-semibold">Ouput:</p>
        <div class="p-2 max-h-64 w-full bg-slate-100 overflow-y-auto">
      <JsonViewer class="ml-2" :value="selectedTransaction?.data?.execution_output || {}"
                :theme="uiStore.mode === 'light' ? 'light' : 'dark'" :expand="true" sort />  
      </div>
      </div>
    </div>
  </Modal>
</template>
<style></style>
