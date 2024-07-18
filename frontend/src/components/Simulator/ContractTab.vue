<script setup lang="ts">
import { XMarkIcon, DocumentCheckIcon } from '@heroicons/vue/16/solid'
import { type ContractFile } from '@/types'
import { HomeIcon } from '@heroicons/vue/24/solid'

defineProps<{
    contract?: ContractFile,
    isHomeTab?: Boolean,
    isActive: Boolean,
}>()

const emit = defineEmits(['closeContract', 'selectContract'])
</script>

<template>
    <div :class="['group contract-item font-semibold flex items-center relative border-r border-r-gray-200 dark:border-r-zinc-900',
        !isActive && 'bg-gray-100 hover:bg-gray-50 text-neutral-500 dark:bg-zinc-800 hover:dark:bg-zinc-700',
        isActive && 'text-primary bg-white hover:bg-white dark:text-white dark:bg-zinc-600 hover:dark:bg-zinc-600']">

        <button v-if="isHomeTab" class="flex items-center p-2" @click="emit('selectContract')">
            <HomeIcon class="mx-2 h-4 w-4 dark:fill-white fill-primary'" />
        </button>

        <template v-else>
            <button class="flex items-center p-2 gap-1 pr-7" @click="emit('selectContract')"
                @click.middle="emit('closeContract')">
                <DocumentCheckIcon class="h-4 w-4" :class="{ 'dark:fill-white fill-primary': isActive }" />
                {{ contract?.name }}
            </button>

            <button
                :class="['absolute p-2 right-0', isActive && 'opacity-50 hover:opacity-100', !isActive && 'opacity-0 group-hover:opacity-100']"
                @click="emit('closeContract')" @click.middle="emit('closeContract')">
                <XMarkIcon class="h-4 w-4" />
            </button>
        </template>

        <div v-if="isActive" class="absolute bottom-0 w-full h-[2px] bg-primary dark:bg-accent" />
    </div>
</template>
