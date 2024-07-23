<script setup lang="ts">
import type { DeployedContract, ContractMethod } from '@/types'
import { computed, ref } from 'vue'
import LoadingIndicator from '@/components/LoadingIndicator.vue'

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
  getContractState: (
    contractAddress: string,
    method: string,
    methodArguments: string[]
  ) => void
  callingState: boolean
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
  <div
    class="mt-6 flex w-full flex-col bg-slate-100 px-2 py-2 dark:bg-zinc-700"
    id="tutorial-contract-state"
  >
    <h5 class="text-sm">Current Intelligent Contract State</h5>
  </div>
  <div class="flex flex-col overflow-y-auto p-2">
    <div class="flex w-full justify-start px-1">
      <span class="text-xs text-primary dark:text-white">{{
        deployedContract?.address
      }}</span>
    </div>
    <div v-if="deployedContract" class="mt-2 flex w-full flex-col px-1">
      <div v-for="method in methodList" :key="method.name" class="flex">
        <div class="flex flex-1 justify-between">
          <button
            @click="
              getContractState(
                deployedContract.address,
                method.name,
                inputParams[method.name]
                  ? inputParams[method.name].split(',')
                  : []
              )
            "
            class="w-[40%] overflow-hidden text-ellipsis whitespace-nowrap rounded bg-primary px-4 py-2 font-semibold text-white hover:opacity-80"
          >
            <LoadingIndicator v-if="props.callingState" :color="'white'" />
            <template v-else>{{ method.name }}</template>
          </button>
          <input
            v-if="Object.keys(method.inputs).length > 0"
            v-model="inputParams[method.name]"
            :name="`${method.name}`"
            type="text"
            :placeholder="getInputPlaceholder(method.inputs)"
            class="w-[60%] bg-slate-100 p-2 dark:dark:bg-zinc-700"
            label="Input"
          />
        </div>
        <div
          class="mb-6 mt-2 flex"
          :data-testid="`contract-state-item-${method.name}`"
        >
          {{ contractState[method.name] }}
        </div>
      </div>
    </div>
  </div>
</template>
<style></style>
