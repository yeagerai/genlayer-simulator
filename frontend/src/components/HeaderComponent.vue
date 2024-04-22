<script setup lang="ts">
import { SunIcon } from '@heroicons/vue/24/solid'
import { useUIStore } from '@/stores'
const uiStore = useUIStore()

const toogleMode = () => {
    uiStore.toogleMode()
}
</script>

<template>
    <header
        class="flex justify-between items-center p-2 border-b border-b-slate-500 dark:border-b-white/60 dark:bg-zinc-800">
        <a href="/">
            <img alt="GenLayer Logo" class="logo" src="@/assets/logo.png" width="125" height="125" />
        </a>
        <button class="mx-3" @click="toogleMode">
            <SunIcon class="h-5 w-5 fill-gray-700" v-if="uiStore.mode === 'light'" />
            <SunIcon class="h-5 w-5 fill-gray-200" v-else />
            <ToolTip text="Swtitch Theme" :options="{ placement: 'bottom' }" />
        </button>
    </header>
</template>
