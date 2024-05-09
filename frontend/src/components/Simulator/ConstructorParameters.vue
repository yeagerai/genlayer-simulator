<script setup lang="ts">
import { ref, defineEmits, watch, onMounted } from 'vue'
import { InputTypesMap } from '@/utils'
interface Props {
  inputs: { [k: string]: string }
}

// TODO: check if we need to update again also we have an issue with conversion 
// between `bool` in Python with value `True` vs JSON boolean with value `true`

const mapInputs = (inputs: { [k: string]: string }) => Object.keys(inputs || {})
  .map(key => (
    { name: key, type: InputTypesMap[key], value: inputs[key] })
  ).reduce((prev, curr) => {
    if (typeof curr.value === 'boolean') {
      prev = { ...prev, [curr.name]: curr.value ? 'True' : 'False' }
    } else {
      prev = { ...prev, [curr.name]: curr.value }
    }

    return prev
  }, {})

const setInputParams = (inputs: { [k: string]: string }) => {
  inputParams.value = Object.keys(inputs).map(key => ({ name: key, value: inputs[key] })).reduce((prev, curr) => {
    switch (curr.value) {
      case 'bool':
        prev = { ...prev, [curr.name]: false }
        break;
      case 'str':
        prev = { ...prev, [curr.name]: '' }
        break;
      case 'int':
        prev = { ...prev, [curr.name]: 0 }

        break;
      case 'float':
        prev = { ...prev, [curr.name]: 0.00 }

        break;
      default:
        prev = { ...prev, [curr.name]: '' }
        break;
    }
    return prev
  }, {})
}
const jsonParams = ref('{}')
const inputParams = ref<{ [k: string]: any }>({})
const props = defineProps<Props>()
const emit = defineEmits(['deployContract'])
const mode = ref<'json' | 'form'>('form')

const handleDeployContract = () => {
  if (mode.value === 'json') {
    const params = mapInputs(JSON.parse(jsonParams.value || '{}'))
    emit('deployContract', { params })
  } else {
    const params = mapInputs(inputParams.value || {})
    emit('deployContract', { params })
  }
}
const toogleMode = () => {
  mode.value = mode.value === 'json' ? 'form' : 'json'
  if (mode.value === 'json') {
    jsonParams.value = JSON.stringify(inputParams.value || {}, null, 2)
  }
}


watch((() => props.inputs), (newValue) => {
  if (Object.keys(newValue || {}).length > 0) {
    setInputParams(newValue)
  }
})

onMounted(() => {
  if (props.inputs) {
    setInputParams(props.inputs)
  }
})
</script>

<template>
  <div class="flex flex-col p-2 my-4">
    <div class="flex flex-col">
      <div class="flex justify-between align-middle">
        <div class="text-xs flex align-middle h-full">Constructor Parameters</div>
        <button class="bg-primary hover:opacity-80 text-white px-2 rounded texm-xs" @click="toogleMode">{{ mode ===
          'json' ? 'Inputs' : 'Json' }}
          <ToolTip :text="mode === 'json' ? 'See the inputs' : 'Write raw json'" :options="{ placement: 'top' }" />
        </button>
      </div>
      <p v-if="mode === 'json'" class="text-xs">Please provide a json object with the constructor parameters.</p>
    </div>
    <div class="flex mt-2" v-if="mode === 'json'">
      <textarea rows="5" class="w-full bg-slate-100 dark:dark:bg-zinc-700 p-2" v-model="jsonParams"
        clear-icon="ri-close-circle" label="State" />
    </div>
    <div class="flex mt-2" v-else>
      <div class="flex items-center py-2 justify-between" v-for="(inputType, input) in props.inputs" :key="input">
        <label :for="`${input}`" class="text-xs mr-2">{{ input }}</label>
        <input v-model="inputParams[input]" :name="`${input}`" :type="InputTypesMap[inputType]"
          :placeholder="`${input}`" class="bg-slate-100 dark:dark:bg-zinc-700 p-2" label="Input" />
      </div>
    </div>
  </div>
  <div class="flex flex-col p-2 w-full justify-center">
    <ToolTip text="Deploy" :options="{ placement: 'top' }" />
    <button @click="handleDeployContract"
      class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">
      Deploy
    </button>
  </div>

</template>

<style>
.editor {
  width: 100% !important;
  min-height: 20rem !important;
}
</style>
