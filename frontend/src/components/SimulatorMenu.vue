<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { DocumentIcon, AdjustmentsHorizontalIcon, UserCircleIcon, CommandLineIcon } from '@heroicons/vue/24/solid'
</script>

<template>
    <nav class="flex flex-col items-center w-12 justify-between border-r border-r-slate-500 dark:border-r-white/60">
        <div class="flex flex-col items-center">
            <RouterLink :to="{ name: 'simulator.contracts' }"
                class="p-3 border-r-4 border-transparent opacity-75 hover:border-r-primary hover:opacity-100">
                <DocumentIcon class="h-6 w-6 fill-primary" />
                <ToolTip text="Contracts" :options="{ placement: 'right' }" />
            </RouterLink>
            <RouterLink :to="{ name: 'simulator.run-debug' }"
                class="p-3 border-r-4 border-transparent opacity-75 hover:border-r-primary hover:opacity-100">
                <CommandLineIcon class="h-6 w-6 fill-primary" />
                <ToolTip text="Run / Debug" :options="{ placement: 'right' }" />
            </RouterLink>
            <RouterLink :to="{ name: 'simulator.settings' }"
                class="p-3 border-r-4 border-transparent opacity-75 hover:border-r-primary hover:opacity-100">
                <AdjustmentsHorizontalIcon class="h-6 w-6 fill-primary" />
                <ToolTip text="Settings" :options="{ placement: 'right' }" />
            </RouterLink>
        </div>
        <div class="flex flex-col">
            <RouterLink :to="{ name: 'profile' }"
                class="p-3 border-r-4 border-transparent opacity-75 hover:border-r-primary hover:opacity-100">
                <UserCircleIcon class="h-6 w-6 fill-primary" />
                <ToolTip text="Profile" :options="{ placement: 'right' }" />
            </RouterLink>
        </div>
    </nav>
</template>

<style scoped></style>
