<script setup lang="ts">
import { XMarkIcon, DocumentCheckIcon } from '@heroicons/vue/24/solid'
import { type ContractFile } from '@/types';

defineProps<{
    contract: ContractFile,
    isActive: boolean
}>()

const emit = defineEmits(['closeContract', 'selectContract'])
</script>

<template>
    <div :id="`contract-item-${contract.id}`"
        :class="['contract-item font-semibold flex justify-between text-neutral-500', isActive ? 'border-b-2 border-primary dark:text-white text-primary' : '']">
        <button class="bg-transparent flex p-2" @click="emit('selectContract')" @click.middle="emit('closeContract')">
            <DocumentCheckIcon class="h-4 w-4 mr-2" :class="{ 'dark:fill-white fill-primary': isActive }" />
            {{ contract.name }}
        </button>
        <button class="bg-transparent" @click="emit('closeContract')">
            <XMarkIcon class="ml-4 h-4 w-4" />
        </button>
    </div>
</template>
