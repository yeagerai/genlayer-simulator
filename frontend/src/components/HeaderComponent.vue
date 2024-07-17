<script setup lang="ts">
import { SunIcon, MoonIcon, PresentationChartLineIcon } from '@heroicons/vue/24/solid'
import { useUIStore, useAccountsStore } from '@/stores'
import { shortenAddress } from '@/utils'
import { RouterLink } from 'vue-router'


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
        class="flex justify-between items-center p-2 border-b border-b-slate-500 dark:border-b-white/60 dark:bg-zinc-800">
        <a href="/">
            <img v-if="uiStore.mode === 'light'" alt="GenLayer Logo" class="logo" src="@/assets/images/logo.png" width="125" height="125"/>
            <img v-else alt="GenLayer Logo" class="logo" src="@/assets/images/logo_white.png" width="125" height="125"/>
        </a>
        <div class="flex items-center" id="tutorial-end">
            <RouterLink :to="{ name: 'profile' }" class="text-sm  text-primary dark:text-white">
                {{ shortenAddress(accounts.currentUserAddress || '') }}
                <ToolTip :text="accounts.currentUserAddress" :options="{ placement: 'bottom' }" />
            </RouterLink>

            <button class="mx-3" @click="toggleMode">
                <SunIcon v-if="uiStore.mode === 'light'" class="h-5 w-5 fill-gray-700" />
                <MoonIcon v-else class="h-5 w-5 fill-gray-200" />
                <ToolTip text="Switch Theme" :options="{ placement: 'bottom' }" />
            </button>
            <button class="mx-3" @click="showTutorial">
                <PresentationChartLineIcon class="h-5 w-5 fill-gray-700" :class="uiStore.mode === 'light' ? 'fill-gray-700' : 'fill-gray-200'" />
                <ToolTip text="Show Tutorial" :options="{ placement: 'bottom' }" />
            </button>
        </div>
    </header>
</template>
