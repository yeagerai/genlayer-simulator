<script setup lang="ts">
import Modal from '@/components/ModalComponent.vue'
import { ref } from 'vue';

const props = defineProps<{
  transactions: any[]
}>()

const selectedTransaction = ref<any>(null)

const handleSelectTransaction = (transaction: any) => {
  selectedTransaction.value = transaction
}

const handleCloseModal = () => {
  selectedTransaction.value = null
}

</script>
<template>
  <div class="flex flex-col px-2 mt-6 py-2 w-full bg-slate-100">
    <h5 class="text-sm">Latest Transactions</h5>
  </div>
  <div class="flex flex-col p-2">
    <div
      class="flex flex-col text-xs w-full max-h-[98%] overflow-y-auto px-1 mt-2 scroll-smooth overscroll-contain snap-y  snap-start">
      <div class="flex flex-col m-1" v-for="transaction in props.transactions" :key="transaction.id">
        <div class="flex cursor-pointer text-primary hover:underline" @click="handleSelectTransaction(transaction)">{{
        transaction.id }}</div>
      </div>
    </div>
  </div>
  <Modal :open="!!selectedTransaction" @close="handleCloseModal">
    <div class="flex flex-col">
      <div class="flex justify-between">
        <div class="text-xl">Transaction details</div>
        <div class="text-primary">ID: {{ selectedTransaction?.id }}</div>
      </div>
      <div class="flex flex-col p-2 mt-2">
        <p class="text-md font-semibold">Result:</p>

        <div class="p-2 w-full bg-slate-100 overflow-y-auto">
          {{ selectedTransaction?.result.message }}
        </div>
      </div>
      <div class="flex flex-col p-2 mt-2">
        <p class="text-md font-semibold">Ouput:</p>
        <div class="p-2 max-h-64 w-full bg-slate-100 overflow-y-auto">{{
        JSON.stringify(selectedTransaction?.result?.execution_output || {}, null, 2) }}</div>
      </div>
    </div>
  </Modal>
</template>
<style></style>
