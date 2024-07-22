<script setup lang="ts">
import { PresentationChartLineIcon } from '@heroicons/vue/24/solid'
import { SunIcon, MoonIcon } from '@heroicons/vue/16/solid'
import { useUIStore, useAccountsStore } from '@/stores'
import { shortenAddress } from '@/utils'
import { RouterLink } from 'vue-router'
import Logo from '@/assets/images/logo.svg'

const uiStore = useUIStore()
const accounts = useAccountsStore()
const toggleMode = () => {
    uiStore.toggleMode()
}
const showTutorial = () => {
    uiStore.runTutorial()
}
</script>

<template>
    <header
        class="flex justify-between items-center p-2 border-b border-b-slate-500 dark:border-b-zinc-500 dark:bg-zinc-800">
        <RouterLink to="/">
            <Logo alt="GenLayer Logo" height="36"
                :class="['block', uiStore.mode === 'light' ? 'text-primary' : 'text-white']" />
        </RouterLink>
        <div class="flex items-center gap-2 pr-2" id="tutorial-end">
            <RouterLink :to="{ name: 'profile' }"
                class="  hover:bg-slate-200 dark:hover:bg-zinc-700 rounded-md p-1 px-2">
                <span class="text-sm text-primary dark:text-white font-medium">
                    {{ shortenAddress(accounts.currentUserAddress || '') }}
                </span>
                <ToolTip :text="accounts.currentUserAddress" :options="{ placement: 'bottom' }" />
            </RouterLink>

            <button @click="toggleMode" class="hover:bg-slate-200 dark:hover:bg-zinc-700 rounded-md p-1">
                <SunIcon v-if="uiStore.mode === 'light'" class="h-5 w-5 fill-gray-700" />
                <MoonIcon v-else class="h-5 w-5 fill-gray-200" />
                <ToolTip text="Switch Theme" :options="{ placement: 'bottom' }" />
            </button>

            <button @click="showTutorial" class="hover:bg-slate-200 dark:hover:bg-zinc-700 rounded-md p-1">
                <PresentationChartLineIcon class="h-5 w-5"
                    :class="uiStore.mode === 'light' ? 'fill-gray-700' : 'fill-gray-200'" />
                <ToolTip text="Show Tutorial" :options="{ placement: 'bottom' }" />
            </button>
        </div>
    </header>
</template>
