<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { InputTypesMap } from '@/utils'
import type { ContractMethod } from '@/types'
import LoadingIndicator from '@/components/LoadingIndicator.vue'

interface Props {
    title: string
    loading: boolean
    methods: ContractMethod[]
}

const props = defineProps<Props>()
const emit = defineEmits(['callMethod'])
const selectedMethod = ref<ContractMethod>()
const inputs = computed<{ [k: string]: any }>(() => {
    return props.methods.reduce((prev: any, curr) => {
        prev[curr.name] = {}
        return prev
    }, {})
})

const onMethodChange = (event: Event) => {
    const method = (event.target as HTMLSelectElement).value
    if (method) {
        selectedMethod.value = props.methods.find((m: ContractMethod) => m.name === method)
    } else selectedMethod.value = undefined
}

const handleMethodCall = () => {
    if (selectedMethod.value) {
        const params = Object.values(inputs.value[selectedMethod.value.name] || {})
        emit('callMethod', { method: selectedMethod.value.name, params })
        inputs.value[selectedMethod.value.name] = {}
    }
}

watch(() => props.methods, () => {
    selectedMethod.value = undefined
})

</script>
<template>
    <div class="flex flex-col px-2 mt-6 py-2 w-full bg-slate-100 dark:bg-zinc-700">
        <h5 class="text-sm">{{ title }}</h5>
    </div>
    <div class="flex flex-col p-2 overflow-y-auto">
        <div class="flex justify-start w-full mt-4">
            <select name="dropdown-execute-method" @change="onMethodChange" class="w-full dark:bg-zinc-700">
                <option value="">Select a method</option>
                <option v-for="method in methods" :key="method.name" :value="method.name">
                    {{ method.name }}()
                </option>
            </select>
        </div>
        <template v-if="selectedMethod">
            <div class="flex flex-col mt-4 w-full">
                <div class="flex items-center py-2 justify-between" v-for="(inputType, input) in selectedMethod.inputs"
                    :key="input">
                    <label :for="`${input}`" class="text-xs mr-2">{{ input }}</label>
                    <input v-model="inputs[selectedMethod.name][input]" :name="`${input}`"
                        :type="InputTypesMap[inputType]" :placeholder="`${input}`"
                        class="bg-slate-100 dark:dark:bg-zinc-700 p-2" label="Input" />
                </div>
            </div>
            <div class="flex flex-col mt-4 w-full">
                <ToolTip :text="`Execute ${selectedMethod.name}()`" :options="{ placement: 'top' }" />
                <button @click="handleMethodCall"
                    class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">
                    <LoadingIndicator v-if="props.loading" :color="'white'">
                    </LoadingIndicator>
                    <template v-else>Execute{{ ` ${selectedMethod.name}` }}()</template>
                </button>
                <slot name="results" :method-name="selectedMethod.name"></slot>
            </div>
        </template>
    </div>
</template>