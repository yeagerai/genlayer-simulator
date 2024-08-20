<script setup lang="ts">
import { useContractsStore } from '@/stores';
const contractStore = useContractsStore();
import { type ContractFile } from '@/types';
import { FolderOpenIcon } from '@heroicons/vue/16/solid';

defineProps<{
  contract: ContractFile;
  title: string;
}>();
</script>

<template>
  <div
    class="rounded-md border border-gray-300 bg-slate-100 p-2 dark:border-gray-800 dark:bg-gray-700 dark:bg-opacity-50"
  >
    <h4 class="text-sm font-semibold text-gray-500 dark:text-gray-400">
      {{ title }}
    </h4>

    <p class="my-2 text-xs">
      <slot />
    </p>

    <Btn secondary tiny @click="contractStore.openFile(contract.id)">
      <FolderOpenIcon class="h-3 w-3" />
      Open Contract
    </Btn>
  </div>
</template>
