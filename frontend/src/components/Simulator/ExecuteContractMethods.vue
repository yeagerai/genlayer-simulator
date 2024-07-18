<script setup lang="ts">
import { ref, watch } from 'vue'
import type { ContractMethod } from '@/types'
import ContractMethods from '@/components/Simulator/ContractMethods.vue'

interface Abi {
  methods: {
    [k: string]: {
      inputs: { [k: string]: string }
    }
  }
  class: string
}

interface Props {
  abi?: Abi
  callingGetter: boolean
  callingWriter: boolean
  contractState?: { [k: string]: any }
}

const props = defineProps<Props>()
const emit = defineEmits(['callWriter', 'callGetter'])
const getters = ref<ContractMethod[]>([])
const writers = ref<ContractMethod[]>([])

watch(() => props.abi, (newValue) => {
  const methods = Object.entries(newValue?.methods || {})
  getters.value = methods
    .filter((m) => !m[0].startsWith('_') && m[0].startsWith('get_'))
    .map((m) => ({
      name: m[0],
      inputs: m[1].inputs
    }))
  writers.value = methods
    .filter((m) => !m[0].startsWith('_') && !m[0].startsWith('get_'))
    .map((m) => ({
      name: m[0],
      inputs: m[1].inputs
    }))
})

const handleWriterCall = ({ method, params }: { method: string; params: any[] }) => {
  if (method) {
    emit('callWriter', { method, params })
  }
}

const handleGetterCall = ({ method, params }: { method: string; params: any[] }) => {
  if (method) {
    emit('callGetter', { method, params })
  }
}
</script>

<template>
  <div class="flex flex-col">
    <ContractMethods title="Read Methods" :methods="getters" @call-method="handleGetterCall" :loading="callingGetter">
      <template #results="{ methodName }">
        <div class="flex mt-2 justify-start items-center flex-wrap"
          v-if="props.contractState && props.contractState[methodName] !== undefined"
          :data-testid="`contract-state-item-${methodName}`">
          <span class="text-sm font-semibold mr-1">Result:</span>
          {{ props.contractState[methodName] }}
        </div>
      </template>
    </ContractMethods>
  </div>

  <div class="flex flex-col">
    <ContractMethods title="Execute Transactions" :methods="writers" @call-method="handleWriterCall"
      :loading="callingWriter" />
    <div id="tutorial-creating-transactions" class="flex"></div>
  </div>
</template>

<style>
.editor {
  width: 100% !important;
  min-height: 20rem !important;
}
</style>
