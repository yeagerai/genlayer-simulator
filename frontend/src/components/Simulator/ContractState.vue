<script setup lang="ts">
import type { DeployedContract } from '@/types';
import { ref, watch } from 'vue'

const props = defineProps<{
  contractState: any,
  deployedContract?: DeployedContract
}>()

const stateItems = ref<{ name: string; value: any }[]>([])

watch(
  () => props.contractState,
  (newValue) => {
    if (newValue && Object.keys(newValue).length > 0) {
      stateItems.value = Object.entries(newValue).map((item) => ({ name: item[0], value: item[1] }))
    }
  }
)
</script>
<template>
  <div class="flex flex-col px-2 mt-6 py-2 w-full bg-slate-100">
    <h5 class="text-sm">Current Intelligent Contract State</h5>
  </div>
  <div class="flex flex-col p-2 overflow-y-auto">
    <div class="flex justify-start w-full px-1">
      <span class="text-xs text-primary">{{ deployedContract?.address }}</span>
    </div>
    <div class="flex flex-col w-full px-1 mt-2">
      <div class="flex justify-between" v-for="item in stateItems" :key="item.name">
        <div class="flex">{{ item.name }}: </div>
        <div class="flex">{{ item.value }}</div>
      </div>
    </div>
  </div>

</template>
<style></style>
