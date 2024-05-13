<script setup lang="ts">
import type { DeployedContract, ContractMethod } from '@/types'
import { computed, ref } from 'vue'

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
  getContractState: (contractAddress: string, method: string, methodArguments: string[]) => void
}>()

const inputParams = ref<{ [k: string]: any }>({})

const methodList = computed<ContractMethod[]>(() => {
  const list = Object.entries(props.abi?.methods || {})
    .filter((m) => m[0].startsWith('get_'))
    .map((m) => ({ name: m[0], inputs: m[1].inputs })) as ContractMethod[]
  return list
})

const getInputPlaceholder = (methodInputs: { [k: string]: string }) => {
  return Object.keys(methodInputs)
    .map((inputName) => `${inputName} ${methodInputs[inputName]}`)
    .join(', ')
}
</script>
<template>
  <div class="flex flex-col px-2 mt-6 py-2 w-full bg-slate-100">
    <h5 class="text-sm">Current Intelligent Contract State</h5>
  </div>
  <div class="flex flex-col p-2 overflow-y-auto">
    <div class="flex justify-start w-full px-1">
      <span class="text-xs text-primary">{{ deployedContract?.address }}</span>
    </div>
    <div v-if="deployedContract" class="flex flex-col w-full px-1 mt-2">
      <div v-for="method in methodList" :key="method.name">
        <div class="flex justify-between">
          <button
            @click="
              getContractState(
                deployedContract.address,
                method.name,
                inputParams[method.name] ? inputParams[method.name].split(',') : []
              )
            "
            class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded text-ellipsis w-[40%] overflow-hidden whitespace-nowrap"
          >
            {{ method.name }}
          </button>
          <input
            v-if="Object.keys(method.inputs).length > 0"
            v-model="inputParams[method.name]"
            :name="`${method.name}`"
            type="text"
            :placeholder="getInputPlaceholder(method.inputs)"
            class="bg-slate-100 dark:dark:bg-zinc-700 p-2 w-[60%]"
            label="Input"
          />
        </div>
        <div class="flex mt-2 mb-6">{{ contractState[method.name] }}</div>
      </div>
    </div>
  </div>
</template>
<style></style>
