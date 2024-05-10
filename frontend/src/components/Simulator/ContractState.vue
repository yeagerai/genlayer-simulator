<script setup lang="ts">
import type { DeployedContract } from '@/types'
import { computed } from 'vue'

interface Abi {
  methods: {
    [k: string]: {
      inputs: { [k: string]: string }
    }
  }
  class: string
}

const props = defineProps<{
  abi?: Abi
  contractState: any
  deployedContract?: DeployedContract
  getContractState: (contractAddress: string, method: string) => void
}>()

const methodList = computed<string[]>(() => {
  const list = Object.entries(props.abi?.methods || {})
    .filter((m) => m[0].startsWith('get_'))
    .map((m) => m[0])
  return list
})
</script>
<template>
  <div class="flex flex-col px-2 mt-6 py-2 w-full bg-slate-100 dark:bg-zinc-700" id="tutorial-contract-state">
    <h5 class="text-sm">Current Intelligent Contract State</h5>
  </div>
  <div class="flex flex-col p-2 overflow-y-auto">
    <div class="flex justify-start w-full px-1">
      <span class="text-xs  dark:text-white text-primary">{{ deployedContract?.address }}</span>
    </div>
    <div v-if="deployedContract" class="flex flex-col w-full px-1 mt-2">
      <div class="flex justify-between mt-2" v-for="method in methodList" :key="method">
        <button
          @click="getContractState(deployedContract.address, method)"
          class="bg-primary m-w-[50%] hover:opacity-80 text-white font-semibold px-4 py-2 rounded"
        >
          {{ method }}
        </button>
        <div class="flex ml-2 flex-1 justify-end">{{ contractState[method] }}</div>
      </div>
    </div>
  </div>
</template>
<style></style>
