<script setup lang="ts">
const props = defineProps<{
  transactions: any[]
}>()

</script>
<template>
  <div class="flex flex-col px-2 mt-6 py-2 w-full bg-slate-100">
    <h5 class="text-sm">Latest Transactions</h5>
  </div>
  <div class="flex flex-col p-2 m-h-20 overflow-y-auto">
    <div class="flex flex-col w-full px-1 mt-2">
      <div class="flex justify-between" v-for="(transaction, index) in props.transactions" :key="index">
        <div class="flex">{{ transaction }}: </div>
      </div>
    </div>
  </div>

</template>
<style></style>
