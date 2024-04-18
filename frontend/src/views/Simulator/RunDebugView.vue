<script setup lang="ts">
import { useContractsFilesStore } from "@/stores"
import { computed } from "vue";
const store = useContractsFilesStore()
const contract = computed(() => store.contracts.find(contract => contract.id === store.currentContractId))
</script>

<template>
  <div class="flex flex-col w-full">
    <div class="flex flex-col p-2 w-full">
      <h3 class="text-xl">Run and Debug</h3>
    </div>
    <div class="flex flex-col px-2 py-2 w-full bg-slate-100">
      <div>Intelligent Contract:</div>
      <div class="text-xs text-neutral-800">
        {{ contract?.name }}.gpy
      </div>
    </div>
    <div class="flex flex-col mt-4 p-2 w-full justify-center">
      <ToolTip text="Deploy" :options="{ placement: 'top' }" />
      <button class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">Deploy Intelligent
        Contract</button>
    </div>
  </div>
</template>
