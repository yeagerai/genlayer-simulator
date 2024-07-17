<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { InputTypesMap } from '@/utils'
import type { ContractMethod } from '@/types'
import LoadingIndicator from '@/components/LoadingIndicator.vue'
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
  callingMethod: boolean
  title: string
  mode: 'read' | 'write'
  contractState?: { [k: string]: any }
}

const props = defineProps<Props>()
const emit = defineEmits(['callMethod'])
const methodList = ref<ContractMethod[]>([])
const method = ref<ContractMethod>()

const inputs = computed<{ [k: string]: any }>(() => {
  return methodList.value.reduce((prev: any, curr) => {
    prev[curr.name] = {}
    return prev
  }, {})
})

watch(() => props.abi, (newValue) => {
  method.value = undefined
  methodList.value = Object.entries(newValue?.methods || {})
    .filter((m) => {
      if (props.mode === 'read') {
        return !m[0].startsWith('_') && m[0].startsWith('get_')

      }
      return !m[0].startsWith('_') && !m[0].startsWith('get_')
    })
    .map((m) => ({
      name: m[0],
      inputs: m[1].inputs
    }))
})


const handleMethodCall = () => {
  if (method.value) {
    const params = Object.values(inputs.value[method.value.name] || {})
    emit('callMethod', { method: method.value.name, params })
    inputs.value[method.value.name] = {}
  }
}


const onMethodChange = (event: Event) => {
  const selectedMethod = (event.target as HTMLSelectElement).value
  if (selectedMethod) {
    method.value = methodList.value.find((m) => m.name === selectedMethod)
  } else method.value = undefined
}

</script>

<template>
  <div class="flex flex-col px-2 mt-6 py-2 w-full bg-slate-100 dark:bg-zinc-700">
    <h5 class="text-sm">{{ title }}</h5>
  </div>
  <div class="flex flex-col p-2 overflow-y-auto">

    <div class="flex justify-start w-full mt-4">
      <select name="dropdown-execute-method" @change="onMethodChange" class="w-full dark:bg-zinc-700">
        <option value="">Select a method</option>
        <option v-for="method in methodList" :key="method.name" :value="method.name">
          {{ method.name }}()
        </option>
      </select>
    </div>
    <template v-if="method">
      <div class="flex flex-col mt-4 w-full">
        <div class="flex items-center py-2 justify-between" v-for="(inputType, input) in method.inputs" :key="input">
          <label :for="`${input}`" class="text-xs mr-2">{{ input }}</label>
          <input v-model="inputs[method.name][input]" :name="`${input}`" :type="InputTypesMap[inputType]"
            :placeholder="`${input}`" class="bg-slate-100 dark:dark:bg-zinc-700 p-2" label="Input" />
        </div>
      </div>
      <div class="flex flex-col mt-4 w-full">
        <ToolTip :text="`Execute ${method.name}()`" :options="{ placement: 'top' }" />
        <button @click="handleMethodCall"
          class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">
          <LoadingIndicator v-if="props.callingMethod" :color="'white'">
          </LoadingIndicator>
          <template v-else>Execute{{ ` ${method.name}` }}()</template>
        </button>
        <div class="flex mt-2 mb-6 justify-start items-center flex-wrap"
          v-if="props.mode === 'read' && props.contractState && props.contractState[method.name] !== undefined"
          :data-testid="`contract-state-item-${method.name}`"><span class="text-sm font-semibold mr-1">Result:</span> {{
      contractState?.[method.name] }}</div>
      </div>
    </template>
  </div>
</template>

<style>
.editor {
  width: 100% !important;
  min-height: 20rem !important;
}
</style>
