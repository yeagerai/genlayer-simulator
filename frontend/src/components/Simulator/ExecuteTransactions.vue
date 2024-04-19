<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { InputTypesMap } from '@/utils'

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
}

const props = defineProps<Props>()
const emit = defineEmits(['callMethod'])

const methodList = computed(() => {
  return Object.entries(props.abi?.methods || {})
    .filter(m => m[0] !== 'call_llm')
    .map(m => ({
      name: m[0],
      inputs: m[1].inputs,
    }))
})

const inputs = ref<{ [k: string]: any }>({})

const handleMethodCall = (method: string) => {
  const params = Object.values(inputs.value[method] || {})
  emit('callMethod', { method, params })
}

watch(
  () => props.abi?.methods,
  () => {
    inputs.value = methodList.value.reduce((prev: any, curr) => {
      prev[curr.name] = {}

      return prev
    }, {})
  },
)
</script>

<template>
  <div class="flex flex-col px-2 mt-6 py-2 w-full bg-slate-100">
    <h5 class="text-sm">Execute transactions</h5>
  </div>
  <div class="flex flex-col p-2 m-h-20 overflow-y-auto">
    <!-- <VListItem
              v-for="method in methodList"
              :key="method.name"
            >
              <template #prepend>
                <VListItemAction start>
                  <VBtn @click="handleMethodCall(method.name)">
                    {{ method.name }}()
                  </VBtn>
                </VListItemAction>
              </template>
<template v-for="(inputType, input) in method.inputs" :key="input">
                <VCheckbox
                  v-if="inputType === 'bool'"
                  v-model="inputs[method.name][input]"
                  :label="`${input}`"
                />
                <VTextField
                  v-else
                  :key="input"
                  v-model="inputs[method.name][input]"
                  :type="InputTypesMap[inputType]"
                  :label="`${input}`"
                />
              </template>
</VListItem> -->
  </div>

</template>

<style>
.editor {
  width: 100% !important;
  min-height: 20rem !important;
}
</style>
