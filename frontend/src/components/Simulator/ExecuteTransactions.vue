<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { InputTypesMap } from '@/utils'
import { useMainStore } from '@/stores'
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
}

const store = useMainStore()
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
  methodList.value =  Object.entries(newValue?.methods || {})
    .filter((m) => !m[0].startsWith('_') && !m[0].startsWith('get_'))
    .map((m) => ({
      name: m[0],
      inputs: m[1].inputs
    }))
})


const handleMethodCall = () => {
  if (method.value) {
    const params = Object.values(inputs.value[method.value.name] || {})
    emit('callMethod', { method: method.value.name, params })
  }
}


const onMethodChange = (event: Event) => {
  const selectedMethod = (event.target as HTMLSelectElement).value
  if (selectedMethod) {
    method.value = methodList.value.find((m) => m.name === selectedMethod)
  } else method.value = undefined
}

const setCurentUserAddress = (event: Event) => {
  if ((event.target as HTMLSelectElement)?.value) {
    store.currentUserAddress = (event.target as HTMLSelectElement)?.value
  }
}
</script>

<template>
  <div class="flex flex-col px-2 mt-6 py-2 w-full bg-slate-100 dark:bg-zinc-700">
    <h5 class="text-sm">Execute transactions</h5>
  </div>
  <div class="flex flex-col p-2 overflow-y-auto">
    <div class="flex flex-col items-start w-full">
      <p>Current Account:</p>
      <select name="" id="" @change="setCurentUserAddress" class="text-xs w-full dark:bg-zinc-700"
        :value="store.currentUserAddress">
        <option v-for="account in store.accounts" :key="account" :value="account">
          {{ account }}
        </option>
      </select>
    </div>
    <div class="flex justify-start w-full mt-4">
      <select name="" id="" @change="onMethodChange" class="w-full dark:bg-zinc-700">
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
          <template v-else>Execute {{ ` ${method.name}` }}()</template>
        </button>
      </div>
    </template>
    <div id="tutorial-creating-transactions" class="flex"></div>
  </div>
</template>

<style>
.editor {
  width: 100% !important;
  min-height: 20rem !important;
}
</style>
